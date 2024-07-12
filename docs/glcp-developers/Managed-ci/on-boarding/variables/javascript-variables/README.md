### Variables for javascript system
```text
GLCP_BUILD_SYSTEM: <Build system type supported by managed ci>
## Valid values are golang|golang-lib|maven|python|python-lib|sbt|shell|terraform|javascript|javascript-image
## This variable if not delcared in mci-variables.yaml file, will be picked up from repository variable GLCP_BUILD_SYSTEM

APP_NAME: <name of the application in coreupdate and quay(usually repo name)>
## EXAMPLE: For the following repository https://github.com/glcp/ui-doorway ==> APP_NAME: ui-doorway

IMAGE_REGISTRIES: 
  - hpeartifacts-glcp-images.jfrog.io
  - quay.io
## List of registries to login to (required by unit testing and build stages)

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

#############################################
#Java script specific variables used by build
# JS_BUILD_SCRIPT: build
# JS_BUILD_PATH: dist
# JS_WORKING_DIR: ./
# JS_PACKAGE_MANAGER: pnpm
# JS_CACHE_VERSION: v1
# JS_NODE_VERSION: 16
# JS_PNPM_VERSION: 7
# JS_PNPM_RECURSIVE: true
# Default values of above  variables are listed
# These can be changed if passed through mci-variables
###############################################
# Java script variable to specify test script(s)
# Example value given below. By default test script is 'test'
# JS_UNIT_TEST_SCRIPTS: ['test:coverage','e2e:coverage']
#
###############################################

```
