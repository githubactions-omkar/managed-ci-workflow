# build
This workflow, [build](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build.yaml),
depends on the [unit-test](../unit-test/README) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered
(unless otherwise stated).

Repos for Python lib builds use the [mci-build-python-lib.yaml](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build-python-lib.yaml)
workflow and the workflow includes these jobs:

* [create-tag](#create-tag)
* [build-publish](#build-publish)

## create-tag 
This job runs these steps to construct the output variable `tag`:
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Construct](https://github.com/glcp/mci-actions-version-number/tree/v1) and set the
   environment variable `VERSION_NUMBER`, which is used in the step below
4. Set output variable `tag`, based on these conditions
   ```text
   if the MCI variable VERSION is empty, 
      set TAG_VERSION='2.0'
   else
      set TAG_VERSION=VERSION
   set tag=TAG_VERSION.VERSION_NUMBER
   tag the files in the workspace
   push the tags
   ```
4. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
   to the artifact named `variables-build`

## build-publish

1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Build and publish](https://github.com/glcp/mci-actions-build/lib-build/tree/v1) only when running
   on the default branch


