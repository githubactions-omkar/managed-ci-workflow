### Variables for sbt system
```yaml
GLCP_BUILD_SYSTEM: <Build system type supported by managed ci>
## Valid values are golang|golang-lib|maven|python|python-lib|sbt|shell|terraform
## This variable if not delcared in mci-variables.yaml file, will be picked up from repository variable GLCP_BUILD_SYSTEM

APP_NAME: <name of the application in coreupdate and quay(usually repo name)>
## EXAMPLE: For the following repository https://github.com/glcp/harmony-data-plane ==> APP_NAME: harmony-data-plane

JAVA_VERSION: 11
DISTRIBUTION: zulu 
## JAVA VERSION and DISTRIBUTION to be used for unit test and build
## Please check the link for the list of available distributions; https://github.com/marketplace/actions/setup-java-jdk#:~:text=15.0.0%2B2%2Dea-,Supported%20distributions,-Currently%2C%20the%20following

IMAGE_REGISTRIES:
  - hpeartifacts-docker-harmony.jfrog.io
## List of registries to login to (required by unit testing and build stages)

LINT_WORKSPACE_BACKUP: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-pre-lint and mci-lint stages, needed only if application needs to backup workspace in pre-lint stage and use in lint stage 

UNIT_TEST_WORKSPACE_BACKUP: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-pre-test and mci-test stages, needed only if application needs to backup workspace in pre-test stage and use in unit-test stage
```
