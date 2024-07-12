### Variables for golang system
```yaml
GLCP_BUILD_SYSTEM: <Build system type supported by managed ci>
## Valid values are golang|golang-lib|maven|python|python-lib|sbt|shell|terraform
## This variable if not delcared in mci-variables.yaml file, will be picked up from repository variable GLCP_BUILD_SYSTEM

APP_NAME: <name of the application in coreupdate and quay(usually repo name)>
## EXAMPLE: For the following repository https://github.com/glcp/service-registry ==> APP_NAME: service-registry

APP_ID: <Application ID in coreupdate>
## EXAMPLE: For the following repository https://github.com/glcp/service-registry ==> APP_ID: ea047964-f9cf-4a3f-a239-7c2d7f30b409

GO_VERSION: <GO version to be used during unit test and build>
## EXAMPLE: For the following repository https://github.com/glcp/service-registry ==> GO_VERSION: 1.18
## Application teams are required to provide the GO version they use

APP_DIR: <only needed if the application source directory is other than "app">
## Example: For the following repository https://github.com/glcp/ccs-appfactory ==> APP_DIR: hpe_ccs_appfactory

IMAGE_REGISTRIES:
  - hpeartifacts-glcp-images.jfrog.io
  - quay.io
## List of registries to login to (required by unit testing and build stages)
## Used by the glcp/mci-actions-registry-login action

PR_VALIDATION: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-check stage and needed only if PR TITLE VALIDTION is required

LINT_WORKSPACE_BACKUP: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-pre-lint and mci-lint stages, needed only if application needs to backup workspace in pre-lint stage and use in lint stage

UNIT_TEST_WORKSPACE_BACKUP: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-pre-test and mci-test stages, needed only if application needs to backup workspace in pre-test stage and use in unit-test stage

VERSION: <MAJOR:MINOR values in the version to be used>
## EXAMPLE: For the following repository https://github.com/glcp/service-registry ==> VERSION: '3.2'
## please place them in quotes, because if its 3.0 without quotes it will be considered as 3

BOOTSTRAP_DEV_ENV:true
##required only if you want to run UT in the dev env

DC_COMMAND:''
##optional command to run for UT in dev-env .by default it runs "../bootstrap-dev-env/setup-ccs-dev.sh"

DC_PROJECT_SERVICES: ''
##optional servies required for dev env to run UT . default is set to ccs-dev ccs-redis ccs-pg ccs-localstack

JFROG_URL: ''
## jfrog url to use for pull images for build default is set to https://aruba.jfrog.io





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

PRODUCTS:
- BUILD_TYPE: ## This is just an identifier if its 'app' or 'app build with fips' or 'automation' or some other which makes sence to the application team for example if application is producing different images for multiple components
  DOCKERFILE_PATH: ## path to the Dockerfile to be used for the build
  IMAGE_REGISTRY: ## Image registry to which the Docker image need to be pushed
  TARGET: ## target image currently we see applications using prod-image, final, ci-image, automation-base and any other that is being used in Dockerfile
  TAG_EXTENSION: # only required if an extension need to be added to the tag. The final image tag will be "${tag}${TAG_EXTENSION}"
  APP_NAME:  ## Name of the application in coreupdate and quay(usually repo name)
  APP_ID:  ## Application ID in coreupdate
  REGISTRY:  ## registry to which the image is being pushed
  BASE_IMAGE: ## Provide only if the Dockerfile requires a BASE_IMAGE argument ignore if not
  DOCKER_PUSH: ## whether to push the docker image ot not
- BUILD_TYPE: app ## Examples with filled content below
  DOCKERFILE_PATH: ./docker/deploy/token-exchange/Dockerfile
  IMAGE_REGISTRY: quay.io/ccsportal/token-exchange
  TARGET: final
  TAG_EXTENSION: '-token-exchange'
  APP_NAME: service-registry
  APP_ID: ea047964-f9cf-4a3f-a239-7c2d7f30b409
  REGISTRY: quay.io
  BASE_IMAGE: quay.io/ccsportal/ubuntu:golang118-dev-ma-202208151538
  DOCKER_PUSH: true
- BUILD_TYPE: automation
  DOCKERFILE_PATH: ./docker/deploy/pce-api-clients/Dockerfile
  IMAGE_REGISTRY: quay.io/ccsportal/pce-api-clients
  TARGET: final
  TAG_EXTENSION: '-pce-api-clients'
  APP_NAME: service-registry
  APP_ID: ea047964-f9cf-4a3f-a239-7c2d7f30b409
  REGISTRY: quay.io
  BASE_IMAGE: hpeartifacts-glcp-images.jfrog.io/hpe.com/go:1.19-dev
  DOCKER_PUSH: true

## the above example shows three typical builds that are available for go base repository service-registry which is 'app' build for multiple components like token-exchange, api-clients, pce-api-clients etc., and 'automation'

########################################################################
### Only the following variables need to be set if the repo is a mirrored repo.

APP_NAME: <name of the mirrored repo>
## example: APP_NAME: tracing-proxy

GET_EXTERNAL_RELEASE_VERSION: true
## The release version of the external repo is used to tag the generated artifacts.

GO_VERSION: <go-version>
## The version of Go to be used
## example: GO_VERSION: 1.21.3

IMAGE_REGISTRIES:
  - hpeartifacts-glcp-images.jfrog.io
## List of all image registeries login required during the build

JFROG_URL: https://hpeartifacts.jfrog.io

ORG_NAME: <the org name of the external repo>
## This value is used to query the external repo to get the external release version
## example: ORG_NAME: opsramp

PUSH_TO_JFROG: true
## If set to true, then the artifacts will be uploaded to HPE Artifactory
## If not set at all, then the artifacts will NOT be uploaded to HPE Artifactory

SKIP_COREUPDATE_PUSH: true
## Whether or not to skip the push to coreupdate

SKIP_SET_VERSION_NUMBER: true
## Whether or not to skip the call to https://github.com/glcp/mci-actions-version-number

########################################################################

```

