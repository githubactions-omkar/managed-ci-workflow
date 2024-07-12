# build
This workflow, [build](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build.yaml),
depends on the [unit-test](../unit-test/README) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered
(unless otherwise stated).

Builds for Terraform-based repos use the [mci-build-terraform.yaml](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build-terraform.yaml)
workflow and the workflow includes these jobs:

* [create-tag](#create-tag)
* [build-custom-apt](#build-custom-apt)
* [build-platform-scripts](#build-platform-scripts)
* [build-ova](#build-ova)
* [publish-ova](#publish-ova)

## create-tag
This job runs these steps to construct the output variable `tag`:
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Construct](https://github.com/glcp/mci-actions-version-number/tree/v1) and set the
   environment variable `VERSION_NUMBER`, which is used in the step below
4. Construct the output   variable `tag` from ${{vars.semantic_version}} and `VERSION_NUMBER`.
5. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
   to the artifact named `variables-build``

## build-custom-apt
This job runs only on the default branch,  and when run is scheduled.
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Construct](https://github.com/glcp/mci-actions-version-number/tree/v1) and set the
   environment variable `VERSION_NUMBER
4. Build custom-apt based using the code.
  ```
          - name: overwrite WORKFLOW_TYPE
        if: github.event_name != 'schedule' && github.event_name != 'workflow_dispatch'
        run: |
          if [[ "${{ github.event_name }}" == "push" && "${{ github.ref_name }}" == "${{ github.event.repository.default_branch }}" ]]; then
          echo "WORKFLOW_TYPE=merge" >> $GITHUB_ENV
          else
          echo "WORKFLOW_TYPE=ci" >> $GITHUB_ENV
          fi
      - name: Check if sources changed
        uses: glcp/paths-filter@v2
        id: sources
        with:
          filters: |
            changed:
              - 'custom-apt/**'
              - 'clone/**'
              - 'clean/**'
              - 'scripts/**'
      - name: Show jFrog Artifacts URL
        run: |
          echo "If this build is successful you should find the artifacts here:"
          echo
          echo "  - https://hpeartifacts.jfrog.io/ui/repos/tree/General/glcp_opg_files/glcp_op_binaries/${{ github.ref_name }}/${VERSION_NUMBER}/"
          echo
      - name: Dump Environment Variables for Debugging
        run: env

      - name: Ensure the OVA Builder VM has been started (make start)
        if: steps.sources.outputs.changed == 'true' ## && !contains(fromJSON('["golden"]'), env.WORKFLOW_TYPE) }} TODO: check with onprem team
        shell: bash
        run: |
           echo "Ensure the OVA Builder VM has been started (make start)"
           echo "======================================================="
           make start
           echo ""
           echo "Clean the Work Directories of the OVA Builder (make clean)"
           echo "=========================================================="
           make clean
           echo ""
           echo "Clone onprem-ova to VM (make clone)"
           echo "==================================="
           make clone
           echo ""
           echo "Build custom APT binaries tarball and upload to jfrog"
           echo "===================================================="
           make custom-apt
  ```


## build-platform-scripts
This job runs only on the default branch,  and when run is scheduled.
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Construct](https://github.com/glcp/mci-actions-version-number/tree/v1) and set the
   environment variable `VERSION_NUMBER
4. Build custom-apt based using the code.
  ```
      - name: overwrite WORKFLOW_TYPE
        if: github.event_name != 'schedule' && github.event_name != 'workflow_dispatch'
        run: |
          if [[ "${{ github.event_name }}" == "push" && "${{ github.ref_name }}" == "${{ github.event.repository.default_branch }}" ]]; then
          echo "WORKFLOW_TYPE=merge" >> $GITHUB_ENV
          else
          echo "WORKFLOW_TYPE=ci" >> $GITHUB_ENV
          fi
      - name: Check if sources changed
        uses: glcp/paths-filter@v2
        id: sources
        with:
          filters: |
            changed:
              - 'custom-apt/**'
              - 'clone/**'
              - 'clean/**'
              - 'scripts/**'
      - name: Show jFrog Artifacts URL
        run: |
          echo "If this build is successful you should find the artifacts here:"
          echo
          # echo "  - https://hpeartifacts.jfrog.io/ui/repos/tree/General/glcp_opg_files/glcp_op_binaries/${{ github.ref_name }}/${{ github.run_number }}/"
          echo "  - https://hpeartifacts.jfrog.io/ui/repos/tree/General/glcp_opg_files/glcp_op_binaries/${{ github.ref_name }}/${VERSION_NUMBER}/"
          echo
      - name: Dump Environment Variables for Debugging
        run: env

      - name: Ensure the OVA Builder VM has been started (make start)
        if: steps.sources.outputs.changed == 'true'  ## && !contains(fromJSON('["golden"]'), env.WORKFLOW_TYPE) }} TODO: check with onprem team
        shell: bash
        run: |
           echo "Ensure the OVA Builder VM has been started (make start)"
           echo "======================================================="
           make start
           echo ""
           echo "Clean the Work Directories of the OVA Builder (make clean)"
           echo "=========================================================="
           make clean
           echo ""
           echo "Clone onprem-ova to VM (make clone)"
           echo "==================================="
           make clone
           echo ""
           echo "Build platform scripts tarball and upload to jfrog"
           echo "=================================================="
           make platform-scripts
   ```

## build-ova
This job runs only on the default branch,  and when run is scheduled.
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Construct](https://github.com/glcp/mci-actions-version-number/tree/v1) and set the
   environment variable `VERSION_NUMBER
4. Set few environment variables based on VERSION_NUMBER.
  ```
       - name: overwrite WORKFLOW_TYPE
        if: github.event_name != 'schedule' && github.event_name != 'workflow_dispatch'
        run: |
          if [[ "${{ github.event_name }}" == "push" && "${{ github.ref_name }}" == "${{ github.event.repository.default_branch }}" ]]; then
          echo "WORKFLOW_TYPE=merge" >> $GITHUB_ENV
          else
          echo "WORKFLOW_TYPE=ci" >> $GITHUB_ENV
          fi
      - name: Registry login
        uses: glcp/mci-actions-registry-login@v1
        with: 
          secrets: ${{ toJson(secrets) }}


      - name: Set ARTIFACTS_BUILD_DIR
        run: |
            echo "ARTIFACTS_BUILD_DIR=~/onprem-ova-builds/build-${{ env.WORKFLOW_TYPE }}-${VERSION_NUMBER}" >> $GITHUB_ENV
      - name: Show artifacts destination
        run: |
            echo "If this build is successful, you should find the artifacts here:"
            echo
            echo " - ${ARTIFACTS_SERVER_USER}@${ARTIFACTS_SERVER}:${ARTIFACTS_BUILD_DIR}/"
            echo
      - name: Set environment variables
        run: |
            echo "UBUNTU_ISO_PATH=${HOME}/iso-images/ubuntu-20.04.1-legacy-server-amd64.iso" >> $GITHUB_ENV
      - name: Dump Environment Variables for Debugging
        run: env
  ```

5. [Build Ova](https://github.com/glcp/mci-actions-ova-build@v1) Runs the ova build.

## publish-ova
This job runs only on the default branch,  and when run is scheduled.
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Construct](https://github.com/glcp/mci-actions-version-number/tree/v1) and set the
   environment variable `VERSION_NUMBER
4. Copies built artifacts to artifact server.
  ```
      - name: overwrite WORKFLOW_TYPE
        if: github.event_name != 'schedule' && github.event_name != 'workflow_dispatch'
        run: |
          if [[ "${{ github.event_name }}" == "push" && "${{ github.ref_name }}" == "${{ github.event.repository.default_branch }}" ]]; then
          echo "WORKFLOW_TYPE=merge" >> $GITHUB_ENV
          else
          echo "WORKFLOW_TYPE=ci" >> $GITHUB_ENV
          fi
      - name: Set variables
        run: |
            # echo "TARGET_DIR_PREFIX=~/golden-image" >> $GITHUB_ENV
            # echo "TARGET_DIR=golden-image-staging-${{ github.run_number }}" >> $GITHUB_ENV
            # echo "ARTIFACTS_BUILD_DIR=~/onprem-ova-builds/build-${{ env.WORKFLOW_TYPE }}-${{ github.run_number }}" >> $GITHUB_ENV
            echo "TARGET_DIR_PREFIX=~/golden-image" >> $GITHUB_ENV
            echo "TARGET_DIR=golden-image-staging-${VERSION_NUMBER}" >> $GITHUB_ENV
            echo "ARTIFACTS_BUILD_DIR=~/onprem-ova-builds/build-${{ env.WORKFLOW_TYPE }}-${VERSION_NUMBER}" >> $GITHUB_ENV
      - run: |
            ssh ${{ env.ARTIFACTS_SERVER_USER }}@${{ env.ARTIFACTS_SERVER }} \
              "mkdir -p ${{ env.TARGET_DIR}} && \
              cp ${ARTIFACTS_BUILD_DIR}/*.ova ${{ env.TARGET_DIR}}"
  ```




