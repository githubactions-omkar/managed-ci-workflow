# unit-test
This workflow, [unit-test](https://github.com/glcp/managed-ci-workflow/tree/main/.github/workflows/mci-unit-test.yaml), 
depends on the [pre-test](../pre-test/jobs) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered 
(unless otherwise stated).
For Manual trigger of the managed CI on non-default branch the execution can be skipped for manual runs in non-default branch by adding variable `SKIP_CHECKS: true` in mci-variables.yaml

Javascript-based repos use the **javascript-default** ,**javascript-custom** , **javascript-custom-report**  jobs in this workflow.


## javascript-default  
This job is run when there is no input variable `JS_UNIT_TEST_SCRIPT` mentioned in mci variables.
1. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-test` artifact
2.   
   * [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
     from the artifact named `workspace-test` **only if the** `UNIT_TEST_WORKSPACE_BACKUP`
     **variable is set to the string** `true` in the `.github/mci-variables.yaml` file
   * If the workspace restoration was skipped, then
     [checkout](https://github.com/actions/checkout) the application repository
3. Run [Javascript setup](https://github.com/glcp/mci-actions-javascript-setup/tree/v1)
4. Run unit tests with below steps.
 ```text
                echo 
             if [ "${{ env.JS_WORKING_DIR }}" == "" ]; then
                echo ${{ needs.get-mci-variables.outputs.unittest_scripts }}
                pnpm install; pnpm test
             else   
                cd ${{ env.JS_WORKING_DIR }}; pnpm install; pnpm test
             fi
 ```
5. Run merge unit coverage results. This is run only when there is any custom step of creating cypress coverage file in pre-test step. based on availability
   of cypress coverage info file.
   ```text
            if test -f ${{ github.workspace }}/merged_all_cypress_lcov.info;then
               lcov --zerocounters --directory .
               merged_cypress_lcov="${{ github.workspace }}/merged_all_cypress_lcov.info"
               merged_lcov="${{ github.workspace }}/merged_all_lcov.info"
               lcov --add-tracefile "$merged_cypress_lcov" --add-tracefile ~/actions-runner/unit_coverage/lcov.info --output-file "$merged_lcov"
            fi
    ```
6. Run [SonarQube scanning](https://github.com/hpe-actions/sonarqube-scan)
7. [Backup](https://github.com/glcp/mci-actions-workspace-backup/tree/v1) the workspace


## javascript-custom 
This job is run when there is a custom input variable `JS_UNIT_TEST_SCRIPT` mentioned in mci variables. 
And run on a matrix supporting multiple scripts being mentioned.
example JS_UNIT_TEST_SCRIPT: ['test:coverage','e2e:coverage']

1. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-test` artifact
2.   
   * [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
     from the artifact named `workspace-test` **only if the** `UNIT_TEST_WORKSPACE_BACKUP`
     **variable is set to the string** `true` in the `.github/mci-variables.yaml` file
   * If the workspace restoration was skipped, then
     [checkout](https://github.com/actions/checkout) the application repository
3. Run [Javascript setup](https://github.com/glcp/mci-actions-javascript-setup/tree/v1)
4. Run unit tests with below steps.
 ```text
             if [ "${{ env.JS_WORKING_DIR }}" == "" ]; then
                pnpm install; pnpm ${{ matrix.script }}
             else
                cd ${{ env.JS_WORKING_DIR }}; pnpm install; pnpm ${{ matrix.script }}
             fi
 ```
 5. Upload coverage report .nyc_output with artifact-name as 
   `echo "artifact-name=nyc-output-${{ matrix.script }}" | sed  's/:/-/' >> $GITHUB_ENV`
 6. [Backup](https://github.com/glcp/mci-actions-workspace-backup/tree/v1) the workspace    

## javascript-custom-report
This job is run when there is a custom input variable `JS_UNIT_TEST_SCRIPT` mentioned in mci variables. 
1. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from the `variables-test` artifact
2.   
   * [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
     from the artifact named `workspace-test` **only if the** `UNIT_TEST_WORKSPACE_BACKUP`
     **variable is set to the string** `true` in the `.github/mci-variables.yaml` file
   * If the workspace restoration was skipped, then
     [checkout](https://github.com/actions/checkout) the application repository
3. Run [Javascript setup](https://github.com/glcp/mci-actions-javascript-setup/tree/v1)
4. Download coverage reports all of them uploaded from the `javascript-cutom` jobs. And generate a combined coverage report.
  ```text
      - name: Download  coverage reports
        uses: actions/download-artifact@v4
        with:
          pattern: nyc-output-*
          path: .nyc_output
          merge-multiple: true
      - name: Generate coverage report
        shell: bash
        run: |
          ./node_modules/.bin/nyc report --reporter=lcov
  ```
5. Run merge unit coverage results. This is run only when there is any custom step of creating cypress coverage file in pre-test step. based on availability
   of cypress coverage info file.
   ```text
            if test -f ${{ github.workspace }}/merged_all_cypress_lcov.info;then
               lcov --zerocounters --directory .
               merged_cypress_lcov="${{ github.workspace }}/merged_all_cypress_lcov.info"
               merged_lcov="${{ github.workspace }}/merged_all_lcov.info"
               lcov --add-tracefile "$merged_cypress_lcov" --add-tracefile ~/actions-runner/unit_coverage/lcov.info --output-file "$merged_lcov"
            fi
    ```
6. Run [SonarQube scanning](https://github.com/hpe-actions/sonarqube-scan)
7. [Backup](https://github.com/glcp/mci-actions-workspace-backup/tree/v1) the workspace