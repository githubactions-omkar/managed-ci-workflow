custom-final
============
This `workflow <https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/templates/mci-custom-final.yaml>`_
runs after the `post-build <../post-build/jobs.html>`_ workflow.

The application team can use this workflow to execute project-specific jobs/steps
after the ``post-build`` stage that cannot be incorporated into Managed CI.

This workflow is just a boilerplate workflow with the following steps:

    - retrieve MCI variables that were saved during the `build <../build/README.html>`_ stage
    - application project-specific steps
    - backup MCI variables

The MCI variables are retrieved from the artifact named ``variables-build``.
The MCI variables are backed up to the artifact named ``variables-custom-final``.

The `MCI Deployer <../../../on-boarding/mci-deployer/README.html>`_ deploys this workflow
to the ``.github/workflows`` folder of the application repository.

