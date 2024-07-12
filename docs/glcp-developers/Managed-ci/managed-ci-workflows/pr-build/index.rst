.. _mci-pr-ft_index:

======================
Managed CI Build on PR
======================

The `Managed CI Build on PR`_ workflow runs in parallel with the other
Managed CI workflows.

Builds on PR
------------

Builds on PR run when the event name is ``pull_request`` and the type is one of:
``opened``, ``reopened``, or ``synchronize``.

This workflow will run builds for

.. toctree::
   :maxdepth: 1

   ./pr-build/golang.md
   ./pr-build/maven.md
   ./pr-build/python.md

.. _`Managed CI Build on PR`: https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-pr-build.yaml

