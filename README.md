## Managed CI Workflow

This devops managed workflow is designed to be shared by most or all repositories that produce production artifacts.   It consists of a primary workflow that delegates work to a set of reusable workflows within both glcp/managed-ci-workflow and a local project repository.

### Where to find help
HPE Internal Slack: #ask-glcp-managed-ci 
Jira Help Desk ticket: https://hpe.atlassian.net/servicedesk/customer/portal/10/group/42/create/171


### Managed CI Features
Functions managed by managed-ci-workflow:
*  pre-check
    * secret scan
    * malware scanning
    * PR title check
*  lint
    * also includes code reformatting for languages that support it (ie: SBT/scala)
*  unit tests
*  build
*  post-build
    * ![SonarQube](https://github.com/glcp/devx-sonarqube/tree/main) 
    * SigStore cosign container signing
    * SBOM upload to HPE VTN
 
Functions left to the discretion of project owners:
* pre-stage
* pre-test

**NOTE:** Release notes for the managed ci workflows can be [found here](https://hpe.atlassian.net/l/cp/HHHM0mxj). Please refer the release notes for the latest changes

 
**End of Support (EOS)

The DevOps team supports latest minor version plus 3 most recent minor versions released before.
Every team can continue to use older versions, but no support will be provided.

**End of Life (EOL)
The code reference for minor versions that are more than 6 releases older than current release will be removed and MCI will not work anymore.
Repositories that are still using old versions will be required to upgrade to have their CI working.
 
**Mandatory upgrade request
It is possible that teams will be requested to upgrade earlier in case of vulnerability or mandatory new features required for GLP CI process.
 
**Upgrade Process
To upgrade the owner of the repository has to raise a PR for https://github.com/glcp/managed-ci-workflow/blob/main/workflow-deployment.yaml .
Release notes will include if any additional change is required for specific version.
 
**Notification
Owners of repositories onboarded in MCI will be notified for any new release.
Notification will include EOS and EOL announcements.
