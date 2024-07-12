post-build
==========
This workflow, `post-build`_, depends on the `build <../build/README.html>`_ workflow,
and is common for all build systems.
This workflow includes these jobs:

* `set-matrix-variables`_
* `sbom-image`_
* `sbom-fs`_

set-matrix-variables
--------------------
This job is executed on the default branch or on the ``released``
event [``github.event.action == 'released'``]
and does the following:

1. get the variables from the ``.github/mci-variables.yaml`` file that was generated
   by the ``build`` stage
2. set matrix with ``.SBOM`` list (of ``PRODUCT_NAME`` from ``variables-build`` artifact) that is populated during build stage for languages Golang, Python, Sbt, Maven.

   Currently supported languages for sbom-image(signing and attesting image) are Golang, Python, Sbt, Maven.
3. This job searches the `vtn-config.yaml <https://github.com/glcp/managed-ci-workflow/blob/main/utils/vtn-config.yaml>`_ file to see if the app/repo was already onboarded to VTN
   and sets the output variable ``ENABLE_SBOM_UPLOAD`` to the string ``true`` if the entry is available in VTN config file
   or to the string ``false`` if the entry is not available in VTN config file.

   Example for enabled sbom upload:
.. code-block:: yaml

   Projects:
    - name: 'service-identity'
      product-name: 'token-exchange'
      product-version: '1.0.0'
      mgr-list:
        - andrew.m.pitman@hpe.com
      nonmgr-list:
        - eugene.cheverda@hpe.com

..
4. search the `vtn-config.yaml <https://github.com/glcp/managed-ci-workflow/blob/main/utils/vtn-config.yaml>`_ file to see if the app/repo was already onboarded to VTN
   and set the output variable ``ENABLE_FS_SBOM_UPLOAD`` to the string ``true`` if the entry is available in VTN config file
   or to the string ``false`` if the entry is not available in VTN config file.

   Example for enabled fs sbom upload:
.. code-block:: yaml   

   Projects:
    - name: 'onprem-test'
      product-name: 'fs'
      product-version: '1.0.0'
      mgr-list:
        - javier.albornoz@hpe.com
      nonmgr-list:
        - jason.bugallon@hpe.com

..
4. set matrix with .SBOM list (of product names from variables-build artifact) that is populated during build stage for languages Golang, Python, Sbt, Maven.

   Currently supported languages for sbom-image(signing and attesting image) are Golang, Python, Sbt, Maven.

sbom-image
-----------
This job is executed when ALL of these conditions are met:
* this workflow was triggered on the default branch or on the ``released`` event.


This job uses the `mci-actions-sbom-upload <https://github.com/glcp/mci-actions-sbom-upload/tree/v3>`_
to :
- co-sign and verify the image
- create spdx-json and attest the image with the generated sbom
- upload the SBOM to VTN only when ENABLE_SBOM_UPLOAD is true.

To enable sbom image upload, the inputs ``name``, ``product-name``, ``product-version``,
``mgr-list`` and ``nonmgr-list`` are are taken from `vtn-config.yaml`_ file.

.. code-block:: yaml

   Generic:
     - name: 'properties'
       org-name: 'GreenLake'
       api-url: 'https://vtn.hpecorp.net/api'
    
   Projects:
    - name: 'service-identity'
      product-name: 'token-exchange'
      product-version: '1.0.0'
      mgr-list:
        - andrew.m.pitman@hpe.com
      nonmgr-list:
        - eugene.cheverda@hpe.com

.. _`vtn-config.yaml`: https://github.com/glcp/managed-ci-workflow/blob/main/utils/vtn-config.yaml
.. _`post-build`: https://github.com/glcp/managed-ci-workflow/blob/main/.github/workflows/mci-post-build.yaml


sbom-fs
-----------
This job is executed when ALL of these conditions are met:
* this workflow was triggered on the default branch or on the ``released`` event


This job uses the `mci-actions-sbom-upload <https://github.com/glcp/mci-actions-sbom-upload/tree/v3>`_
to :
- Create file system sbom.
- upload the SBOM to  VTN only when ENABLE_FS_SBOM_UPLOAD is true.

To enable sbom image upload, the inputs ``name``, ``product-name``, ``product-version``,
``mgr-list`` and ``nonmgr-list`` are are taken from `vtn-config.yaml`_ file.

.. code-block:: yaml

   Generic:
     - name: 'properties'
       org-name: 'GreenLake'
       api-url: 'https://vtn.hpecorp.net/api'
    
   Projects:
    - name: 'onprem-test'
      product-name: 'fs'
      product-version: '1.0.0'
      mgr-list:
        - bharani.batna@hpe.com
      nonmgr-list:
        - akluong@hpe.com

.. _`vtn-config.yaml`: https://github.com/glcp/managed-ci-workflow/blob/main/utils/vtn-config.yaml
.. _`post-build`: https://github.com/glcp/managed-ci-workflow/blob/main/.github/workflows/mci-post-build.yaml
