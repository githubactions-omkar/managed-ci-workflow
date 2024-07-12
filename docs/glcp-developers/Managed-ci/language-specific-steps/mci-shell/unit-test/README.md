# unit-test
This workflow, [unit-test](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-unit-test.yaml), 
depends on the [pre-test](../pre-test/jobs) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered 
(unless otherwise stated).
For Manual trigger of the managed CI on non-default branch the execution can be skipped for manual runs in non-default branch by adding variable `SKIP_CHECKS: true` in mci-variables.yaml

Shell-based repos use the **shell** job in this workflow to run these steps:

1. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-test` artifact
2.
    * [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
      from the artifact named `workspace-test` **only if the** `UNIT_TEST_WORKSPACE_BACKUP`
      **variable is set to the string** `true` in the `.github/mci-variables.yaml` file
    * If the workspace restoration was skipped, then
      [checkout](https://github.com/actions/checkout) the application repository
3. Run unit tests by invoking `make test`
4. Run [SonarQube scanning](https://github.com/hpe-actions/sonarqube-scan)
5. [Backup](https://github.com/glcp/mci-actions-workspace-backup/tree/v1) the workspace to the
   artifact named `workspace-test` **only if the** `UNIT_TEST_WORKSPACE_BACKUP`
   **variable is set to the string** `true` in the `.github/mci-variables.yaml` file

