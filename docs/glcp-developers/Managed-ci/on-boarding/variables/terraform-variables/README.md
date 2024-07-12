### Variables for Terraform-based repos
```yaml
GLCP_BUILD_SYSTEM: <Build system type supported by managed ci>
## Valid values are golang|golang-lib|maven|python|python-lib|sbt|shell|terraform
## This variable if not delcared in mci-variables.yaml file, will be picked up from repository variable GLCP_BUILD_SYSTEM

APP_NAME: <name of the application in coreupdate and quay(usually repo name)>
## EXAMPLE: For the following repository https://github.com/glcp/ccp-resource-concourse-pipeline-demo ==> APP_NAME: ccp-resource-concourse-pipeline-demo

PREFIX: <Only required if a prefix needed to be added to the tag, if not provided branch name will be added as prefix>
## EXAMPLE: For the following repository https://github.com/glcp/ccp-resource-concourse-pipeline-demo ==> PREFIX: mci-onboard

AWS_OIDC_ROLE: "arn:aws:iam::461650285373:role/ccp-concourse-pipeline-github-actions-role"
AWS_REGION: us-west-2
## AWS OIDC IAM ROLE and AWS REGION to be used to push the images to CCP ECR

DOCKER_PUSH: true
## Determine whether to push the image to ECR and QUAY

QUAY_REGISTRY: quay.io/cloudops
## QUAY Organisation to which the images are pushed

CONTAINER_NAME: devcontainer
## CONTAINER_NAME is used to determmine the ECR repo path QUAY repository that the image need to be pushed and for teh ClusterDB update

ECR_REGISTRY: 461650285373.dkr.ecr.us-west-2.amazonaws.com
## ECR registry where all the container images will be stored

IMAGE_REGISTRIES:
  - quay.io
## List of registries to login to (required by unit testing and build stages)

GO_VERSION: <GO version to be used during unit test and build>
## EXAMPLE: For the following repository https://github.com/glcp/service-registry ==> GO_VERSION: 1.18
## Application teams are required to provide the GO version they use

CDB_URL_QA: "https://api-csp.arubathena.com/v2/application"
CDB_URL_PROD: "https://api-csp.central.arubanetworks.com/v2/application"
## Cluster DB url for QA and PROD

CLUSTERDB_UPDATE: true
## Flag to determine if we need to update cluster db or not
QA_UPDATE: true
## Flag to determine if we need to update ClusterDB QA or not
PROD_UPDATE: false
## Flag to determine if we need to update ClusterDB PROD or not

LINT_WORKSPACE_BACKUP: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-pre-lint and mci-lint stages, needed only if application needs to backup workspace in pre-lint stage and use in lint stage 

UNIT_TEST_WORKSPACE_BACKUP: true
## required only for v1.4.0 and above of the Managed CI
## only used in mci-pre-test and mci-test stages, needed only if application needs to backup workspace in pre-test stage and use in unit-test stage
```

