# unit-test
This workflow, [unit-test](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-unit-test.yaml), 
depends on the [pre-test](../pre-test/jobs) workflow.
All jobs and steps in this workflow are configured to run on these 
events (unless otherwise stated):
* manual runs [`github.event_name == 'workflow_dispatch'`] on non-default branches
   **For Manual trigger of the managed CI on non-default branch the execution can be skipped for manual runs in non-default branch by adding variable `SKIP_CHECKS: true` in mci-variables.yaml**
* pull requests  [`github.event_name == 'pull_request'`]

Scala-based repos use the **sbt** job in this workflow to run these steps:

1. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-test` artifact
2. 
   * [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
     from the artifact named `workspace-test` **only if the** `UNIT_TEST_WORKSPACE_BACKUP`
     **variable is set to the string** `true` in the `.github/mci-variables.yaml` file
   * If the workspace restoration was skipped, then
     [checkout](https://github.com/actions/checkout) the application repository
3. [Set up](https://github.com/actions/setup-java/tree/v1) the JDK using the MCI variables
    `JAVA_VERSION` and `DISTRIBUTION`
4. [Set up](https://github.com/glcp/harmony-actions-artifactory-credentials)
   artifactory credentials
5. Copy Credentials to appropriate locations
6. [Login](https://github.com/glcp/mci-actions-registry-login/tree/v2) to the registry
7. Run `sbt verify`
8. Override source path in `coverage.xml` for Sonar scanning
9. Run [SonarQube scanning](https://github.com/hpe-actions/sonarqube-scan)
10. Show contents of SonarQube report file
11. [Backup](https://github.com/glcp/mci-actions-workspace-backup/tree/v1) the workspace to the
    artifact named `workspace-test` **only if the** `UNIT_TEST_WORKSPACE_BACKUP`
    **variable is set to the string** `true` in the `.github/mci-variables.yaml` file

