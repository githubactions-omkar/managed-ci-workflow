### Variables for onprem-based repos
```yaml
GLCP_BUILD_SYSTEM: <Build system type supported by managed ci>
## Valid values are golang|golang-lib|maven|python|python-lib|sbt|shell|onprem|onprem
## This variable if not delcared in mci-variables.yaml file, will be picked up from repository variable GLCP_BUILD_SYSTEM

APP_NAME: <name of the application in coreupdate and quay(usually repo name)>

ARTIFACTS_SERVER_USER: esroot
## Artifacts server user
## EXAMPLE: For the following repository https://github.com/glcp/onprem-ova/


ARTIFACTS_SERVER: 10.14.144.19
## Artifacts server servername/ip
## EXAMPLE: For the following repository https://github.com/glcp/onprem-ova/


VCENTER_SERVER: "vcenter01-gl325-g10ps02.hstlabs.glcp.hpecorp.net"
## Vm center server 
## EXAMPLE: For the following repository https://github.com/glcp/onprem-ova/

WORKFLOW_TYPE: golden
## EXAMPLE: For the following repository https://github.com/glcp/onprem-ova/

IMAGE_REGISTRIES:
  - quay.io
## List of registries to login to (required by unit testing and build stages)
