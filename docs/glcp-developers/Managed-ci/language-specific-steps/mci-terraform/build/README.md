# build
This workflow, [build](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build.yaml),
depends on the [unit-test](../unit-test/README) workflow.
All jobs and steps in this workflow are configured to run whenever Managed CI is triggered
(unless otherwise stated).

Builds for Terraform-based repos use the [mci-build-terraform.yaml](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build-terraform.yaml)
workflow and the workflow includes these jobs:

* [create-tag](#create-tag)
* [build-publish](#build-publish)
* [clusterdb](#clusterdb)

## create-tag 
This job runs these steps to construct the output variables `tag` and `containerVersion`.
This job runs only on the default branch, branch names starting with
`infra-release`, or when run manually.
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. Run [mci-actions-tagging](https://github.com/glcp/mci-actions-tagging/tree/v1)
   to set output variables `tag` and `containerVersion`

## build-publish
This job runs only on the default branch, branch names starting with
`infra-release`, or when run manually.
1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
   from `.github/mci-variables.yaml` file
3. [Set up](https://github.com/docker/setup-qemu-action/tree/v2) QEMU
4. [Set up](https://github.com/docker/setup-buildx-action/tree/v2) Docker Buildx
5. [Login](https://github.com/glcp/mci-actions-registry-login/tree/v2) to the registry
6. [Configure](https://github.com/aws-actions/configure-aws-credentials/tree/v2)
   AWS Credentials
7. [Get](https://github.com/aws-actions/amazon-ecr-login/tree/v1) Amazon ECR Login Token
8. [Build](https://github.com/docker/build-push-action/tree/v4)
9. Update the SBOM information in `.github/mci-variables.yaml` with the Product name,
   URL and SHA1.  This updated info will be used in the `sbom-upload` job in the
   post-build job.
10. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
    to the artifact named `variables-build`
11. [Backup](https://github.com/glcp/mci-actions-workspace-backup/tree/v1) the workspace
    to the artifact named `workspace-build`

## clusterdb

1. [Restore](https://github.com/glcp/mci-actions-workspace-restore/tree/v1) the workspace
   from the artifact named `workspace-build`
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI 
   variables from the `variables-build` artifact
3. Update the ClusterDB

