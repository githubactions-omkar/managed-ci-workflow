# build
This workflow, [build](https://github.com/glcp/managed-ci-workflow/tree/main/.github/workflows/mci-build.yaml),
depends on the [unit-test](../unit-test/README) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered
(unless otherwise stated).

Builds for Javascript-image-based repos use the [mci-build-javascript-image.yaml](https://github.com/glcp/managed-ci-workflow/tree/main/.github/workflows/mci-build-javascript-image.yaml)
workflow and the workflow includes these jobs:

* [create-tag](#create-tag)
* [docker-build](#docker-build)
* [set-artifact-urls](#set-artifact-urls)
* [jira_update](#jira_update)


## create-tag
This job runs these steps to construct the output variable `tag`:
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Construct](https://github.com/glcp/mci-actions-version-number/tree/v1) and set the
   environment variable `VERSION_NUMBER`, which is used in the step below
4. Set output variable `tag`, based on these conditions
   ```text
   assign default value: MAJOR="2"
   assign default value: MINOR="0"
   if MCI variable VERSION_MAJOR is not empty, then set MAJOR=VERSION_MAJOR
   if MCI variable VERSION_MINOR is not empty, then set MINOR=VERSION_MINOR
   
   if this workflow was triggered by the "push" event to the default branch, then
      1. set output variable tag=MAJOR.VERSION_NUMBER.MINOR
      2. tag the files in the workspace using the value of the output variable
      3. push the tag
   else if GitHub event action is "released", then     
     set output variable tag=MAJOR.github_run_number.MINOR
   else
     set output variable tag=MAJOR.VERSION_NUMBER.MINOR-dev
   endif
   ```
5. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
   to the artifact named `variables-build`


## docker-build
This job is triggered only for manual runs, pushes, and releases.
This job runs only if the PRODUCTS matrix is set.
The following steps are run in parallel for each product found in 
the `PRODUCTS` MCI variable:
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Login](https://github.com/glcp/mci-actions-registry-login/tree/v2) to the registry
3. Run [Docker build and push](https://github.com/glcp/mci-actions-docker-build-push/tree/v1)

## set-artifact-urls
This job is triggered only for manual runs, pushes, and releases.
This job runs only if the PRODUCTS matrix is set.
This job updates the SBOM information in `.github/mci-variables.yaml`
with the Product name, URL and SHA1.  This updated info will be used in
the `sbom-upload` job in the post-build job.
The MCI variables are then [backed up](https://github.com/glcp/mci-actions-variables-backup/tree/v2)
to the artifact named `variables-build`

## jira_update
This job is used to [update the jira ticket](https://github.com/glcp/mci-actions-jira-update/tree/v1.0) 
with the build tag. 
This job and is **triggered only by pushes to the default branch**.

