### Variables for shell system
```yaml
GLCP_BUILD_SYSTEM: <Build system type supported by managed ci>
## Valid values are golang|golang-lib|maven|python|python-lib|sbt|shell|terraform
## This variable if not delcared in mci-variables.yaml file, will be picked up from repository variable GLCP_BUILD_SYSTEM

APP_NAME: <name of the application in coreupdate and quay(usually repo name)>
## EXAMPLE: For the following repository https://github.com/glcp/pingfederate-base ==> APP_NAME: pingfederate-base

SCRIPT_TO_RUN: './scripts/build_base.sh'
##  The script to be triggered to start the build

VERSION: <MAJOR:MINOR values in the version to be used>
## EXAMPLE: For the following repository https://github.com/glcp/pingfederate-base ==> VERSION: '1.0'
## please place them in quotes, because if its 1.0 without quotes it will be considered as 1

DOCKER_PUSH: 1
## Set this value to '1' if you want to push images into quay
## only needed if you want to push the docker image

IMAGE_REGISTRIES: 
  - quay.io
## List of registries to login to (required by unit testing and build stages)

```
