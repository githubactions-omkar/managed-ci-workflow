# build
This workflow, [build](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build.yaml),
depends on the [unit-test](../unit-test/README) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered
(unless otherwise stated).

Builds for Java-based repos use the [mci-build-maven.yaml](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build-maven.yaml)
workflow and the workflow includes these jobs:

* [create-tag](#create-tag)
* [set-vals](#set-vals)
* [build-app](#build-app)
* [build-automation](#build-automation)
* [coreupdate](#coreupdate)
* [jira_update](#jira_update)


## create-tag
This job runs these steps to construct the output variable `tag`:
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Construct](https://github.com/glcp/mci-actions-version-number/tree/v1) and set the
   environment variable `VERSION_NUMBER`, which is used in the step below
4. [Construct](https://github.com/glcp/mci-actions-version-tag/tree/v1/java) the output
   variable `tag`
5. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
   to the artifact named `variables-build`

## set-vals
This job runs the following steps to set output variables to be used in downstream jobs.  
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. Set output variables: 
   * `docker_target` : this output variable is set to `ci-stage` for pull requests.
      Otherwise, it is set to `prod-image` for other events
   * `docker_push` : this output variable is set to the string `false` if the MCI variable
     `SKIP_DOCKER_PUSH` is set to the string `true`.  Otherwise, the output variable is 
     set to `true` if the MCI variable `SKIP_DOCKER_PUSH` or is set to the string `false`,
     or is NOT set
4. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
   to the artifact named `variables-build`

## build-app
The build-app job is used for the app build and is **triggered only by manual runs or 
pushes to the default branch**.
1. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-build` artifact
2. [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
   from the artifact named `workspace-test` (NOT from `workspace-build`)
3. Run [Docker build and push](https://github.com/glcp/mci-actions-docker-build-push-app/tree/v1.01)

NOTE: PR builds for Java-based repos are handled in a different workflow, and that
workflow runs in parallel with this workflow.
See [Builds on PR](../../../managed-ci-workflows/pr-build/index)
for details.

## build-automation
The build-automation job is used for the automation build and is **triggered only 
by manual runs or pushes to the default branch**.
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
3. [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
   from the artifact named `workspace-build`
4. Run [Docker Automation Build](https://github.com/glcp/mci-actions-docker-build-push-automation/tree/v1.01) 
   **only if the** `./tests/feature_test/docker/Dockerfile_FT` file **exists**
5. [Login](https://github.com/glcp/mci-actions-registry-login/tree/v1) to the registry
6. Update the SBOM information in `.github/mci-variables.yaml`
   with the Product name, URL and SHA1.  This updated info will be used in
   the `sbom-upload` job in the post-build job.
7. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables

## coreupdate
The coreupdate job is used to update the channel versions in 
Coreupdate and is **triggered only by manual runs or pushes to the default branch**.
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
3. [Set](https://github.com/glcp/mci-actions-coreupdate-channel/tree/v1) the Coreupdate channel
4. [Push to Coreupdate](https://github.com/glcp/mci-actions-coreupdate/tree/v1.0) if the Coreupdate
   channel from the previous step is NOT empty.

## jira_update
This job is used to [update the jira ticket](https://github.com/glcp/mci-actions-jira-update/tree/v1.0) 
with the build tag. 
This job and is **triggered only by pushes to the default branch**.

