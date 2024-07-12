# Creating Hotfix-branch
 Hotfix workflow is used to create a hot fix branch from the Tag which is passed as in input parameter. this workflow does the following steps
 
     1. create branch  out of Tag with name hotfix-<Tag> 
     2. add manage-ci-hotfix-<Tag>.yaml workflow to the branch 
     3. update the version in mci-variables
     

    
**Functions managed by managed-ci-hotfix:**

* check
  * secret scan
  * malware scanning
  * PR title check
*  lint
   * also includes code reformatting for languages that support it (ie: SBT/scala)
*  unit-test
*  build
*  post-build
  
  * [SonarQube](https://github.com/glcp/devx-sonarqube/tree/main)
  * SigStore cosign container signing
  * SBOM upload to HPE VTN
 
**Functions left to the discretion of project owners:**
 * pre-lint
 * pre-test
 
 manage-ci-hotfix.yaml workflow will run on push to hotfix-<Tag> branch and default core update channel for the build on this branch is "GLCP-HF". 
 To add hotfix workflow copy the below workflow 
 
 ```yaml
 
 name: Managed CI on Merge HOTFIX

 on:
   workflow_dispatch:
     inputs:
       tag:
         description: 'Enter valid tag name'
         type: string
         required: true

 jobs:
   hot-fix:
     permissions: write-all
     runs-on: ubuntu-latest
     steps:
       - name: Generate github app token
         id: generate_token
         uses: glcp/github-app-token-action@v1.7.0
         with:
           app_id: ${{ secrets.APP_ID }}
           private_key: ${{ secrets.PRIVATE_KEY }}

       - name: Clone App repo
         uses: actions/checkout@v3.3.0
         with:
           token: ${{ steps.generate_token.outputs.token }}
           ref: ${{ inputs.tag }}


       - name: Clone Managed CI
         uses: actions/checkout@v3.3.0
         with:
           repository: glcp/managed-ci-workflow
           token: ${{ secrets.GLCP_GH_TOKEN }}
           path: managed-ci

       - name: Create hotfix branch
         env:
           GITHUB_TOKEN: ${{ steps.generate_token.outputs.token }}
           GIT_AUTHOR_NAME: GLCP HOTFIX
           GIT_AUTHOR_EMAIL: glcp-gh-bot@github.com
           GIT_COMMITTER_NAME: GLCP HOTFIX
           GIT_COMMITTER_EMAIL: glcp-gh-bot@github.com
           Tag: ${{inputs.tag}}
         run: |
           chmod +x managed-ci/hotfix/scripts/hotfix.sh
           bash managed-ci/hotfix/scripts/hotfix.sh
```

