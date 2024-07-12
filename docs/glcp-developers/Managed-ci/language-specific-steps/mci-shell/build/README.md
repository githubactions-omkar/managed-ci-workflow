# build
This workflow, [build](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build.yaml),
depends on the [unit-test](../unit-test/README) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered
(unless otherwise stated).

Builds for Shell-based repos use the [mci-build-script.yaml](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build-script.yaml)
workflow and the workflow includes these steps:

1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
3. Set output variable `tag`, based on one of these conditions
   ```text
   if this workflow was triggered by the "push" event to the default branch, then
      1. set output variable tag=VERSION.github_run_number
      2. tag the files in the workspace using the value of the output variable
      3. push the tag
   else
     set output variable tag=VERSION.github_run_number-dev
   fi 
   ```
   where `VERSION` is an MCI variable
4. [Login](https://github.com/glcp/mci-actions-registry-login/tree/v1) to the registry
5. Run build script specified in the MCI variable `SCRIPT_TO_RUN`

