===============================
 GHpages clean up
===============================


we run a workflow every day for cleaning up the GHpages branch for all repositories onboarded to MCI. To implement this, please add a .ghpagesretention file to the root directory with the retention days specified.

Sample .ghpagesretention file:

``
RETENTION_DAYS: 30

``

This workflow runs every day, checks the RETENTION_DAYS in the .ghpagesretention file, and deletes all directories older than the specified RETENTION_DAYS.  

.. note::

   If there is no ``.ghpagesretention`` file or no ``RETENTION_DAYS`` in the ``.ghpagesretention`` file, we skip the repository without taking any action.

