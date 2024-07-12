# build
This workflow, [build](https://github.com/glcp/managed-ci-workflow/tree/main/.github/workflows/mci-build.yaml),
depends on the [unit-test](../unit-test/README) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered
(unless otherwise stated).

Builds for Javascript-based repos use the [mci-build-javascript.yaml](https://github.com/glcp/managed-ci-workflow/tree/main/.github/workflows/mci-build-javascript.yaml)
workflow and the workflow includes these jobs:

* [create-tag](#create-tag)
* [build-javascript](#build-javascript)
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


## build-javascript
The build-javascript job is used for the javascript build and is **triggered only by manual runs or 
pushes to the default branch**.
1. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-build` artifact
2. [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
   from the artifact named `workspace-test` (NOT from `workspace-build`)
3. Set default values for Javascript specifics if not provided in mci-variables.
   ```text
          if [[ -z "${{ env.JS_BUILD_SCRIPT }}" ]]; then 
            echo "JS_BUILD_SCRIPT=build" >> $GITHUB_ENV
          fi
          if [[ -z "${{ env.JS_BUILD_PATH }}" ]]; then 
            echo "JS_BUILD_PATH=dist" >> $GITHUB_ENV
          fi
          if [[ -z "${{ env.JS_WORKING_DIR }}" ]]; then 
            echo "JS_WORKING_DIR=./" >> $GITHUB_ENV
          fi
          if [[ -z "${{ env.JS_PACKAGE_MANAGER }}" ]]; then 
            echo "JS_PACKAGE_MANAGER=pnpm" >> $GITHUB_ENV
          fi
          if [[ -z "${{ env.JS_CACHE_VERSION }}" ]]; then 
            echo "JS_CACHE_VERSION=v1" >> $GITHUB_ENV
          fi
          if [[ -z "${{ env.JS_NODE_VERSION }}" ]]; then 
            echo "JS_NODE_VERSION=16" >> $GITHUB_ENV
          fi
          if [[ -z "${{ env.JS_PNPM_VERSION }}" ]]; then 
            echo "JS_PNPM_VERSION=7" >> $GITHUB_ENV
          fi
          if [[ -z "${{ env.JS_PNPM_RECURSIVE }}" ]]; then 
            echo "JS_PNPM_RECURSIVE=true" >> $GITHUB_ENV
          fi
   ``` 
3. Run [javascript build ](https://github.com/glcp/mfe-workflows/.github/actions/build@v1)

NOTE: PR builds for Javascript-based repos are handled in a different workflow, and that
workflow runs in parallel with this workflow.
See [Builds on PR](../../../managed-ci-workflows/pr-build/index)
for details.

## jira_update
This job is used to [update the jira ticket](https://github.com/glcp/mci-actions-jira-update/tree/v1.0) 
with the build tag. 
This job and is **triggered only by pushes to the default branch**.

