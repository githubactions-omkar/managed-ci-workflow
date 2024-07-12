# Build on PR for Java
                                                                           
When the [repository variable](../../on-boarding/index.html#repository-variables)
`GLCP_BUILD_SYSTEM` is set to `maven`, the jobs 
[get-docker-image-name](#get-docker-image-name), [build-maven-app](#build-maven-app) 
and [build-maven-coreupdate](#build-maven-coreupdate) are executed to run a build 
for Java-based repositories.
   
### 1. get-docker-image-name
This job gets the Docker image name from the variable `BUILD_CONTAINER_IMAGE` 
in the `.github/mci-variables.yaml` file and sets an output variable that 
the [build-maven-app](#build-maven-app) job will use.  If the `BUILD_CONTAINER_IMAGE`
variable doesn't exist in the `.github/mci-variables.yaml` file, or if the variable
is set to an empty value, then [build-maven-app](#build-maven-app) job will NOT
run inside a container.

```yaml
  get-docker-image-name:
    runs-on: ubuntu-latest
    needs: checks-done
    if: |
      vars.GLCP_BUILD_SYSTEM == 'maven' &&
      (github.event_name == 'pull_request' && 
       contains(fromJSON('["opened", "reopened", "synchronize"]'), github.event.action))
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3.3.0

      - uses: glcp/mci-actions-variables-restore@v1
        with:
          use-artifact: false

      - name: Get Docker image name from MCI variables
        id: this-docker-image-name
        run: |
          echo "BUILD_CONTAINER_IMAGE=$BUILD_CONTAINER_IMAGE" >> $GITHUB_OUTPUT
    outputs:
      docker-image-name: ${{ steps.this-docker-image-name.outputs.BUILD_CONTAINER_IMAGE }}
```

### 2. build-maven-app
This job is used for the app build and will run inside a container if the 
output variable from the [get-docker-image-name](#get-docker-image-name) job is non-empty.

The following steps are executed in order.

|    | _Description_                                                                                          | _Actions_                                       |
|:--:|:-------------------------------------------------------------------------------------------------------|:------------------------------------------------|
| 1  | [Checkout source code](https://github.com/actions/checkout/tree/v3.3.0)                                | ```actions/checkout@v3.3.0```                   |
| 2  | [Set environment variables for the job](https://github.com/glcp/mci-actions-variables-restore/tree/v1) | ```glcp/mci-actions-variables-restore@v1```     |
| 3  | Install dependencies                                                                                   | Execute ```./install-dependencies.sh```         |
| 4  | [Set environment variable VERSION_NUMBER](https://github.com/glcp/mci-actions-version-number/tree/v1)  | ```glcp/mci-actions-version-number@v1```        | 
| 5  | [Assemble Git Tag](https://github.com/glcp/mci-actions-version-tag/tree/v1/java)                       | ```glcp/mci-actions-version-tag/java@v1```      | 
| 6  | Generate dependency files for Docker App Build                                                         | Execute ```./build_ut.sh --ut-skip```           |
| 7* | [Build and export to Docker](https://github.com/glcp/mci-actions-docker-build-push-app/tree/v3)        | ```glcp/mci-actions-docker-build-push-app@v3``` |
| 8  | [Scan for CVE](https://github.com/glcp/jfrog-scan-cve/tree/main)                                       | ```glcp/jfrog-scan-cve@v1```                    |
| 9  | [Docker App Build](https://github.com/glcp/mci-actions-docker-build-push-app/tree/v3)                  | ```glcp/mci-actions-docker-build-push-app@v3``` |

Note on step 7: the following additional parameters are passed in:
```
docker_load: true
docker_push: false
```

#### Inputs/Secrets for build-app-maven

| _Input_        | _Default_                                          | _Description_                                         | _Required_ |
|:---------------|:---------------------------------------------------|:------------------------------------------------------|:-----------|
| appname        | ```${{ env.APP_NAME }}```                          | Application name; Usually same as the repository name | false      |
| tag            | ```${{ needs.create-tag.outputs.tag }}```          | GitHub tag                                            | false      |
| docker_load    | ```false```                                        | local build, and export to Docker                     | false      |
| docker_push    | ```true```                                         | local build, so do NOT push to registry               | false      |
| registry       | ```quay.io```                                      | Registry name                                         | true       |
| image_registry | ```quay.io/ccsportal/${{ env.APP_NAME }}```        | Quay Registry                                         | false      |
| quay_username  | ${{ secrets.CCS_QUAY_CCSPORTAL_BUILDER }}          | Quay username                                         | true       |
| quay_password  | ${{ secrets.CCS_QUAY_CCSPORTAL_BUILDER_PASSWORD }} | Quay password                                         | true       |
| jfrog_username | ${{ secrets.CCS_JFROG_USERNAME }}                  | Jfrog username                                        | false      |      
| jfrog_password | ${{ secrets.CCS_JFROG_PASSWORD }}                  | Jfrog password                                        | false      |
| target         | ci-stage                                           | Docker target                                         | false      |

### 3. build-maven-coreupdate
This job is used to update the channel versions in Coreupdate. 
The core update will be executed if the env var `SKIP_COREUPDATE_PUSH` is not `true`.

The following steps are executed in order.

|   | _Description_                          | _Actions_                                    |
|:-:|:---------------------------------------|:---------------------------------------------|
| 1 | Clone the repository                   | ```actions/checkout@v3.3.0```                |
| 2 | Set environment variables for the job. | ```glcp/mci-actions-variables-restore@v1```  |
| 3 | Channel                                | ```glcp/mci-actions-coreupdate-channel@v1``` |
| 4 | Coreupdate Push                        | ```glcp/mci-actions-coreupdate@v1.0```       |

#### Inputs/Secrets for coreupdate

| _Input_           | _Default_                                                | _Description_                                                       | _Required_ |
|:------------------|:---------------------------------------------------------|:--------------------------------------------------------------------|:-----------|
| appname           | ```${{ env.APP_NAME }}```                                | Application name in coreupdate, Usually same as the repository name | false      |
| appid             | ```${{ env.APP_ID }}```                                  | Coreupdate Application ID                                           | false      |
| tag               | ```${{ needs.build-maven-app.outputs.tag }}```           | GitHub tag                                                          | false      |
| image_registry    | ```quay.io/ccsportal/${{ env.APP_NAME }}```              | Quay registry                                                       | false      |
| channel           | ```${{ steps.channel.outputs.channel }}```               | Coreupdate channel name                                             | false      |
| UPDATECTL_USER    | ```${{ secrets.CCS_UPDATECTL_USER }}```                  | updatectl user                                                      | false      |
| UPDATECTL_SERVER  | ```${{ secrets.CCS_UPDATECTL_SERVER }}```                | updatectl server                                                    | false      |
| UPDATECTL_KEY     | ```${{ secrets.CCS_UPDATECTL_KEY }}```                   | updatectl password                                                  | false      |
| COREROLLER_USER   | ```${{ secrets.CCS_COREROLLER_USER }}```                 | coreroller user                                                     | false      |
| COREROLLER_SERVER | ```${{ secrets.CCS_COREROLLER_SERVER }}```               | coreroller server                                                   | false      |
| COREROLLER_KEY    | ```${{ secrets.CCS_COREROLLER_KEY }}```                  | coreroller password                                                 | false      |

