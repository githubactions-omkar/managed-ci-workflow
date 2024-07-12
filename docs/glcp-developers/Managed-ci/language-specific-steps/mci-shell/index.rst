.. _mci-shell_index:
.. _mci-shell_stages_index:

===============================
 Managed CI - Shell
===============================

For shell-based repos, set the `repo variable <../../on-boarding/index.html#repository-variables>`_
``GLCP_BUILD_SYSTEM`` to ``shell``.

Triggers
--------

See `details <../../managed-ci-workflows/triggers/README.html>`_.

Stages
------

**There are 8 stages in this workflow**

.. toctree::
   :maxdepth: 1

   pre-check/jobs.rst
   pre-lint/jobs.rst
   lint/README.md
   pre-test/jobs.rst
   unit-test/README.md
   build/README.md
   post-build/jobs.rst
   custom-final/jobs.rst
   status-checks/jobs.rst

MCI variables
-------------

| The MCI variables are used throughout the stages.
| See `description <../../on-boarding/variables/shell-variables/README.html#variables-for-shell-system>`_ of the variables.


