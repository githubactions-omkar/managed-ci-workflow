.. _Installation_index:


===============================
Onboarding to Managed CI
===============================

**Steps to installing ManageCI workflow:**

1. Create variables from `Additional Variables`_ in .github/mci-variables.yaml
2. Disable current build process or workflows that are triggered by PRs or pushes to 
   main/mainline branch. They would be redundant.
3. Create a fork of glcp/managed-ci-workflow and add a project repository name to the 
   `deployment configuration file <https://github.com/glcp/managed-ci-workflow/blob/main/workflow-deployment.yaml>`_ 
   along with the desired glcp/managed-ci-workflow refspec for glcp/managed-ci-workflow 
   and an *optional_workflows* section if necessary.  See the 
   `Managed CI Workflow Deployer`_ for details.  Open a PR for this fork.  When merged, 
   your project repository will receive all of the workflows specified within the 
   `workflow manifest <https://github.com/glcp/managed-ci-workflow/blob/main/workflow-manifest.yaml>`_ 
   file.  Both the primary and template workflows will be copied to under project 
   repo **.github/workflows** folder.
4. If needed, customize the template workflows once they have been deployed to the
   project repository.


GLCP_BUILD_SYSTEM
====================
Name the variable ``GLCP_BUILD_SYSTEM`` in `.github/mci-variables.yaml` and give it one of the following values.   
This will be the predominant build system for your project:

* ``golang`` for Go-based repos
* ``golang-lib`` for Go-based repos containing libraries
* ``maven`` for Java-based repos
* ``python`` for Python-based repos
* ``python-lib`` for Python-based repos containing libaries
* ``sbt`` for Scala-based repos
* ``shell`` for Shell-based repos
* ``terraform`` for Terraform-based repos
* ``javascript`` for Javascript-based repos
* ``javascript-image`` for Javascript-based repos containing dockerimages
* ``onprem`` for onprem ova based repos

Enabling SBOM Upload
====================
1. Sbom can be generated for images and filesystem.
   In case of images follow the next steps 2 & 3 . In case of filesystem follow step 4.

2. Takes inputs from set matrix with ``.SBOM`` list (of ``PRODUCT_NAME`` from ``variables-build`` artifact) that is populated during build stage for languages Golang, Python, Sbt, Maven.
   
   Currently supported languages for sbom-image(signing and attesting image) are ``Golang, Python, Sbt, Maven``. 
   
   Also By default for these languages generated docker images are signed and attested with the generated sboms.
   In addition to this to upload the sbom to VTN follow the below steps.

3. To enable sbom upload to VTN for the docker images generated in the build phase, Add these entries to `vtn-config.yaml <https://github.com/glcp/managed-ci-workflow/blob/main/utils/vtn-config.yaml>`_ file.

   Note: 

   The ``name`` refers to  repository name.

   The ``product-name`` refers to docker image name, should be matching the ``PRODUCT_NAME`` from ``SBOM`` list in ``variables-build`` artifact generated during build phase of mci merge workflow. If there are multiple entries, you should make multiple entries with same name and different product-names in vtn config file.
    

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
    - name: 'service-identity'
      product-name: 'token-exchange-second'
      product-version: '1.0.0'
      mgr-list:
        - andrew.m.pitman@hpe.com
      nonmgr-list:
        - eugene.cheverda@hpe.com

..

4. To enable sbom upload to VTN for filesystem sbom Add these entries to `vtn-config.yaml <https://github.com/glcp/managed-ci-workflow/blob/main/utils/vtn-config.yaml>`_ file.

   Note: 

   The ``name`` refers to  repository name.

   The ``product-name`` should be ``fs`` to generate filesystem sbom and upload it to VTN.


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

How to Verify and Download SBOMs
================================

**Steps to verify signature and download SBOM manually for the docker artifacts**

**1. Overview**

MCI stores an SBOM as an attestation in the Docker manifest. The attestation is saved in the Docker repository along with the contents of the Docker image. An 
attestation may be downloaded from the Docker repository, and the SBOM may be extracted.

Attestations with SBOMs are stored in the Docker manifest with a predicate type of https://spdx.dev/Document

The process of downloading and viewing SBOMs stored as attestations in the Docker repository consists of the following steps.

* Download the attestation from the Docker repository.
* Extract the JSON payload from the attestation.
* Decode the base64 data of the payload.
* Extract the SBOM from the predicate of the decoded payload.

**2. Prerequisites**

The following command-line tools are needed for downloading attestations and extracting. SBOMs from the Docker repository. These tools also verify the 
cryptographic signatures MCI creates for Docker containers.

* Install cosign available `here <https://docs.sigstore.dev/system_config/installation/>`_
* Install jq available `here <https://jqlang.github.io/jq/download/>`_

Additionally, you must use docker login with the Docker repository before using the cosign command. The cosign command will reuse the existing docker login 
credentials.

**3. Downloading SBOMs from a Docker Repository**

Example commands for downloading the attestation containing the SBOM-associated with the Docker container.

*MCI Version 1.6.1 and Later*

.. code-block:: yaml

       cosign download attestation \
         --predicate-type=https://spdx.dev/Document \
         quay.io/ccsportal/service-identity:0.0.202 \
         | jq -r .payload | base64 -d | jq .predicate

..

*MCI Version 1.6.0 and Earlier*

Example to fetch the SBOM for the Docker container tagged as quay.io/ccsportal/service-identity:0.0.194. In earlier versions of MCI, the --attachment-tag- 
prefix option is needed.

.. code-block:: yaml 

       cosign download attestation \
        --attachment-tag-prefix='image-spdx-json' \
        --predicate-type=https://spdx.dev/Document \
        quay.io/ccsportal/service-identity:0.0.194 \
        | jq -r .payload | base64 -d | jq .predicate

..

**4. Downloading SBOMS from HPE VTN**

If configured, MCI will upload SBOMs to HPE VTN. The SBOMs may be downloaded from the HPE VTN service. Please consult the HPE VTN docs for details.

**5. Validating Signatures**

MCI signs all Docker containers with a cryptographic signature using SigStore Cosign. You can verify the signature of the Docker container to ensure it has 
not been tampered with.

*MCI Version 1.6.0 and Later*

.. code-block:: yaml   

        cosign verify \
         --certificate-identity-regexp='https://github\.com/glcp/*' \
         --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
         quay.io/ccsportal/service-identity:0.0.202 \
         | jq

..
Alternatively, you can log into quay.io or hpeartifacts-docker.jfrog.io to check for the signature.



Additional Variables
====================

Additional variables that influence the build are stored within the
``.github/mci-variables.yaml`` file.
These will vary between build systems.

.. toctree::
   :maxdepth: 1

   variables/golang-variables/README.md
   variables/maven-variables/README.md
   variables/python-variables/README.md
   variables/sbt-variables/README.md
   variables/shell-variables/README.md
   variables/terraform-variables/README.md
   variables/javascript-variables/README.md
   variables/javascript-image-variables/README.md
   variables/onprem-variables/README.md

**Reusable Workflows within a project owner's control:**

The reusable workflows with prefix ``mci-`` within the **.github/workflows** folder 
are largely boilerplate when installed, with bookend jobs to restore and then preserve the 
build/test environment.  Workflow-specific steps may be placed between the bookend 
jobs detailed below.  These "bookends" should not be altered, and the files should not 
be renamed.

  * pre-stage: .github/workflows/mci-pre-stage.yaml
  * pre-test: .github/workflows/mci-pre-test.yaml


**An example from mci-pre-stage.yaml:**

Each of the reusable workflow dependency files (other than the first) begins with 
two steps that restore a prior environment:

.. code-block:: yaml

    - name: Restore workspace artifacts
      uses: actions/download-artifact@v3
      with:
        name: workspace-artifacts

    - name: Unzip workspace
      run: |
        unzip -oq workspace.zip
        rm workspace.zip
      shell: bash

This example restores from the artifact that was created at the end of the pre-check 
job, then deletes the downloaded zip file.  The artifact itself remains intact and 
can be downloaded again.

Each reusable workflow file ends with two steps that preserve the workspace.  Files 
and resources outside of the workspace will not be preserved (i.e. Docker images and 
running containers):

.. code-block:: yaml

    - name: Zip workspace
      run: |
        zip -rq workspace.zip .
      shell: bash
      
    - name: Preserve directories
      uses: actions/upload-artifact@v3
      with:
        name: workspace-artifacts
        path: workspace.zip


**Reusable workflows outside of a project owner's control:**

In addition to the project-specific workflows, managed-ci-workflow invokes several 
reusable workflows that are outside of a project owner's control.  They are hosted 
at `glcp/managed-ci-workflow <https://github.com/glcp/managed-ci-workflow>`_.

* check
* lint
* unit-test
* build
* post-build


Top-level workflow:

.. code-block:: yaml


   name: Managed CI
   on:
     workflow_dispatch:
     pull_request:
     push:
       branches:
         - main
         - master
         - mainline
       tags:
         - '[0-9]+.[0-9]+.[0-9]+'
   
   jobs:
     pre-check:
       uses: glcp/managed-ci-workflow/.github/workflows/mci-pre-check.yaml@v1.1.0
       secrets: inherit
     pre-stage:
       uses: ./.github/workflows/mci-pre-stage.yaml
       secrets: inherit
       needs: pre-check
     lint:
       uses: glcp/managed-ci-workflow/.github/workflows/mci-lint.yaml@v1.1.0
       secrets: inherit
       needs: pre-stage
     pre-test:
       uses: ./.github/workflows/mci-pre-test.yaml
       secrets: inherit
       needs: lint
     unit-test: 
       uses: glcp/managed-ci-workflow/.github/workflows/mci-unit-test.yaml@v1.1.0
       secrets: inherit
       needs: pre-test
     build:
       uses: glcp/managed-ci-workflow/.github/workflows/mci-build.yaml@v1.1.0
       secrets: inherit
       needs: unit-test
     post-build:
       uses: glcp/managed-ci-workflow/.github/workflows/mci-post-build.yaml@v1.1.0
       secrets: inherit
       needs: build




** Top level workflows, Managed reusable workflows, Example project-specific reusable workflows:



- `Managed reusable workflows <https://github.com/glcp/managed-ci-workflow/blob/main/.github/workflows>`_
- `Top level workflows <https://github.com/glcp/managed-ci-workflow/blob/main/workflows>`_


Managed CI Workflow Deployer 
============================

.. toctree::
   :maxdepth: 0

   mci-deployer/README.md

