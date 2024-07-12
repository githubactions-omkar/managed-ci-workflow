# build
This workflow, [build](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build.yaml),
depends on the [unit-test](../unit-test/README) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered
(unless otherwise stated).

Builds for Go-based repos use the [mci-build-go.yaml](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build-go.yaml)
workflow and the workflow includes these jobs:

* [create-tag](#create-tag)
* [set-matrix-variables](#set-matrix-variables)
* [docker-build](#docker-build)
* [sbom-variables](#sbom-variables)
* [coreupdate_job](#coreupdate_job)
* [jira_update](#jira_update)


## create-tag
This job runs the following steps to construct the output variable `tag` (in the last step)
to be used in downstream jobs.
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Construct](https://github.com/glcp/mci-actions-version-number/tree/v1) and set the 
   environment variable `VERSION_NUMBER`, which is used in the step below
4. Set output variable `custom_tag` to one of these values:
   * `<GitHub-tag-name>` if the `<GitHub-tag-name>` triggered the workflow 
   * `$VERSION.$VERSION_NUMBER-dev` if workflow NOT triggered by the GitHub tag;
     `$VERSION` comes from the MCI variables and `VERSION_NUMBER` comes from the step above
5. Set output variable `new_tag` with value `$VERSION.$VERSION_NUMBER`.  This tag is pushed
   if this workflow was triggered by `push` event to the default branch and the MCI 
   variable `CUSTOM_TAG` is NOT set to the string `true`
6. Set output variable `hotfix_tag` with value `$VERSION.$GITHUB_RUN_NUMBER` if current branch
   is a hotfix branch
7. Set output variable `tag`, based on one of these conditions
   ```text
   if custom_tag is not empty, then
     set tag=custom_tag
   else if new_tag is not empty, then
     set tag=new_tag
   else if hotfix_tag is not empty, then 
     set tag=hotfix_tag
   else
     echo "NO TAG EXISTS"
   ```
7. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
   to the artifact named `variables-build`

## set-matrix-variables
This job in only triggered if the output variable `tag` is NOT empty.
This job creates a JSON object for the matrix strategy from the `PRODUCTS` MCI variable.
This JSON object is used by the [docker-build](#docker-build) job.

## docker-build
This job is used for the app build and is **triggered only by manual run or push**.
The following steps are run for each product found in  the `PRODUCTS` MCI variable:
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Login](https://github.com/glcp/mci-actions-registry-login/tree/v2) to the registry
3. Run [Docker build and push](https://github.com/glcp/mci-actions-docker-build-push-app/tree/v1.01)

NOTE: PR builds for Go-based repos are handled in a different workflow, and that
workflow runs in parallel with this workflow.
See [Builds on PR](../../../managed-ci-workflows/pr-build/index)
for details.

## sbom-variables
This job updates the SBOM information in `.github/mci-variables.yaml`
with the Product name, URL and SHA1.  This updated info will be used in 
the `sbom-upload` job in the post-build job.
The MCI variables are then [backed up](https://github.com/glcp/mci-actions-variables-backup/tree/v2)
to the artifact named `variables-build`

## coreupdate
The coreupdate job is used to update the channel versions in Coreupdate. 
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
3. Set the Coreupdate output variable `channel`
4. [Push to Coreupdate](https://github.com/glcp/mci-actions-coreupdate/tree/v1.0) if the
   MCI variable `SKIP_COREUPDATE_PUSH` is NOT set to the string `true`.

## jira_update
This job is used to [update the jira ticket](https://github.com/glcp/mci-actions-jira-update/tree/v1.0)
with the build tag.
This job and is **triggered only by pushes to the default branch**.


NOTE: If the output variable `tag` is empty, then all downstream jobs after 
[create-tag](#create-tag) will be skipped.

