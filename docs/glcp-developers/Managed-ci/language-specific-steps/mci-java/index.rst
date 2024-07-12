.. _mci-java_index:
.. _mci-java_stages_index:

===============================
 Managed CI - Java
===============================

For Java-based repos, set the `repo variable <../../on-boarding/index.html#repository-variables>`_
``GLCP_BUILD_SYSTEM`` to ``maven``.

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
| See `description <../../on-boarding/variables/maven-variables/README.html#variables-for-maven-system>`_ of the variables.

