# lint
This workflow, [lint](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-lint.yaml),
depends on the [pre-lint](../pre-lint/jobs) workflow.
All jobs and steps in this workflow are configured to run on these 
events (unless otherwise stated):
* manual runs [`github.event_name == 'workflow_dispatch'`]
   **the execution can be skipped for manual runs in non-default branch by adding variable `SKIP_CHECKS: true` in mci-variables.yaml**
* pull requests  [`github.event_name == 'pull_request'`]

Shell-based repos use the **shell** job in this workflow to run these steps:

1. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-lint` artifact
2.
    * [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
      from the artifact named `workspace-lint` **only if the** `LINT_WORKSPACE_BACKUP`
      **variable is set to the string** `true` in the `.github/mci-variables.yaml` file
      **Regex can be provided to exclude linting for specific folder using mci variable `LINT_REGEX_EXCLUDE` in `.github/mci-variables.yaml`**
    * If the workspace restoration was skipped, then
      [checkout](https://github.com/actions/checkout) the application repository
3. Run [linting](https://github.com/glcp/super-linter/tree/v5/slim)
   **Only new or edited files will be parsed for validation.**
4. Run [Lint-checklines](https://github.com/glcp/mci-actions-linter-checklines) this will compare lint output with git diff, if it find any lint errors on new code it will break the workflow
5. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
   to the artifact named `variables-lint`
6. [Backup](https://github.com/glcp/mci-actions-workspace-backup/tree/v1) the workspace to the
   artifact named `workspace-lint` **only if the** `LINT_WORKSPACE_BACKUP`
   **variable is set to the string** `true` in the `.github/mci-variables.yaml` file

