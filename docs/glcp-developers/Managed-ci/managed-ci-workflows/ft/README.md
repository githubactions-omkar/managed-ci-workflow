# Enabling FT on PR

FT on PR is currently applicable for Python, Go, and Maven repositories. 
After the top-level workflow determines that FT should be run, it is launched with 
the [mci-deploy-and-test.yaml](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-deploy-and-test.yaml)
workflow.
There are several dependencies within the workflow which make it suitable only 
for CCS at the moment, including (but not limited to):

* CCS-specific spinnaker jobs
* CCS-specific s3 buckets

## Dockerfile location

To enable FT on PR , ensure that one of these conditions is met:
* A feature-test Dockerfile exists at `tests/feature_test/docker/Dockerfile_FT`.
* A feature-test Dockerfile exists elsewhere within the service repository
* A feature-test Dockerfile exists *within a different repository*

When using a remote test repository (the last case above), the name and refspec of the feature test repository must be provided with `FT_REPOSITORY` in `mci-variables.yaml` (e.g. `FT_REPOSITORY: glcp/my-test-repo@my-refspec`).

If using a `PRODUCTS` list within `mci-variables.yaml`, ensure than a `BUILD_TYPE: automation` object exists within the list.  Within that object:

* Include a `DOCKERFILE_PATH` variable.   This is the full path and filename of the FT Dockerfile on either the local service repository or the remote test repository.
* Include a `FT_REPOSITORY` variable as described above if using a remote test repository.

If ***not*** using a `PRODUCTS` list:

* Include a `FT_DOCKERFILE_PATH` variable.   This is the full path and filename of the FT Dockerfile on either the local service repository or the remote test repository.
* Include a `FT_REPOSITORY` variable as described above if using a remote test repository.

An example of the final configuration method might look like:

```yaml
PRODUCTS:
- BUILD_TYPE: automation
  DOCKERFILE_PATH: docker/Dockerfile
  FT_REPOSITORY: glcp/auto-unified-api@main
  (etc.)
- BUILD_TYPE: app
  DOCKERFILE_PATH: ./build/docker/unified-routing/Dockerfile
  IMAGE_REGISTRY: quay.io/ccsportal/unified-api-routing
  (etc.)
```

If not using a `PRODUCTS` list, the equivalent automation variables might look like:

```yaml
FT_DOCKERFILE_PATH: docker/Dockerfile
FT_REPOSITORY: glcp/auto-unified-api@main
```

(please note the use of the `FT_` prefix for the Dockerfile path in this case!)

## Deploy manifest location

Kubernetes manifests will be deployed to core from the `deploy` directory by default, but this can be overridden to point to a different repository.  To use this feature, add the variables below to `mci-variables.yaml` at the global level.

* `FT_DEPLOY_REPOSITORY` - repository name and refspec (e.g. `glcp/my-deploy-repo@my-refspec`)
* `FT_DEPLOY_REPOSITORY_PATH` - k8s manifest file folder within the remote repository (e.g. `deploy`)

## Conditions for FT on PR

FT on PR runs when ALL of these conditions are met:

1. One of these is true:
   * The event name is ``pull_request`` and the type is ``labeled``
   * The event name is ``pull_request_review`` and the type is ``submitted``
2. The dockerfile exists (as described above)
3. One of these is true:
   * The pull requests has exactly 2 approvals submitted.
   * FT on PR label `trigger_ft_on_pr_workflow` exists on the pull request  
      (Label should be created in your repo and applied to PR as shown in below screenshot)
4. `GLCP_BUILD_SYSTEM` specifies a build system that is supported by FT
5.  By default FT is run(enabled) on dependabot PRs.
   `FT_DISABLE_DEPENDABOT` set this variable to true in mci variables to disable FT run on dependabot PRs.

***Note***: The workflow will be triggered by the creation of ***any*** PR label but test execution will only occur in the presence of the `trigger_ft_on_pr_workflow` label.  If FT has previously passed for a commit, a `ft_passed_<SHORTSHA>` label on the PR will permit the workflow to short-circuit and register a `PASS` result.

 ![FTPRlabel](../../../../../../assets/FTPRlabel.png)

Processing of these conditions is split into two top level workflows:

* `managed-ci-pr-ft-check.yaml` - Checks for exactly 2 PR approvals and labels the PR with `trigger_ft_on_pr_workflow` if they are found.
* `managed-ci-pr-ft.yaml` - The heart of FT.  Triggered by the creation of any label.   As described above, only `trigger_ft_on_pr_workflow` will permit the FT execution.
