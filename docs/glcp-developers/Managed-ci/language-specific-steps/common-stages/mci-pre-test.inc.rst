pre-test
============
This `workflow <https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/templates/mci-pre-test.yaml>`_
runs in parallel with the `check <../pre-check/jobs.html>`_ workflow
and the `pre-lint <../pre-lint/jobs.html>`_ workflow.

The application team can use this workflow to execute project-specific jobs/steps
before the ``unit-test`` stage that cannot be incorporated into Maneged CI.

This workflow is just a boilerplate workflow with the following steps:

    - checkout the application repository
    - retrieve MCI variables
    - application project-specific steps
    - backup MCI variables
    - backup workspace

The MCI variables are retrieved from the artifact named ``variables-test``.
The MCI variables are backed up to the artifact named ``variables-test``.

The workspace is backed up to the artifact named ``workspace-test``.
**The workspace is backed up only if the MCI variable ``UNIT_TEST_WORKSPACE_BACKUP``
is set to the string ``true``.**

The `MCI Deployer <../../../on-boarding/mci-deployer/README.html>`_ deploys this workflow
to the ``.github/workflows`` folder of the application repository.

