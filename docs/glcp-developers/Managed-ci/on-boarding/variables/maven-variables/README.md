### Variables for maven system
```yaml
GLCP_BUILD_SYSTEM: <Build system type supported by managed ci>
## Valid values are golang|golang-lib|maven|python|python-lib|sbt|shell|terraform
## This variable if not delcared in mci-variables.yaml file, will be picked up from repository variable GLCP_BUILD_SYSTEM

APP_NAME: <name of the application in coreupdate and quay(usually repo name)>
## EXAMPLE: For the following repository https://github.com/glcp/subscription-management ==> APP_NAME: subscription-management

APP_ID: <Application ID in coreupdate>
## EXAMPLE: For the following repository https://github.com/glcp/subscription-management ==> APP_ID: f49aae42-439b-4705-8fb3-d486ce4d1d82

# If BUILD_CONTAINER_IMAGE is NOT set, then Managed CI will NOT run inside the container
BUILD_CONTAINER_IMAGE: quay.io/ccsportal/ubuntu:focal-openjdk17-latest-ma

# Used only for manual builds ("workflow_dispatch" event) and hotfixes ("refs/heads/hotfix")
# If CHANNEL is NOT set, then manual builds and hotfixes will skip Corepudate Push
CHANNEL: PR
# Managed CI will use these hard-coded values for other events:
#  pushing to default branch: CHANNEL="Jenkins-Continuous"
#  pull requests: CHANNEL="PR"

# for CI on PR
# If CI_VERSION_PREFIX is NOT set, then the default value is 0.1.0
CI_VERSION_PREFIX: 0.1.0

IMAGE_REGISTRY: quay.io/ccsportal/subscription-management

JFROG_URL: ''
## jfrog url to use for pull images for build default is set to https://aruba.jfrog.io

# List of registries to login to (required by unit testing and build stages)
IMAGE_REGISTRIES:
  - quay.io

# Used by the install-dependencies.sh script
# If MAVEN_VERSION is NOT set, then the default value is 3.9.4
MAVEN_VERSION: 3.9.4

# Used by install-dependencies.sh only if MAVEN_VERSION is set.
# If SHA_MAVEN_TAR_FILE is NOT set, then install-dependencies.sh will default to
#  deaa39e16b2cf20f8cd7d232a1306344f04020e1f0fb28d35492606f647a60fe729cc40d3cba33e093a17aed41bd161fe1240556d0f1b80e773abd408686217e
SHA_MAVEN_TAR_FILE: deaa39e16b2cf20f8cd7d232a1306344f04020e1f0fb28d35492606f647a60fe729cc40d3cba33e093a17aed41bd161fe1240556d0f1b80e773abd408686217e

# Set to true to skip Coreupdate Push
# If this variable is NOT set, then Coreupdate Push WILL run.
#SKIP_COREUPDATE_PUSH: true

# Set to true to skip running the "docker push" command
# If this variable is NOT set, then "docker push" WILL run.
#SKIP_DOCKER_PUSH: true

# Set to true to skip the "Push to JFrog" step
# If this variable is NOT set, then the "Push to JFrog" step WILL run.
#SKIP_JFROG_PUSH: true

PR_VALIDATION: true 
## required only for v1.4.0 and above of the Managed CI
## only used in mci-check stage and needed only if PR TITLE VALIDTION is required

LINT_WORKSPACE_BACKUP: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-pre-lint and mci-lint stages, needed only if application needs to backup workspace in pre-lint stage and use in lint stage 

UNIT_TEST_WORKSPACE_BACKUP: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-pre-test and mci-test stages, needed only if application needs to backup workspace in pre-test stage and use in unit-test stage
## For java based application the backup workspace afat the end of unit test is done irrespective of the variable because of the content requirement during docker image build

# major number of the generated image tag; default is 2
VERSION_MAJOR: 3

# minor number of the generated image tag; default is 0
#VERSION_MINOR: 0

###########################
# These VERSION_OFFSET_* variables are used by Managed CI to set the
# VERSION_NUMBER env var that will be used in the various stages:
#  VERSION_NUMBER = <GitHub run number> + <offset value>
# Managed CI will then construct the tag based on the VERSION_NUMBER
# See https://github.com/glcp/mci-actions-version-number for details

# VERSION_OFFSET_MANUAL is used if the workflow is manually triggered
# If NOT set, then default value is 0
#VERSION_OFFSET_MANUAL: 0

# VERSION_OFFSET_PR is used if the workflow is triggered via a pull request
# If NOT set, then default value is 0
#VERSION_OFFSET_PR: 0

# VERSION_OFFSET_PUSH is used if the workflow is triggered via pushes (merges)
# If NOT set, then default value is 0
#VERSION_OFFSET_PUSH: 0

###########################
```

