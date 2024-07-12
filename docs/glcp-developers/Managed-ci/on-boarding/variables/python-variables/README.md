### Variables for python system
```text
GLCP_BUILD_SYSTEM: <Build system type supported by managed ci>
## Valid values are golang|golang-lib|maven|python|python-lib|sbt|shell|terraform
## This variable if not delcared in mci-variables.yaml file, will be picked up from repository variable GLCP_BUILD_SYSTEM

APP_NAME: <name of the application in coreupdate and quay(usually repo name)>
## EXAMPLE: For the following repository https://github.com/glcp/ui-doorway ==> APP_NAME: ui-doorway

APP_ID: <Application ID in coreupdate>
## EXAMPLE: For the following repository https://github.com/glcp/ui-doorway ==> APP_ID: babbffed-ed85-4a21-8a5f-69caa19ee560

APP_NAME_FIPS: <name of the application with FIPS in coreupdate and quay(usually repo name)>
## EXAMPLE: For the following repository https://github.com/glcp/ui-doorway ==> APP_NAME_FIPS: ui-doorway-fips

APP_ID_FIPS: <Application ID for FIPS in coreupdate> 	2405e245-6845-4b12-9785-9950b32cec2d
## EXAMPLE: For the following repository https://github.com/glcp/ui-doorway ==> APP_ID_FIPS: 2405e245-6845-4b12-9785-9950b32cec2d

DEV_ENV_DIR:  <Workspace path to which the glcp/dev-env repository should be cloned(usually ${APP_NAME}-dev-env)> 
## EXAMPLE: For the following repository https://github.com/glcp/ui-doorway ==> DEV_ENV_DIR: ui-doorway-dev-env

DC_PROJECT_NAME: <project name for docker compose (usually ${APP_NAME}-ci)>
## Default: ${APP_NAME}-ci
## EXAMPLE: For the following repository https://github.com/glcp/ui-doorway ==> DEV_ENV_DIR: ui-doorway-ci

UT_DC_PROJECT_SERVICES: Services from dev-env docker-compose to bring up in unit-test dev-env
## Default: `ccs-dev ccs-redis ccs-pg ccs-localstack`

UT_DC_RUNEXEC_MODE: Mode for docker-compose for unit-test dev-env [run|exec]
## Default: `run`

UT_DC_COMMAND: Command to run within the indicated service from docker-compose in unit-test dev-env
## Default: `../bootstrap-dev-env/setup-ccs-dev.sh` (from the mci-actions-bootstrap-dev-env action)

UT_DC_SERVICE: Service within docker-compose file to use for UT_DC_COMMAND (for unit-test dev-env)
## Default: `ccs-dev`

UT_DC_BUILD: Indicate whether to use `--build` for docker-compose for unit-test dev-env
## Default: false

UT_DC_FILE: The name of the docker-compose file from dev-env for unit-test
## Default: `docker-compose_linux.yml`

DEV_ENV_LOCAL: true 
## only needed if they need to use bootstrap scripts for dev-env from the application repository

DEV_ENV_TAG: latest
## providing the ablility to the application team to get a different branch/tag of glcp/dev-env repository

PINGFEDERATE_CLONE: true 
## only needed if application need to clone pingfederate repo for dev-env bootsstrap
## PINGFEDERATE_REPO: https://github.com/glcp/pingfederate

APP_DIR: <only needed if the application source directory is other than "app">
## Example: For the following repository https://github.com/glcp/ccs-appfactory ==> APP_DIR: hpe_ccs_appfactory

BUILD_RUNNER: "Should only be used by the teams that needs to build docker image on a specific runner other than ubuntu-latest. If the variable is provided the python build job expects to find a runner with the variable name and try to build using that runner. If default to be used don't use the variable."
## Example: To use large runners instead of ubuntu-latest ==> BUILD_RUNNER: ubuntu-latest-4-cores

IMAGE_REGISTRIES: 
  - hpeartifacts-glcp-images.jfrog.io
  - quay.io
## List of registries to login to (required by unit testing and build stages)

BASE_IMAGE: <base image required for the docker app build without fips>
BASE_IMAGE_FIPS: <base image required for the docker app build with fips>
## Mostly required in repositories with both "WITH FIPS" and "WITHOUT FIPS" builds which uses same Dockerfile but different base images
## having said that this can also be used to used override base image in Dockerfile dynamically by adding the ARG BASE_IMAGE to it
## required only if MULTI_BUILD: true is not setup from v1.4.0 and above of the Managed CI

PR_VALIDATION: true 
## required only for v1.4.0 and above of the Managed CI
## only used in mci-check stage and needed only if PR TITLE VALIDTION is required

LINT_WORKSPACE_BACKUP: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-pre-lint and mci-lint stages, needed only if application needs to backup workspace in pre-lint stage and use in lint stage 

UNIT_TEST_WORKSPACE_BACKUP: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-pre-test and mci-test stages, needed only if application needs to backup workspace in pre-test stage and use in unit-test stage

# major number of the generated image tag; default is 2
VERSION_MAJOR: 3

# minor number of the generated image tag; default is 0
VERSION_MINOR: 0

# Set to true to skip Coreupdate Push
# If this variable is NOT set, then Coreupdate Push WILL run.
#SKIP_COREUPDATE_PUSH: true

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

MULTI_BUILD: true
## used to execute the builds in paralle
## if set to true PRODUCTS: need to be set in mci-variables.yaml

PRODUCTS:
- BUILD_TYPE: ## This is just an identifier if its 'app' or 'app build with fips' or 'automation' or some other which makes sence to the application team for example if application is producing different images for multiple components
  DOCKERFILE_PATH: ## path to the Dockerfile to be used for the build
  IMAGE_REGISTRY: ## Image registry to which the Docker image need to be pushed
  TARGET: ## target image currently we see applications using prod-image, final, ci-image, automation-base and any other that is being used in Dockerfile
  TAG_EXTENSION: # only required if an extension need to be added to the tag. The final image tag will be "${tag}${TAG_EXTENSION}"
  APP_NAME:  ## Name of the application in coreupdate and quay(usually repo name)
  APP_ID:  ## Application ID in coreupdate
  REGISTRY:  ## registry to which the image is being pushed
  BASE_IMAGE: ## Provide only if the Dockerfile requires a BASE_IMAGE 
  DOCKER_PUSH: ## whether to push the docker image ot not
- BUILD_TYPE: app-fips ## Examples with filled content below
  DOCKERFILE_PATH: ./docker/app/Dockerfile
  IMAGE_REGISTRY: quay.io/ccsportal/sample-python-app
  TARGET: final
  TAG_EXTENSION: '-fips'
  APP_NAME: sample-python-app
  APP_ID: 89f5abfd-2ea4-47cd-a406-05c16627702a
  REGISTRY: quay.io
  BASE_IMAGE: quay.io/ccsportal/ubuntu:python38-latest-ma 
  DOCKER_PUSH: true
- BUILD_TYPE: automation
  DOCKERFILE_PATH: ./tests/feature_test/docker/Dockerfile_FT
  IMAGE_REGISTRY: quay.io/ccsportal/sample-python-app
  TARGET: automation-base
  TAG_EXTENSION: '-automation'
  APP_NAME: sample-python-app
  APP_ID: 89f5abfd-2ea4-47cd-a406-05c16627702a
  REGISTRY: quay.io
  BASE_IMAGE: quay.io/ccsportal/ubuntu:python38-latest-ma 
  DOCKER_PUSH: true

## the above example shows three typical builds that are available for python which is 'app', 'app build with fips' and 'automation'
```
