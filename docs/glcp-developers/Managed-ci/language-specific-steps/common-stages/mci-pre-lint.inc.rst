pre-lint
============
This `workflow <https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/templates/mci-pre-lint.yaml>`_
runs in parallel with the `check <../pre-check/jobs.html>`_ workflow
and the `pre-test <../pre-test/jobs.html>`_ workflow.

The application team can use this workflow to execute project-specific jobs/steps
before the ``lint`` stage that cannot be incorporated into Managed CI.

This workflow is just a boilerplate workflow with the following steps:

    - checkout the application repository
    - retrieve MCI variables
    - application project-specific steps
    - backup MCI variables
    - backup workspace

The MCI variables are retrieved from the artifact named ``variables-lint``.
The MCI variables are backed up to the artifact named ``variables-lint``.

The workspace is backed up to the artifact named ``workspace-lint``.
**The workspace is backed up only if the MCI variable ``LINT_WORKSPACE_BACKUP``
is set to the string ``true``.**

The `MCI Deployer <../../../on-boarding/mci-deployer/README.html>`_ deploys this workflow
to the ``.github/workflows`` folder of the application repository.

