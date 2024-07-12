# README
This repo contains the Documentation and references for ![Managed CI](https://github.com/glcp/managed-ci-workflow).

## Generating the documentation
1. **Make sure to update the ![Changelog](https://github.com/glcp/managed-ci-workflow/blob/main/docs/glcp-developers/change-log/README.md) to 
    include the pull request number**
2. Create and push the tag with format: `v<digit(s)>.<digit(s)>.<digit(s)>`<br>
    Example: `v1.3.0`
3. Verify that the ![Build Github Pages](https://github.com/glcp/managed-ci-workflow/actions/workflows/gh-pages.yaml) 
   workflow to generate the documentation was triggered automatically
4. Verify that the ![pages-build-deployment](https://github.com/glcp/managed-ci-workflow/actions/workflows/pages/pages-build-deployment)
   workflow was triggered successfully
5. View updated documentation at https://mci-doc.glcp.hpedev.net/

The tag with the highest version number will be the default version of the 
documentation when visiting https://mci-doc.glcp.hpedev.net/

## Generating the documentation locally
1. Create local tag in the workspace.  Example: `git tag v9.9.9`
2. Run the ![local-build.sh](https://github.com/glcp/managed-ci-workflow/blob/main/docs-creation/local-build.sh) 
   script in the `docs-creation` directory:
   ```
   cd <Git-workspace>/docs-creation
   ./local-build.sh
   ```
3. The generated documentation will be in `<Git-workspace>/docs-creation/_build/html` directory
4. Start up a simple web server to view the docs:
   1. run: `cd <Git-workspace>/docs-creation/_build/html`
   2. run: `python3 -m http.server 8888` (change port `8888` if required)
   3. view the docs at http://localhost:8888 (change port number accordingly)

The tag with the highest version number will be the default version of the 
documentation when visiting http://localhost:8888

## Updating the configuration
The `smv_tag_whitelist` setting in the ![conf.py](https://github.com/glcp/managed-ci-workflow/blob/main/docs-creation/conf.py) 
file controls which tags to include when generating the documentation.  It is currently 
set to include only tags that start with `v` with the `v<digit(s)>.<digit(s)>.<digit(s)>` 
format:

`smv_tag_whitelist = r'^v\d+\.\d+\.\d+$'`

The ![Build Github Pages](https://github.com/glcp/managed-ci-workflow/actions/workflows/gh-pages.yaml)
workflow is configured to trigger only when tags matching the
`v<digit(s)>.<digit(s)>.<digit(s)>` format are pushed.

Update the regex in ![conf.py](https://github.com/glcp/managed-ci-workflow/blob/main/docs-creation/conf.py)
and ![Build Github Pages](https://github.com/glcp/managed-ci-workflow/blob/main/.github/workflows/gh-pages.yaml) 
if other tags should be included.

