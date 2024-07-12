Managed CI Workflow Deployer
----------------------------
In addition to hosting the reusable workflows, [glcp/managed-ci-workflow](https://github.com/glcp/managed-ci-workflow) 
offers the ability to deploy the primary and template workflows to participating repositories.   

Versioning is supported for these workflows and for the workflow file manifest.    
To create a new version for the workflows within this repository:
- Modify, commit, and push the workflow changes
- Create and push a new tag (`git tag <TAG> && git push origin <TAG>`) or a new branch
- For primary, optional, or template workflows (those distributed to remote repositories), 
  reference the tag or branch within the workflow deployment config 
  *workflow-deployments.yaml* as described below
- For reusable workflows (hosted within [glcp/managed-ci-workflow](https://github.com/glcp/managed-ci-workflow)), 
  reference the tag or branch within the primary workflow itself

**Workflow file manifest**<br>
The workflow file names are contained as lists within the `primary-workflows`, 
`optional-workflows`, and `template-workflows` sections of the 
[workflow-manifest.yaml](https://github.com/glcp/managed-ci-workflow/blob/main/workflow-manifest.yaml) 
file, as shown below:
```yaml
primary_workflows:
  - managed-ci-merge.yaml
  - managed-ci-pr.yaml
  - managed-ci-pr-build.yaml
  - managed-ci-pr-check.yaml
  - managed-ci-manual-build.yaml
  - managed-ci-pr-ft.yaml
  - managed-ci-pr-ft-check.yaml
optional_workflows:
  - managed-ci-hotfix-branch-create.yaml
template_workflows:
  - mci-pre-check.yaml
  - mci-post-check.yaml
  - mci-pre-lint.yaml
  - mci-pre-test.yaml
  - mci-custom-final.yaml
```
The contents of this file may change over time and should have an associated tag when it 
does change.  The tag can be referenced within 
[workflow-deployments.yaml](https://github.com/glcp/managed-ci-workflow/blob/main/workflow-deployment.yaml)

**Workflow Deployment configuration**<br>
As with glcp/org-policies, the configuration is intended to be modular -- but for the present 
only supports the *managed-ci-workflow* module.
The contents of the `repositories` list in the [workflow-deployments.yaml](https://github.com/glcp/managed-ci-workflow/blob/main/workflow-deployment.yaml)
file should be the only section that requires updates.


**Repositories**
The repositories list supports the keys:
- *name* - the name of the repository (within the glcp organization) to which the deployer will push workflows described within the manifest.
- *refspec* - a refspec for glcp/managed-ci-workflow (tag, branch, commit sha, etc.)
- *optional_workflows* - an optional key that contains a list of workflows (from the *optional_workflows* list within the manifest) that the participating repository would like to have installed.    These are workflows that are centrally managed but not manditory.   Functional test workflows are an example.
- *needs* - an optional key that gives the repo access to options secrets ,if you are using ft on PR workflows add needs needs key with ft-secrets as variable to add repo to the optional secrets which are required for workflow


```yaml
modules:
  - name: managed-ci-workflow
    description: Managed CI Workflow
    repositories:
      - name: rmcnamara-managed-ci-workflow-test
        refspec: tags/v1.0.0
      - name: rmcnamara-firmware-registry
        refspec: tags/v1.0.0
      - name: managed-ci-workflow-test-python
        refspec: main
        optional_workflows:
          - managed-ci-pr-ft.yaml
        needs:
          - ft-secrets
```     
To [onboard to MCI](../index), add your repo to the [workflow-deployment.yaml](https://github.com/glcp/managed-ci-workflow/blob/main/workflow-deployment.yaml) 
with the repo name and the refspec. 

