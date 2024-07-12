# unit-test
This workflow, [unit-test](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-unit-test.yaml), 
depends on the [pre-test](../pre-test/jobs) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered 
(unless otherwise stated).
For Manual trigger of the managed CI on non-default branch the execution can be skipped for manual runs in non-default branch by adding variable `SKIP_CHECKS: true` in mci-variables.yaml

Java-based repos use the **maven** job in this workflow to run these steps:

1. Create a Docker container using the value of the `BUILD_CONTAINER_IMAGE` variable
   in the `.github/mci-variables.yaml` file to run the steps below    
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-test` artifact
3.   
   * [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
     from the artifact named `workspace-test` **only if the** `UNIT_TEST_WORKSPACE_BACKUP`
     **variable is set to the string** `true` in the `.github/mci-variables.yaml` file
   * If the workspace restoration was skipped, then
     [checkout](https://github.com/actions/checkout) the application repository
4. Install dependencies inside the Docker container by invoking `./install-dependencies.sh`
5. [Construct](https://github.com/glcp/mci-actions-version-number/tree/v1) and set the 
   environment variable `VERSION_NUMBER`, which is used in the step below
6. [Construct](https://github.com/glcp/mci-actions-version-tag/tree/v1/java) the 
   output variable `tag`
7. Run unit tests by invoking `./build_ut.sh` 
8. Run [SonarQube scanning](https://github.com/hpe-actions/sonarqube-scan)
9. Push artifacts to JFrog (only for manual runs on the default branch and
   if the MCI variable `SKIP_JFROG_PUSH` is NOT set to the string `true`)
10. Run OWASP Dependency checks (only for manual runs on the default branch)
11. [Save](https://github.com/actions/upload-artifact/tree/v3) the Dependency checks report 
    using the artifact name `dependency-check-report` (only for manual runs on the default 
    branch)
12. [Backup](https://github.com/glcp/mci-actions-workspace-backup/tree/v1) the workspace

