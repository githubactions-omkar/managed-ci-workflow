# build
This workflow, [build](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build.yaml),
depends on the [unit-test](../unit-test/README) workflow.
All jobs and steps in this workflow are configured to run only on the default branch
or when `github.event.action == 'released'`

Builds for Scala-based repos use the [mci-build-sbt.yaml](https://github.com/glcp/managed-ci-workflow/tree/v1.4.0/.github/workflows/mci-build-sbt.yaml)
workflow and the workflow includes these steps:

1. [Checkout](https://github.com/actions/checkout) the application repository
2. [Retrieve](https://github.com/glcp/mci-actions-variables-restore/tree/v2) the MCI variables
3. [Set up](https://github.com/actions/setup-java/tree/v1) the JDK using the MCI variables
   `JAVA_VERSION` and `DISTRIBUTION`
4. [Set up](https://github.com/glcp/harmony-actions-artifactory-credentials)
   artifactory credentials
5. Copy Credentials to appropriate locations
6. [Login](https://github.com/glcp/mci-actions-registry-login/tree/v1) to the registry
7. Setup helm
8. Run `sbt build`
9. Update the SBOM information in `.github/mci-variables.yaml` with the Product name, 
   URL and SHA1.  This updated info will be used in the `sbom-upload` job in the 
   post-build job.
10. [Backup](https://github.com/glcp/mci-actions-variables-backup/tree/v2) the MCI variables
    to the artifact named `variables-build`
11. Create `target/version.txt` with the version of SBT
12. [Checkout](https://github.com/actions/checkout) the 
    [harmony-versions](https://github.com/glcp/harmony-versions) repo
13. Update the `tag` key in `manifests/harmony-version.yaml` and push changes
14. [Backup](https://github.com/glcp/mci-actions-sbt-backup/tree/v1) the generated artifacts

