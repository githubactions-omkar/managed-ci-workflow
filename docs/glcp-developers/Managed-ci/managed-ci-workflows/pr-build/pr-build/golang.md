# Build on PR for Golang

When the [repository variable](../../on-boarding/index.html#repository-variables) 
`GLCP_BUILD_SYSTEM` is set to `golang`, the jobs 
[set-matrix-variables](#set-matrix-variables) and [build-golang](#build-golang) 
are executed to do a sanity build for Go-based repositories.

### 1. set-matrix-variables
Creates a JSON object for the matrix strategy that is used 
by [build-golang](#build-golang) job

```yaml
  set-matrix-variables:
    if: |
      vars.GLCP_BUILD_SYSTEM == 'golang' && 
      (github.event_name == 'pull_request' && 
       contains(fromJSON('["opened", "reopened", "synchronize"]'), github.event.action))
    needs: checks-done
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3.3.0

      - uses: glcp/mci-actions-variables-restore@v1
        with:
          use-artifact: false

      - id: set-matrix
        run: |
          echo "matrix=$(yq -I=0 -o=json '{"include": .PRODUCTS}' .github/mci-variables.yaml)" >> $GITHUB_OUTPUT
          echo "$(yq -I=0 -o=json '{"include": .PRODUCTS}' .github/mci-variables.yaml | jq)"
```

### 2. build-golang
This job is used for the app build.  The following are the steps for this job:

|    | _description_                                                                                          | _actions_                                       |
|:--:|:-------------------------------------------------------------------------------------------------------|:------------------------------------------------| 
| 1  | [Checkout source code](https://github.com/actions/checkout/tree/v3.3.0)                                | ```actions/checkout@v3.3.0```                   | 
| 2  | [Set environment variables for the job](https://github.com/glcp/mci-actions-variables-restore/tree/v1) | ```glcp/mci-actions-variables-restore@v1```     |
| 3  | [Login to Docker registries](https://github.com/glcp/mci-actions-registry-login/tree/v1)               | ```glcp/mci-actions-registry-login@v1```        |
| 4* | [Build and export to Docker](https://github.com/glcp/mci-actions-docker-build-push-app/tree/v3)        | ```glcp/mci-actions-docker-build-push-app@v3``` | 
| 5  | [Scan for CVE](https://github.com/glcp/jfrog-scan-cve/tree/main)                                       | ```glcp/jfrog-scan-cve@v1```                    |

Note on step 4: the following additional parameters are passed in:
```
docker_load: true
docker_push: false
```

Inputs/Secrets for `build-golang` job:

| _Input_         | _Default_                                                | _Description_                                                       | _Required_ |
|:----------------|:---------------------------------------------------------|:--------------------------------------------------------------------|:-----------|
| appname         | ```${{ env.APP_NAME }}```                                | Application name in coreupdate, Usually same as the repository name | false      |
| appid           | ```${{ env.APP_ID }}```                                  | Coreupdate Application ID                                           | false      |
| docker_load     | ```false```                                              | local build, and export to Docker                                   | false      |
| docker_push     | ```true```                                               | local build, so do NOT push to registry                             | false      |
| dockerfile_path | ```${{ matrix.DOCKERFILE_PATH }}```                      | Obtained from matrix                                                | false      |
| registry        | ```quay.io```                                            | Registry name                                                       | true       |
| image_registry  | ```${{ matrix.IMAGE_REGISTRY }}```                       | Quay registry; obtained from matrix                                 | false      |
| tag             | ```ci-image${{ matrix.TAG_EXTENSION }}```                | Arbitrary/fake value                                                | false      |
| target          | ```${{ matrix.TARGET }}```                               | Docker target; obtained from matrix                                 | false      |
| quay_username   | ```${{ secrets.CCS_QUAY_CCSPORTAL_BUILDER }}```          | Quay Username                                                       | true       |
| quay_password   | ```${{ secrets.CCS_QUAY_CCSPORTAL_BUILDER_PASSWORD }}``` | Quay Password                                                       | true       |
| jfrog_username  | ```${{ secrets.CCS_JFROG_USERNAME }}```                  | JFROG Username                                                      | false      |
| jfrog_password  | ```${{ secrets.CCS_JFROG_PASSWORD }}```                  | JFROG password                                                      | false      |
| gh_token        | ```${{ secrets.GLCP_GH_TOKEN }}```                       | Github Token                                                        | false      |

