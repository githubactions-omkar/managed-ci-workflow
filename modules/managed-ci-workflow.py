# Import hashlib library (md5 method is part of it)
import hashlib
import logging
import os
import sys
import git
from typing import Dict, List, Union
from datetime import datetime

import yaml
from ruamel.yaml import YAML

sys.path.append(f'{os.path.dirname(__file__)}/..')
import subprocess
import utils.myutils as mu
from utils.myutils import file_exists, mkdir_p
from utils.github_apis import GitHubAPIs
from os import listdir
from os.path import isfile, join

import requests
import json

api_url = 'https://api.github.com/graphql'
github_token = os.environ['GITHUB_APP_TOKEN']
organisation = 'githubactions-omkar'
repositories = []
headers = {
    'Authorization': f'Bearer {github_token}',
    'Content-Type': 'application/json'
}

logger: Union[logging.Logger, None] = None
gh_obj = None
topdir = os.path.dirname(os.path.abspath(sys.argv[0]))
logdir = f'{topdir}/logdir'
file_name_pattern='managed-ci'

def main(module_name='', module_description='', repositories=[], default_managed_refspec=None):
    managed_ci_workflow_config_repo = 'tarun-repo-config'
    managed_ci_workflow_config_repo_path = f'{os.path.dirname(__file__)}/../../{managed_ci_workflow_config_repo}'
    managed_ci_workflow_config_repo_path = os.path.abspath(managed_ci_workflow_config_repo_path)
    print(f'managed_ci_workflow_config_repo_path: {managed_ci_workflow_config_repo_path} ..')
    files = os.listdir(managed_ci_workflow_config_repo_path)
    print(files)
    deployment_workflow_path = f'configs/workflow-deployment.yaml'

    if os.environ['RUN_EVENT'] == 'push':
        repo = git.Repo(managed_ci_workflow_config_repo_path)
        try:
          main_branch = repo.heads.main
        except AttributeError:
          raise ValueError("The {managed_ci_workflow_config_repo} repository does not have a branch named 'main'.")
        
        latest_commit_sha = main_branch.commit.hexsha
        second_top_commit = get_second_top_commit(managed_ci_workflow_config_repo_path)
        if not second_top_commit:
            sys.exit("Unable to get second top commit for the managed-ci-workflow-config repository..")
        print(f"Latest commit SHA of 'main': {latest_commit_sha}")
        try:
            file_commit_sha = get_file_content_from_commit(repo, latest_commit_sha, deployment_workflow_path)
            print(file_commit_sha, type(file_commit_sha))
            # print(f"Commit SHA of '{deployment_workflow_path}' in the latest commit: {file_commit_sha}")
            if file_commit_sha:
                try:
                    content_old = get_file_content_from_commit(repo, second_top_commit, deployment_workflow_path)
                    content_new = get_file_content_from_commit(repo, latest_commit_sha, deployment_workflow_path)
                except ValueError as e:
                    print(e)
            
                dict_old = load_yaml(content_old)
                dict_new = load_yaml(content_new)
                # Extract repositories data from dict1 and dict2
                repositories1 = dict_old['modules'][0]['repositories']
                repositories2 = dict_new['modules'][0]['repositories']
                
                changed_repositories = compare_repositories(repositories1, repositories2)
                print(f'Changed repositories: {changed_repositories}')
                process_all_repo(module_name='', module_description='', repositories=changed_repositories.get('repositories'), default_managed_refspec=None)
            else:
                print(f"File '{deployment_workflow_path}' does not exist in the latest commit {latest_commit_sha}")
        except ValueError:
          print(f"File '{deployment_workflow_path}' does not exist in the latest commit {latest_commit_sha}")
    else:
        logger.info("RUN EVENT is not a push event, hence running the script normally")
        process_all_repo(module_name='', module_description='', repositories=[], default_managed_refspec=None)

def process_all_repo(module_name='', module_description='', repositories=[], default_managed_refspec=None):
    """This Function processes all the repos passed to the function"""
    if not 'ORG_NAME' in os.environ:
        org_name='githubactions-omkar'
    else:
        org_name=os.environ['ORG_NAME']
    global managed_ci_workflow_repo
    managed_ci_workflow_repo='managed-ci-workflow'

    app_token = os.environ.get("GITHUB_APP_TOKEN", '')

    mu.mkdir_p(logdir)
    global logger
    global gh_obj
    ## Change values accordingly in get_logger()
    logger = mu.get_logger('workflow-deployer', f'{logdir}/workflow-deployer.log', level='debug', output_to_console=True)
    gh_obj = GitHubAPIs(org_name=org_name, token=app_token, logger=logger)
    # org_repos : List[str] = gh_obj.get_repo_names_in_org()
    org_repos = ['repo-1', 'repo-2', 'repo-3', 'managed-ci-workflow']

    logger.debug(f'Final list of Repos in the glcp org')

    # sq_data: Dict[str, List[Dict[str,str]]] = \
    #    # sonarqube_config(org_name=org_name)
    # num_sq_projects = len(sq_data['Projects'])

    new_deploys={}
    old_deploys={}
    for repo in repositories:
        r = repo.get('name')
        if r not in org_repos:
            # raise Exception(f"Repository {r} not found in {org_name} organization")
            print(f'{r} repo not found in {org_name}')
            continue
        refspec = repo.get('refspec', default_managed_refspec)
        optional_workflows_requested = repo.get('optional_workflows', [])
        full_build_system = repo.get('build_system', [])
        if full_build_system == []:
            build_system = full_build_system
        else:
            build_system = full_build_system[0]

        if gh_obj.check_is_repo_archived(r):
            logger.info(f'Repo "{r}" is Archived ...Skipping')
            continue

        # Clone participating project repo
        git_clone(org_name, r, app_token)

        # Clone managed-ci-workflow and checkout a specific refspec within the project repo directory.
        # Retieve workflows from manifest file.
        clone_status = git_clone(org_name, managed_ci_workflow_repo, app_token, refspec=refspec, directory=r)
        if not clone_status:
            logger.error(f'Failed to clone {r} repository for tag {refspec}. Hence skipping it...')
            continue
        versioned_ci_repo = f'{os.path.dirname(__file__)}/../../{r}/{managed_ci_workflow_repo}'
        versioned_ci_repo = os.path.abspath(versioned_ci_repo)
        template_workflow_path =f'{versioned_ci_repo}/templates'
        primary_workflow_path =f'{versioned_ci_repo}/workflows'
        workflow_manifest_file =f'{versioned_ci_repo}/workflow-manifest.yaml'

        primary_workflows, optional_workflows, template_workflows, custom_branch_workflows, cron_workflows, build_system_workflows = workflow_manifest(workflow_manifest_file, build_system)
        
        workflow_sources=[]
        workflow_exists=[]
        for twf in template_workflows:
            if not gh_obj.check_workflow_file(r, twf):
                # File does not exist, exists at 0 bytes, or other exception
                workflow_sources.append(f'{template_workflow_path}/{twf}')
            else:
                workflow_exists.append(f'{template_workflow_path}/{twf}')
        for owf in optional_workflows:
            if owf not in optional_workflows_requested:
                continue
            source = f'{primary_workflow_path}/common/{owf}'
            dest = get_dest_workflow_path(r, owf)
            logger.debug(f'comparing optional workflow {source} vs. {dest}')
            if not gh_obj.check_workflow_file(r, owf):
                # File does not exist, exists at 0 bytes, or other exception
                logger.debug(f'workflow {owf} does not exist in {r}')
                workflow_sources.append(f'{primary_workflow_path}/common/{owf}')
            else:
                if owf in cron_workflows:
                    cron_wf_update(owf, r, "common")               
                logger.info(f'optional workflow file {owf} exists for repo {r}')
                source_md5sum = calc_template_md5sum(f'{primary_workflow_path}/common/{owf}')
                dest_md5sum = calc_template_md5sum(dest)
                logger.debug(f'md5sum of source optional workflow file {source_md5sum}')
                logger.debug(f'md5sum of user repo {r} optional workflow file {dest_md5sum}')
                if not source_md5sum == dest_md5sum:
                    workflow_sources.append(f'{primary_workflow_path}/common/{owf}')
                    logger.debug(f'need to deploy source optional workflow file to repo "{r}"')
                else:
                    workflow_exists.append(f'{primary_workflow_path}/common/{owf}')
                    logger.debug(f'md5sum of master repo and user repo {r} workflow {owf} is the same.  skipping deployment.')
                    if owf in cron_workflows:
                        cron_wf_revert(owf, r)                      
        for pwf in primary_workflows:
            source = f'{primary_workflow_path}/common/{pwf}'
            dest = get_dest_workflow_path(r, pwf)
            logger.debug(f'comparing primary workflow {source} vs. {dest}')
            if not gh_obj.check_workflow_file(r, pwf):
                # File does not exist, exists at 0 bytes, or other exception
                logger.debug(f'workflow {pwf} does not exist in {r}')
                workflow_sources.append(f'{primary_workflow_path}/common/{pwf}')
            else:
                logger.info(f'primary workflow file {pwf} exists for repo {r}')
                if pwf in custom_branch_workflows:
                    custom_branch_update(pwf, r, "common")
                source_md5sum = calc_template_md5sum(f'{primary_workflow_path}/common/{pwf}')
                dest_md5sum = calc_template_md5sum(dest)
                logger.debug(f'md5sum of source primary workflow file {source_md5sum}')
                logger.debug(f'md5sum of user repo {r} primary workflow file {dest_md5sum}')
                if not source_md5sum == dest_md5sum:
                    workflow_sources.append(f'{primary_workflow_path}/common/{pwf}')
                    logger.debug(f'need to deploy source primary workflow file to repo "{r}"')
                else:
                    workflow_exists.append(f'{primary_workflow_path}/common/{pwf}')
                    logger.debug(f'md5sum of master repo and user repo {r} workflow {pwf} is the same.  skipping deployment.')
        for bswf in build_system_workflows:
            source = f'{primary_workflow_path}/{build_system}'
            dest = get_dest_workflow_path(r, bswf)
            logger.debug(f'comparing {build_system} Build System workflow {source} vs. {dest}')
            if not gh_obj.check_workflow_file(r, bswf):
                # File does not exist, exists at 0 bytes, or other exception
                logger.debug(f'workflow {bswf} does not exist in {r}')
                workflow_sources.append(f'{primary_workflow_path}/{build_system}/{bswf}')
            else:
                logger.info(f'{build_system} Build System workflow file {bswf} exists for repo {r}')
                if bswf in custom_branch_workflows:
                    custom_branch_update(bswf, r, build_system)
                source_md5sum = calc_template_md5sum(f'{primary_workflow_path}/{build_system}/{bswf}')
                dest_md5sum = calc_template_md5sum(dest)
                logger.debug(f'md5sum of source Build System workflow file {source_md5sum}')
                logger.debug(f'md5sum of user repo {r} Build System workflow file {dest_md5sum}')
                if not source_md5sum == dest_md5sum:
                    workflow_sources.append(f'{primary_workflow_path}/{build_system}/{bswf}')
                    logger.debug(f'need to deploy source Build System workflow file to repo "{r}"')
                else:
                    workflow_exists.append(f'{primary_workflow_path}/{build_system}/{bswf}')
                    logger.debug(f'md5sum of master repo and user repo {r} workflow {bswf} is the same.  skipping deployment.')
        
        wf_cleanup(primary_workflows=primary_workflows, template_workflows=template_workflows, optional_workflows=optional_workflows, build_system_workflows=build_system_workflows, repo_name=r)
        git_push_workflows(r, workflow_sources, app_token)

        # Add to the dict of new deployments for the report
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        old_deploys[r] = {}
        old_deploys[r]['refspec'] = refspec
        old_deploys[r]['workflows'] = [{'name': os.path.basename(wf)} for wf in workflow_exists]
        new_deploys[r] = {}
        new_deploys[r]['refspec'] = refspec
        new_deploys[r]['workflows'] = [{'name': os.path.basename(wf), 'updated': timestamp} for wf in workflow_sources]

        # sonarqube_config(sq_data, r, gh_obj.get_default_branch(r))

    # if len(sq_data['Projects']) > num_sq_projects:
    #     sonarqube_config(sq_data, save=True)
    # else:
    #     logger.debug('nothing to push... all repos are present in the SonarQube config file')
        
    repository_statuscheck_secrets(repositories)
    update_log_file(new_deploys=new_deploys, old_deploys=old_deploys)

def repository_statuscheck_secrets(repositories):
    '''This functions adds status checks and secrets to required repositories'''
    repository_list = [reps['name'] for reps in repositories]
    if bool(repository_list):
        common_secrets = get_config(item='common-secrets', data_type=[])
        create_list_repo_ids(repository_list, common_secrets)
    else:
        logger.debug("Unable to fetch repository names from input file")

    for repository in repositories:
        repo_name = repository.get('name')
        refspec = repository.get('refspec')
        try:
            optional_workflows = repository.get('optional_workflows', [])
        except IndentationError:
            optional_workflows = []
        try:
            language = repository.get('language', [])
            language = ', '.join(language)
        except IndentationError:
            language = ''
        try:
            specific_secrets = get_config(item='optional-secrets', data_type=[])
            spl_secrets = specific_secrets['ft-secrets']
        except KeyError:
            spl_secrets = []
        try:
            check_repo_exist(repo_name, refspec, optional_workflows, language)
        except Exception as e:
            logger.debug(f'Error while working on {repo_name}: {str(e)}')
            continue
        try:
            repo_name = list(repo_name.split(" "))
            create_list_repo_ids(repo_name, spl_secrets)
        except Exception as e:
            logger.debug(f'Error while updating specific secrets {spl_secrets} on {repo_name}: {str(e)}')

def workflow_manifest(manifest_file, build_system):
    with open(manifest_file, "r") as f:
        data = yaml.safe_load(f)
        if build_system == []:
            return data.get('primary_workflows', []), data.get('optional_workflows', []), data.get('template_workflows', []), data.get('custom_branch_workflows', []), data.get('cron_workflows', []), []
    return data.get('primary_workflows', []), data.get('optional_workflows', []), data.get('template_workflows', []), data.get('custom_branch_workflows', []), data.get('cron_workflows', []), data.get(build_system, [])


def custom_branch_update(custom_branch_workflow: str, repo_name: str, type: str):
    if type != "common":
        workflow_path = f'/{type}'
    else:
        workflow_path = "/common"
    primary_workflow_path =f'{os.path.dirname(__file__)}/../../{repo_name}/{managed_ci_workflow_repo}/workflows{workflow_path}'
    default_branch = gh_obj.get_default_branch(repo_name)
    with open(f'{primary_workflow_path}/{custom_branch_workflow}', 'r') as file:
        yaml_contents = yaml.safe_load(file)
    default_branches_list =  yaml_contents[True]['push']['branches']
    if default_branch not in default_branches_list:
        logger.debug(f'CUSTOM WF File to be updated : {custom_branch_workflow}')
        cmds = [f'cd {primary_workflow_path} ; sed -i "/branches:/a \ \ \ \ \ \ - {default_branch}" {custom_branch_workflow}'
                ]
        for cmd in cmds:
            ec, out, err = run_subprocess(cmd)
        if ec:
            sys.exit(1)    

def cron_wf_update(cron_workflow: str, repo_name: str, type: str):
    if type != "common":
        workflow_path = f'/{type}'
    else:
        workflow_path = "/common"
    workflow_path=f'{os.path.dirname(__file__)}/../../{repo_name}/.github/workflows/'
    primary_workflow_path =f'{os.path.dirname(__file__)}/../{repo_name}/{managed_ci_workflow_repo}/workflows{workflow_path}'
    logger.debug(f'cron file to be updated : {cron_workflow}')
    cmds = [f'cd {workflow_path}; cp {cron_workflow} {cron_workflow}.bkp; sed -i  "s/cron:.*/cron:/"  {cron_workflow}'
                ]
    for cmd in cmds:
        ec, out, err = run_subprocess(cmd)
    if ec:
        sys.exit(1) 
    
def cron_wf_revert(cron_workflow: str, repo_name: str):
    workflow_path=f'{os.path.dirname(__file__)}/../../{repo_name}/.github/workflows/'
    logger.debug(f'cron file to be reverted : {cron_workflow}')
    cmds = [f'cd {workflow_path} ; mv {cron_workflow}.bkp {cron_workflow}'
                ]
    for cmd in cmds:
        ec, out, err = run_subprocess(cmd)
    if ec:
        sys.exit(1) 
        
def wf_cleanup(primary_workflows=[], template_workflows=[], optional_workflows=[], build_system_workflows=[], repo_name=''):
     # This function will remove the files from the remote repo if the files are not mentioned 
    # in the manifest file  and the file names start with file name pattern 'managed-ci'.
    workflow_dir=f'{os.path.dirname(__file__)}/../../{repo_name}/.github/workflows'
    if not os.path.exists(workflow_dir):
        os.makedirs(workflow_dir)
    wf_files_in_user_repo = [f for f in listdir(workflow_dir) if isfile(join(workflow_dir, f))]
    wf_names=primary_workflows + template_workflows + optional_workflows + build_system_workflows
    wf_files_to_be_deleted=[]
    for i in wf_files_in_user_repo:
        if i in wf_names:
            logger.debug(f'This file {i} is being skipped from deletion because this file is in the manifest')
            continue
        if i.startswith(file_name_pattern):
            logger.debug(f'This file {i} is being added to deletion list because this file is not the manifest and it starts with {file_name_pattern} pattern')
            wf_files_to_be_deleted.append(i)
        else:
            logger.debug(f'This file {i} is being skipped from deletion list because this files are from user repo')
    for i in wf_files_to_be_deleted:
        logger.debug(f'WF File to be deleted: {i}')
        cmds=[f'cd {workflow_dir}; git rm {i}']
        cmds = [
            f'cd {workflow_dir}; git rm {i}',
            f'cd {workflow_dir}; git add .',
            f"cd {repo_name}; git commit -m '[skip actions] delete workflow(s) {i}'"
           ]
        for cmd in cmds:
            ec, out, err = run_subprocess(cmd)
            if ec:
                logger.error(f'{cmd} failed with exit code: {ec}')
                logger.error(f'stdout: {out.decode()}')
                logger.error(f'stderr: {err.decode()}')
                sys.exit(1)
    cmd=f'cd {repo_name}; git push' 
    ec, out, err = run_subprocess(cmd)
    if ec:
        logger.error(f'{cmd} failed with exit code: {ec}')
        logger.error(f'stdout: {out.decode()}')
        logger.error(f'stderr: {err.decode()}')
        sys.exit(1)

def get_dest_workflow_path(repo_name, workflow):
    workflow_path=f'{os.path.dirname(__file__)}/../../{repo_name}/.github/workflows/{workflow}'
    workflow_path = os.path.abspath(workflow_path)
    if file_exists(workflow_path, check_nonzero_filesize=True):
        return workflow_path
    return None

def calc_template_md5sum(pr_template):
    print(f'calc_template_md5sum pr_template {pr_template} {type(pr_template)}')
    with open(pr_template, 'rb') as fh:
        data = fh.read()
        pr_template_md5 = hashlib.md5(data).hexdigest()
    return pr_template_md5

def git_clone(org_name: str, repo_name: str, token: str, refspec=None, directory=None):
    logger.debug(f"git clone {org_name}/{repo_name}")
    git_url=f'https://x-access-token:{token}@github.com/{org_name}/{repo_name}.git'
    cmd=f'git clone {git_url}'
    if directory:
        cmd=f'cd {directory}; {cmd}'
    if refspec:
        cmd=f'{cmd}; cd {repo_name}; git checkout {refspec}'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    out, err = proc.communicate()
    ec = proc.returncode
    if ec > 0:
        logger.error(f'cmd failed with exit code: {ec}')
        logger.error(f'stdout: {out.decode()}')
        logger.error(f'stderr: {err.decode()}')
        return False
        # sys.exit(2)
    else:
        return True

def run_subprocess(cmd: str, abort_on_error=False):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    out, err = proc.communicate()
    ec = proc.returncode
    if ec > 0:
        logger.error(f'cmd: {cmd}')
        logger.error(f'exit code: {ec}')
        logger.error(f'stdout: {out.decode()}')
        logger.error(f'stderr: {err.decode()}')
        if abort_on_error:
            raise Exception(f'the cmd "{cmd}" failed... see stdout/stderr above')
    else:
        logger.debug(f'stdout: {out.decode()}')
    return ec, out, err

def git_push_workflows(repo_name: str, workflow_sources: List, token):
    workflow_dest=f'{os.path.dirname(__file__)}/../../{repo_name}/.github/workflows'
    mu.mkdir_p(workflow_dest)
    wf_basenames = []
    
    # Copy workflow sources to participating repository.   Add to git.
    for wf in workflow_sources:
        filename = os.path.basename(wf)
        wf_basenames.append(filename)
        cmds = [f'cp -fp {wf} {workflow_dest}/{filename}',
                f'cd {workflow_dest} && git add -f {filename}']
        for cmd in cmds:
            ec, out, err = run_subprocess(cmd)
            if ec:
                sys.exit(1)         
 
    
    # Drop out if git status indicates that nothing has changed
    cmd=f'cd {repo_name}; git status'
    ec, out, err = run_subprocess(cmd)
    if ec:
        sys.exit(1)
    if not 'modified:' in out.decode() and not 'new file:' in out.decode():
        logger.debug(f'No workflow changes for repo {repo_name}. Skipping.')
        return

    # Commit and push
    wf_push_list = ', '.join(wf_basenames)
    cmds = [
            f"cd {repo_name}; git commit -m '[skip actions] added/updated workflow(s) {wf_push_list}'",
            f'cd {repo_name}; git push'
           ]
    for cmd in cmds:
        ec, out, err = run_subprocess(cmd)
        if ec:
            sys.exit(1)

def sonarqube_config(data=None, repo_name=None, default_branch_name=None,
                     org_name=None, save=False) -> Union[Dict[str, List[Dict[str,str]]], None]:
    """
    This function operates in 3 modes:
      1. Retrieve the existing SonarQube config from the "devx-sonarqube" repo
          if the "data" param is None
      2. Write the updated SonarQube config changes ("data" param) back to the
          SonarQube config YAML file and push the changes if the "save" param is True.
      3. Update the SonarQube config data struct ("data" param) if the repo
          name and default branch name are provided
    """

    sq_repo_name = 'devx-sonarqube'
    filename = os.environ.get('SQ_CONFIG_FILENAME', 'sonar.yaml')
    yaml_filename = f'{sq_repo_name}/sonarqube-management/sonar_data/{filename}'
    yaml = YAML()

    if not data:
        git_clone(org_name, sq_repo_name, os.environ["GITHUB_APP_TOKEN"],
                  refspec=os.environ.get('SQ_BRANCH_NAME', None))
        with open(yaml_filename, 'rb') as fh:
            data = yaml.load(fh)
        return data

    if save:
        logger.debug(f'updating SonarQube config file "{yaml_filename}" ...')
        yaml.indent(mapping=2, sequence=4, offset=2)
        with open(f'{yaml_filename}', 'wb') as fh:
            yaml.dump(data, fh)
        git_push_sonarqube_config(yaml_filename, sq_repo_name)
        # the GitHub Action that invoked this Python script will check for the
        # existence of this file.  If this file exists, then the
        # workflow "sonar.yaml" in the "devx-sonarqube" GitHub repo will be invoked
        logger.debug(f'creating "need-sq-onboarding.txt" ...')
        with open('need-sq-onboarding.txt', 'w') as fh:
            fh.write('yes please')
        return

    projects: List[Dict[str, str]] = data['Projects']
    if not any(d['name'] == repo_name for d in projects):
        logger.debug(f'repo "{repo_name}" not found in SonarQube config; adding it...')
        projects.append({'name': repo_name,
                         'branch': default_branch_name,
                         'qualitygate': 'glcp-sonarqube'})
    else:
        logger.debug(f'repo "{repo_name}" found in SonarQube config; nothing to do...')

def git_push_sonarqube_config(yaml_filename: str, repo_name: str) -> None:
    """
    Push the updated SonarQube config changes to the "devx-sonarqube" repo
    """

    yaml_path = yaml_filename.rsplit('/', 1)[0]
    filename = yaml_filename.rsplit('/', 1)[1]

    cmds = [
            (f'cd {yaml_path}; '
             f'git commit -m "[skip actions] Onboarding repo(s)" {filename}'
            ),
            f'cd {repo_name}; git push'
           ]
    for cmd in cmds:
        run_subprocess(cmd, abort_on_error=True)

def update_log_file(new_deploys, old_deploys, report_filename=f'devops-reports/workflow-reports/workflows-deployed.yaml'):
    mkdir_p(os.path.dirname(report_filename))

    print(yaml.dump(new_deploys, default_flow_style=False))

    if mu.file_exists(report_filename):
        with open(report_filename,'r') as report_f:
            try:
                report = yaml.safe_load(report_f).get('repositories', {})
            except AttributeError:
                report = {}
            '''
            This hack of a block ensures that the report includes references to workflows even if we have
            not deployed to them on this run.
            '''
            for repo in old_deploys.keys():
                # if this repo is not present in the existing report, append it and move on to the next
                if repo not in report.keys():
                    report.update({repo: old_deploys[repo]})
                    continue
                # for each of the already deployed workflows, check to see if its name is in the workflow list
                # of the current repo.  If not, append it.
                for wf in old_deploys.get(repo, {}).get('workflows', []):
                    if wf.get('name') not in [x.get('name') for x in report.get(repo, {}).get('workflows', [])]:
                        report[repo]['workflows'].append(wf)
            for repo in new_deploys.keys():
                # if this repo is not present in the existing report, append it and move on to the next
                if repo not in report.keys():
                    report.update({repo: new_deploys[repo]})
                    continue
                # we're working with a repo that is already in the report.
                # - if we have deployed an existing workflow, update the 'updated' field
                # - if this is a new workflow, add the workflow name and deployment update fields
                for wf in new_deploys.get(repo, {}).get('workflows', []):
                    matched = False
                    for report_wf in report.get(repo, {}).get('workflows', []):
                        if report_wf.get('name') == wf.get('name'):
                            report_wf['updated'] = wf.get('updated')
                            matched = True
                            break
                    if not matched:
                        report[repo]['workflows'].append(wf)
    else:
        report = new_deploys

    with open(report_filename, mode = 'w') as report_f:
        report_f.write(yaml.dump({'repositories': report}, default_flow_style=False, sort_keys=False))

def get_config(item='', data_type=any):
    '''This function checks if requested item exists in deployer-config.yaml or not'''
    # Read the YAML configuration file
    deployer_config_path = os.path.abspath(f'{os.path.dirname(__file__)}/../deployer-config.yaml')
    with open(deployer_config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    try:
        item = config[item]
    except KeyError:
        # logger.debug(f'{item} is not available in deployer-config.yaml')
        print(f'{item} is not available in deployer-config.yaml')
        item = data_type
    return item

def create_list_repo_ids(repositories, secrets):
    """This functions creates list of repository ids where secret access needs to be updated"""
    auth_header = {'Authorization': 'token '+github_token, 'X-GitHub-Api-Version': '2022-11-28', 'Accept': 'application/vnd.github+json'}
    repository_ids = []
    for repo in repositories:
        githubapi = f"https://api.github.com/repos/{organisation}/{repo}"
        repo_response = requests.get(githubapi, headers=auth_header)
        repository_ids.append(repo_response.json()['id'])
    # if bool(repository_ids):
    #     update_secret_access_to_repo(repository_ids, secrets)
    # else:
    #     logger.debug("Unable to create list of repository ids")

def update_secret_access_to_repo(repository_ids, secrets):
    """This function adds the repositories for to access Organisation secrets"""
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {github_token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    if len(secrets) != 0:
        for secret in secrets:
            url = f"https://api.github.com/orgs/{organisation}/actions/secrets/{secret}/repositories"
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                response_data = json.loads(response.text)
                existing_repo_ids = [rule ["id"] for rule in response_data["repositories"]]
                repo_ids = list(set(existing_repo_ids + repository_ids))
                data = {
                    "selected_repository_ids": repo_ids
                }
            # except requests.exceptions.RequestException as e:
            #     logger.debug(f'Error while fetching existing repository names for {secret} secret')
            # try:
                response = requests.put(url, headers=headers, json=data)
                response.raise_for_status()
                logger.info(f'Updated access to the {secret} secret for given repos')
            except requests.exceptions.RequestException as e:
                logger.debug(f"Failed to update the secret access for repository. Status code: {response.status_code} {str(e)}")
    else:
        logger.debug("Secrets are not defined in deployer-config.yaml file")

def check_repo_exist(repository, refspec, optional_workflows, language):
    """ This Function checks if given Github Repo exists """
    query = f'''
    query {{
        repository(owner: "{organisation}", name: "{repository}") {{
            id
        }}
    }}
    '''
    try:
        response = requests.post(api_url, json={"query": query}, headers=headers)
        response.raise_for_status()
        repository_id = response.json().get("data", {}).get("repository")['id']
        if repository_id:
            get_default_branch(repository_id, repository, refspec, optional_workflows, language)
        else:
            logger.debug(f"The repository '{repository}' does not exist.")
            raise ValueError("The repository '{repository}' does not exist.")
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to query GitHub GraphQL API. Status code: {response.status_code} {str(e)}")
        raise ValueError("The repository '{repository}' does not exist.")

def get_default_branch(repository_id, repository, refspec, optional_workflows, language):
    """ This Function gets default branch for given repo """
    query = f'''
    query {{
    repository(owner: "{organisation}", name: "{repository}") {{
        defaultBranchRef {{
        name
        }}
    }}
    }}
    '''
    variables = {
        "owner": organisation,
        "name": repository
    }
    
    try:
        response = requests.post(api_url, headers=headers, json={'query': query, 'variables': variables})
        response.raise_for_status()
        default_branch = response.json()['data']['repository']['defaultBranchRef']['name']
        check_if_branch_protected(repository, repository_id, default_branch, refspec, optional_workflows, language)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to retrieve the default branch. Status code:, {str(e)}")

def check_if_branch_protected(repository, repository_id, default_branch, refspec, optional_workflows, language):
    """ This function checks if branch protection is already enabled for default branch"""
    query = '''
    query {
    repository(owner: "%s", name: "%s") {
        branchProtectionRules(first: 100) {
        nodes {
            id
            requiredStatusCheckContexts
            pattern
        }
        }
    }
    }
    ''' % (organisation, repository)
    try:
        response = requests.post(api_url, json={"query": query}, headers=headers)
        response.raise_for_status()
        data = response.json().get("data", {}).get("repository", {}).get("branchProtectionRules", {}).get("nodes", [])
        response_data = json.loads(response.text)
        protected_branches = [rule["pattern"] for rule in response_data["data"]["repository"]["branchProtectionRules"]["nodes"]]
        if default_branch not in protected_branches:
            try:
                protected_status_check_context = data[0].get('requiredStatusCheckContexts')
            except:
                protected_status_check_context = []
            updated_status_check_context = evaluate_context_for_bpr(refspec, repository, protected_status_check_context)
            branch_protection_rule(repository, default_branch, updated_status_check_context)
        else:
            for rule in response_data["data"]["repository"]["branchProtectionRules"]["nodes"]:
                if rule["pattern"] == default_branch:
                    protection_rule_id = rule["id"]
                    protected_status_check_context = rule["requiredStatusCheckContexts"]
                    updated_status_check_context = evaluate_context_for_bpr(refspec, repository, protected_status_check_context)
                    branch_protection_rule(repository, default_branch, updated_status_check_context)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to query GitHub GraphQL API. Status code: {response.text} {str(e)}")
        protected_status_check_context = []
        updated_status_check_context = evaluate_context_for_bpr(refspec, repository, protected_status_check_context)
        branch_protection_rule(repository, default_branch, updated_status_check_context)

def remove_none_values(d):
    return {
        k: remove_none_values(v) if isinstance(v, dict) else v
        for k, v in d.items() if v is not None
    }

def add_missing_keys(dictionary, keys, default_value=None):
    for key in keys:
        if key not in dictionary:
            dictionary[key] = default_value

def branch_protection_rule(repository, default_branch, updated_status_check_context):
    """This function creates/updates the branch protection rule for the given repository"""
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {github_token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    url = f'https://api.github.com/repos/{organisation}/{repository}/branches/{default_branch}/protection'
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    if response.status_code == 404:
        logger.error(f"Branch protection rule not found for the {organisation}/{repository}.")
        print('create a new rule')
    try:
        required_pull_request_reviews_count = response_json["required_pull_request_reviews"]["required_approving_review_count"]
        if required_pull_request_reviews_count != 0:
            try:
                dismisss_stale_reviews = response_json["required_pull_request_reviews"]["dismiss_stale_reviews"]
            except KeyError:
                dismisss_stale_reviews = False
            try:
                dismissal_restrictions  = response_json["required_pull_request_reviews"]["dismissal_restrictions"]
                if dismissal_restrictions:
                    dismissal_restrictions_data = {
                        "users": dismissal_restrictions.get("users", []),
                        "teams": dismissal_restrictions.get("teams", []),
                        "apps": dismissal_restrictions.get("apps", [])
                    }
                else:
                    dismissal_restrictions_data = None
            except KeyError:
                dismissal_restrictions_data = { "users": [], "teams": [], "apps": [] }
            try:
                bypass_pull_request_allowances = response_json["required_pull_request_reviews"]["bypass_pull_request_allowances"]
                bypass_pull_request_allowances_data = {
                                "users": bypass_pull_request_allowances.get("users", []),
                                "teams": bypass_pull_request_allowances.get("teams", []),
                                "apps": bypass_pull_request_allowances.get("apps", [])
                            }
            except KeyError:
                bypass_pull_request_allowances_data = None
            required_pull_request_reviews = {
                "dismiss_stale_reviews" : dismisss_stale_reviews,
                "dismissal_restrictions": dismissal_restrictions_data,
                "dismiss_stale_reviews": response_json["required_pull_request_reviews"]["dismiss_stale_reviews"] if 'dismiss_stale_reviews' in response_json["required_pull_request_reviews"] else False,
                "require_code_owner_reviews": response_json["required_pull_request_reviews"]["require_code_owner_reviews"] if 'require_code_owner_reviews' in response_json["required_pull_request_reviews"] else False,
                "required_approving_review_count": response_json["required_pull_request_reviews"]["required_approving_review_count"] if 'required_approving_review_count' in response_json["required_pull_request_reviews"] else 0,
                "require_last_push_approval": response_json["required_pull_request_reviews"]["require_last_push_approval"] if 'require_last_push_approval' in response_json["required_pull_request_reviews"] else False,
                "bypass_pull_request_allowances": bypass_pull_request_allowances_data
            }
        else:
            required_pull_request_reviews = None
    except KeyError:
        required_pull_request_reviews = None
    try:
        restrictions_variables = [
            response_json["restrictions"].get("users", []),
            response_json["restrictions"].get("teams", []),
            response_json["restrictions"].get("apps", [])
        ]
        if any(variable for variable in restrictions_variables if variable != []):
            restrictions_variables = {
                "users": response_json["restrictions"].get("users", []),
                "teams": response_json["restrictions"].get("teams", []),
                "apps": response_json["restrictions"].get("apps", [])
            }
        else:
            restrictions_variables = None
    except KeyError:
        restrictions_variables = None
    payload_schema = {
        "required_status_checks":
        {
            "strict": False,
            "contexts": updated_status_check_context
        },
        "enforce_admins": response_json['enforce_admins']['enabled'] if 'enforce_admins' in response_json else None,
        "required_pull_request_reviews": required_pull_request_reviews,
        "restrictions": restrictions_variables,
        "required_linear_history": response_json["required_linear_history"]["enabled"] if 'required_linear_history' in response_json else False,
        "allow_force_pushes": response_json["allow_force_pushes"]["enabled"] if 'allow_force_pushes' in response_json else False,
        "allow_deletions": response_json["allow_deletions"]["enabled"] if 'allow_deletions' in response_json else False,
        "block_creations": response_json["block_creations"]["enabled"] if 'block_creations' in response_json else False,
        "required_conversation_resolution": response_json["required_conversation_resolution"]["enabled"] if 'required_conversation_resolution' in response_json else False,
        "lock_branch": response_json["lock_branch"]["enabled"] if 'lock_branch' in response_json else False,
        "allow_fork_syncing": response_json["allow_fork_syncing"]["enabled"] if 'allow_fork_syncing' in response_json else False
    }
    cleaned_payload = remove_none_values(payload_schema)
    required_keys = ['required_pull_request_reviews', 'restrictions']
    add_missing_keys(cleaned_payload, required_keys)
    response = requests.put(url, headers=headers, json=cleaned_payload)
    response.raise_for_status()
    
    if response.status_code == 200:
        logger.info(f'Branch protection rule created successfully for {repository} on default branch {default_branch}.')
    else:
        logger.debug(f'Failed to create branch protection rule for {repository} on default branch {default_branch}.')

def evaluate_context_for_bpr(refspec, repository, protected_status_check_context):
    """This function evaluates the CONTEXT for branch protection rule and returns the context and language"""
    default_tag_status_context = get_config(item='default_tag_status_context', data_type={})
    delete_status_checks = get_config(item='delete_status_checks', data_type=[])
    default_tag_status_context_list = []
    for key, value in default_tag_status_context.items():
        default_tag_status_context_list.extend(value)
    delete_status_checks = list(set(delete_status_checks + default_tag_status_context_list))
    protected_status_check_list = [item for item in protected_status_check_context if item not in delete_status_checks]
    tag_status_context = []
    default_tag_status_values = list(default_tag_status_context.values()) + [list(protected_status_check_context)]
    if len(default_tag_status_context) > 0 and refspec:
        for key in default_tag_status_context.keys():
            if refspec.startswith(key):
                tag_status_context = default_tag_status_context[key]
                if refspec == key:
                    tag_status_context = default_tag_status_context[key]
                    break

    # Get lanaguage variable value for this repository
    try:
        lang_variable = get_config(item='lang_variable', data_type='')
        response = requests.get(url=f"https://api.github.com/repos/{organisation}/{repository}/actions/variables/{lang_variable}", headers=headers)
        response.raise_for_status()
        language = response.json()['value']
        default_language_context = get_config(item='default_language_context', data_type={})
        if language in default_language_context:
            language_context = default_language_context[language]
        else:
            logger.info(f"{lang_variable} status check context not found in deployer-config.yaml")
            print(f"{lang_variable} status check context not found in deployer-config.yaml")
            language_context = []
    except requests.exceptions.RequestException:
        logger.debug(f'{lang_variable} repository variable not found in {repository}.')
        print(f'{lang_variable} repository variable not found in {repository}.')
        language_context = []
    required_status_check_contexts = get_config(item='required_status_check_contexts', data_type=[])
    join_status_context = list(set(protected_status_check_list + required_status_check_contexts + tag_status_context + language_context))
    return join_status_context

def load_yaml(file_content):
    """Read workflow-deployment.yaml content into a dictionary."""
    return yaml.safe_load(file_content)

def get_second_top_commit(repo_path):
    repo = git.Repo(repo_path)
    try:
        branch = repo.heads.main
    except AttributeError:
        logger.error("The repository does not have a branch named 'main'.")
        return False

    commits = list(repo.iter_commits(branch.name, max_count=2))
    print(commits)
    if len(commits) < 2:
        logger.error("There are less than two commits in the 'main' branch.")
        return False

    second_top_commit = commits[1]
    commit = repo.commit(commits[0])
    parent_commit = commit.parents[0] if commit.parents else None
    if parent_commit:
        diff = commit.diff(parent_commit)
        changed_files = []
        for change in diff:
            file_info = {
                'file': change.a_path,  # the file name
                'change_type': change.change_type  # 'A', 'M', or 'D'
            }
            changed_files.append(file_info)
        print(changed_files)
    return second_top_commit

def get_file_content_from_commit(repo, commit_sha, file_path):
    """Get the content of a file from a specific commit SHA."""
    print(f'printing get_file_content_from_commit ')
    commit = repo.commit(commit_sha)
    try:
        file_blob = commit.tree[file_path]
        file_content = file_blob.data_stream.read().decode('utf-8')
        return file_content
    except KeyError:
        raise ValueError(f"File '{file_path}' does not exist in commit {commit_sha}")

def compare_repositories(repo_list1, repo_list2):
    """Compare two lists of repositories and return the differences."""
    changes = {'repositories': []}
    # Convert list of dictionaries to a list of unique identifiers (name and refspec)
    def get_repo_identifiers(repo_list):
        return {(repo.get('name'), repo.get('refspec')): repo for repo in repo_list}
    # Convert both lists to identifiers
    repo_dict1 = get_repo_identifiers(repo_list1)
    repo_dict2 = get_repo_identifiers(repo_list2)
    # Find repositories in repo_dict2 that are not in repo_dict1
    for key, repo in repo_dict2.items():
        if key not in repo_dict1:
            changes['repositories'].append(repo)
    # Find repositories that exist in both dicts but have different contents
    for key in repo_dict1.keys():
        if key in repo_dict2 and repo_dict1[key] != repo_dict2[key]:
            changes['repositories'].append(repo_dict2[key])
    # If no changes, return an empty dictionary
    if not changes['repositories']:
        return {}
    return changes
