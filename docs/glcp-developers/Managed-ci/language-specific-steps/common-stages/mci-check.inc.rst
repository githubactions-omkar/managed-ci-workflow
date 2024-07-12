check
======
This `workflow <https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-check.yaml>`_
runs the following jobs only on **pull requests**.
If any job fails, the entire workflow is aborted and any remaining jobs will be skipped.

* `copyright-check`_
* `secret-scanner`_
* `malware-scanner`_
* `pr-validation-check`_
* `pr-validation`_

copyright-check
---------------
This job checks for Hpe copyrights on the source files.

**This job will be executed on Pull Request and, when the workflow is triggered from non-default branch(the execution can be skipped in non-default 
branch by adding variable `SKIP_CHECKS: true` in mci-variables.yaml).**

**It will throw errors on any missing/outdated Copyrights. The user has to fix the copyrights 
and resubmit the pull request**

**This job will NOT run on the default branch.**


The workflow used for the execution of ``copyright-check`` is `copyright.yml`_.

Ignoring Copyright on Specified Files
=====================================

To ignore copyright on specific files, follow these steps:

1. Create a `.copyrightignore` file at the root of your repository.
2. Specify the paths of any files that need to have the copyright check ignored inside `.copyrightignore`.

For example:

.. code-block:: shell

    *.md
    myfile
    src/target/dist

This will ignore copyright checks on files matching the specified patterns (e.g., `*.md`, `myfile`, `src/target/dist`).


secret-scanner
--------------
This job scans for the unencrypted/plain-text secrets/passwords in the latest commit
and reports them to the code-owner.
**This job will be executed on Pull Request and, when the workflow is triggered from non-default branch(the execution can be skipped in non-default 
branch by adding variable `SKIP_CHECKS: true` in mci-variables.yaml)**
**This job will NOT run on the default branch.**

The workflow used for the execution of ``secret-scanner`` is `scanning-workflow.yml`_.

malware-scanner
---------------
This job scans for any malware in the repo and reports the malware in the comments of the PR.
If any malware is found, the workflow will fail.  The scan summary is added to the
comments of the PR, irrespective of the result of the scan.

The workflow used for the execution of ``malware-scanner`` is
`mci-clamav.yml`_.  There is no variable or parameter needed for this worklow.

pr-validation-check
-------------------
This job reads the ``.github/mci-variables.yaml`` file and gets the value of the
MCI variable ``PR_VALIDATION``.  It then sets the output variable ``pr_validation`` with
the value of ``PR_VALIDATION`` variable (string ``true`` or ``false``).
The MCI variable ``PR_VALIDATION`` is optional and by default this variable is set to ``true``, application team should set the string to
``false`` only if your team don't requires PR validation.

pr-validation
-------------
This job runs by default on all the PR's unless the output variable ``pr_validation`` from the
`pr-validation-check`_ job is ``false``.  This job scans the PR title and extracts
the Jira issue ID from the beginning of the title.  The issue ID must match either
``CCS-*`` or ``GLCP-*``. This job will fail if the issue ID does NOT exist in Jira.

The action used for the execution of ``pr-validation`` is
`mci-actions-pr-title-validation`_.  See `README`_ for the required parameters.

.. _`copyright.yml`: https://github.com/hpe-actions/copyright/blob/main/.github/workflows/copyright.yml
.. _`scanning-workflow.yml`: https://github.com/glcp/Secret-Scan-Tool/blob/main/.github/workflows/scanning-workflow.yml
.. _`mci-clamav.yml`: https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-clamav.yml
.. _`mci-actions-pr-title-validation`: https://github.com/glcp/mci-actions-pr-title-validation/tree/v1.0
.. _`README`: https://github.com/glcp/mci-actions-pr-title-validation/tree/v1.0

