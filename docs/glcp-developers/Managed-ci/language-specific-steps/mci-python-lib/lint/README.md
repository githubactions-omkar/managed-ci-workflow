# lint
This workflow, [lint](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-lint.yaml),
depends on the [pre-lint](../pre-lint/jobs) workflow.
All jobs and steps in this workflow are configured to run on these 
events (unless otherwise stated):
* manual runs [`github.event_name == 'workflow_dispatch'`]
   **the execution can be skipped for manual runs in non-default branch by adding variable `SKIP_CHECKS: true` in mci-variables.yaml**
* pull requests  [`github.event_name == 'pull_request'`]

Repos for Python libs use the **python-lib** job in this workflow to run these steps:

1. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-lint` artifact
2.
   * [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
     from the artifact named `workspace-lint` **only if the** `LINT_WORKSPACE_BACKUP`
     **variable is set to the string** `true` in the `.github/mci-variables.yaml` file
   * If the workspace restoration was skipped, then
     [checkout](https://github.com/actions/checkout) the application repository
3. [Login](https://github.com/glcp/mci-actions-registry-login/tree/v2) to the registry
4. 
   * Run the local dev-env bootstrap by invoking the `./automation/ci/bootstrap_dev_env.sh`
      only if the MCI variable `DEV_ENV_LOCAL` is set to the string `true`
   * Otherwise, [BootStrap](https://github.com/glcp/mci-actions-bootstrap-dev-env/tree/v1.0) Dev Env
5. Run linting by invoking `poetry run scripts/lint.sh`
6. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
   to the artifact named `variables-lint`
7. [Backup](https://github.com/glcp/mci-actions-workspace-backup/tree/v1) the workspace to the
   artifact named `workspace-lint` **only if the** `LINT_WORKSPACE_BACKUP`
   **variable is set to the string** `true` in the `.github/mci-variables.yaml` file

