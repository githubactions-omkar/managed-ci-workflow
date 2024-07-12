# Build on PR for Python
                                                                           
When the [repository variable](../../on-boarding/index.html#repository-variables)
`GLCP_BUILD_SYSTEM` is set to `python`, the job [build-python](#build-python) is executed
for Python-based repositories.

### build-python
Thin job is used for the app build and will run inside a container if the 
output variable from the [get-docker-image-name](#get-docker-image-name) job is non-empty.

The following steps are executed in order.

|    | _Description_                                                                                                | _Actions_                                       |
|:--:|:-------------------------------------------------------------------------------------------------------------|:------------------------------------------------|
| 1  | [Checkout source code](https://github.com/actions/checkout/tree/v3.3.0)                                      | ```actions/checkout@v3.3.0```                   |
| 2  | [Set environment variables for the job](https://github.com/glcp/mci-actions-variables-restore/tree/v1)       | ```glcp/mci-actions-variables-restore@v1```     |
| 3  | [Login to Docker registries](https://github.com/glcp/mci-actions-registry-login/tree/v1)                     | ```glcp/mci-actions-registry-login@v1```        |
| 4* | [Build without FIPS and export to Docker](https://github.com/glcp/mci-actions-docker-build-push-app/tree/v3) | ```glcp/mci-actions-docker-build-push-app@v3``` |
| 5  | [Scan for CVE](https://github.com/glcp/jfrog-scan-cve/tree/main)                                             | ```glcp/jfrog-scan-cve@v1```                    |
| 6* | [Build FIPS image and export to Docker](https://github.com/glcp/mci-actions-docker-build-push-app/tree/v3)   | ```glcp/mci-actions-docker-build-push-app@v3``` |
| 7  | [Scan for CVE](https://github.com/glcp/jfrog-scan-cve/tree/main)                                             | ```glcp/jfrog-scan-cve@v1```                    |

Note on steps 4 and 6: the following additional parameters are passed in:
```
docker_load: true
docker_push: false
```

#### Inputs/Secrets for build-app-maven

| _Input_        | _Default_                                                | _Description_                                                                                 | _Required_ |
|:---------------|:---------------------------------------------------------|:----------------------------------------------------------------------------------------------|:-----------|
| appname        | ```${{ env.APP_NAME }}```                                | Application name in coreupdate, Usually same as the repository name                           | false      |
| base_image     | ```${{ env.BASE_IMAGE }}```                              | the base image passed to glcp/mci-actions-docker-build-push-app for the Docker App build      | false      |
|                | --OR-- ```${{ env.BASE_IMAGE_FIPS }}```                  | the base image passed to glcp/mci-actions-docker-build-push-app for the Docker FIPS App build | false      |
| docker_load    | ```false```                                              | local build, and export to Docker                                                             | false      |
| docker_push    | ```true```                                               | local build, so do NOT push to registry                                                       | false      |
| registry       | ```quay.io```                                            | Registry name                                                                                 | true       |
| image_registry | ```"quay.io/ccsportal/${{ env.APP_NAME }}"```            | Quay registry                                                                                 | false      |
| tag            | ```ci_image```                                           | Application tag                                                                               | false      |
| target         | ```ci-stage```                                           | Docker target                                                                                 | false      |
| quay_username  | ```${{ secrets.CCS_QUAY_CCSPORTAL_BUILDER }}```          | Quay Username                                                                                 | true       |
| quay_password  | ```${{ secrets.CCS_QUAY_CCSPORTAL_BUILDER_PASSWORD }}``` | Quay Password                                                                                 | true       |
| jfrog_username | ```${{ secrets.CCS_JFROG_USERNAME }}```                  | JFROG Username                                                                                | false      |
| jfrog_password | ```${{ secrets.CCS_JFROG_PASSWORD }}```                  | JFROG password                                                                                | false      |

