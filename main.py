import os
import sys
import yaml
import json
import importlib.util
managed_ci_repo = f'{os.path.dirname(__file__)}/../tarun-repo-config/'
print(managed_ci_repo)
import os
dirname = os.path.dirname(__file__)
print(f'dirname {dirname}')
filename = os.path.join(dirname, '../../tarun-repo-config/')
print(f'filename {filename}')

from pathlib import Path

# `cwd`: current directory is straightforward
cwd = Path.cwd()

# `mod_path`: According to the accepted answer and combine with future power
# if we are in the `helper_script.py`
mod_path = Path(__file__).parent
# OR if we are `import helper_script`


# `src_path`: with the future power, it's just so straightforward
relative_path_1 = '../tarun-repo-config'

src_path_1 = (mod_path / relative_path_1).resolve()
print(f' src_path_1 {src_path_1}')


def main():
    if not 'GITHUB_APP_TOKEN' in os.environ:
        print(f'ERROR: Env var "GITHUB_APP_TOKEN" must to be set.')
        sys.exit(1)
    
    filename=f'{src_path_1}/configs/workflow-deployment.yaml'
    with open(filename, "r") as yaml_file:
        data = yaml.safe_load(yaml_file)
    modules=data['modules']
    print(f'workflow deployment config:\n{yaml.dump(modules, default_flow_style=False)}')

    for i in modules:
        module_name=i.get('name')
        module_description=i.get('description')
        repositories=i.get('repositories', [])
        module=import_module(module_name)
        module.main(module_name=module_name,
                    module_description=module_description,
                    repositories=repositories)

#This function will load the  specified module dynamically from productModules folder.
def import_module(the_module_name):
    module_dir = 'modules'
    spec = importlib.util.spec_from_file_location(
              the_module_name, 
              f'''managed-ci-workflow/{module_dir}/{the_module_name}.py''')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


main()
