# unit-test
This workflow, [unit-test](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-unit-test.yaml), 
depends on the [pre-test](../pre-test/jobs) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered 
(unless otherwise stated).
For Manual trigger of the managed CI on non-default branch the execution can be skipped for manual runs in non-default branch by adding variable `SKIP_CHECKS: true` in mci-variables.yaml

Python-based repos use the **python** job in this workflow to run these steps:

1. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-test` artifact
2.
   * [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
     from the artifact named `workspace-test` **only if the** `UNIT_TEST_WORKSPACE_BACKUP`
     **variable is set to the string** `true` in the `.github/mci-variables.yaml` file
   * If the workspace restoration was skipped, then
     [checkout](https://github.com/actions/checkout) the application repository
3. [Login](https://github.com/glcp/mci-actions-registry-login/tree/v2) to the registry
4. [Checkout](https://github.com/actions/checkout) the 
   [pingfederate](https://github.com/glcp/pingfederate) repo
5. 
   * Run the local dev-env bootstrap by invoking the `./automation/ci/bootstrap_dev_env.sh`
     only if the MCI variable `DEV_ENV_LOCAL` is set to the string `true`
   * Otherwise, [BootStrap](https://github.com/glcp/mci-actions-bootstrap-dev-env/tree/v1.0) Dev Env
6. Locate the unit test script
7. Run unit tests by invoking `poetry run scripts/<script-name>` 
   (where `<script-name>` is either `unittest.sh` or `test.sh` from the previous step)
8. Override source path in `coverage.xml` for Sonar scanning
9. Run [SonarQube scanning](https://github.com/hpe-actions/sonarqube-scan)
10. Show contents of SonarQube report file
11. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
    to the artifact named `variables-test`
12. [Backup](https://github.com/glcp/mci-actions-workspace-backup/tree/v1) the workspace to the
    artifact named `workspace-test` **only if the** `UNIT_TEST_WORKSPACE_BACKUP`
    **variable is set to the string** `true` in the `.github/mci-variables.yaml` file

