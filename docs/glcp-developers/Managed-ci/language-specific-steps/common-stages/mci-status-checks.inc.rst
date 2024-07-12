status-checks
=============
This `workflow <https://github.com/glcp/managed-ci-workflow/tree/main/templates/mci-pr-status.yaml>`_
runs only after the completion of the `check <../pre-check/jobs.html>`_ workflow, `lint <../lint/README.html>`_
and the `unit-test <../unit-test/README.html>`_ workflows.

The workflow will be used only in Managed CI on PR. This workflow is used to 
consolidate the status of all the mandatory jobs needs on PR and make sure the PR is blocked if any them failed.

This workflow includes these jobs:

* `status-check`_
* `comment-pt`_

status-check
--------------------
This job is executed on the event [``github.event.action == 'released'``]
and does the following:

1. checks the status of all the mandatory jobs and exit if any failures

comment-pt
-----------
This job is executed on all pull_request actions :

* comments the status of all the jobs in PR


 .. image:: /assets/status-checks.png
