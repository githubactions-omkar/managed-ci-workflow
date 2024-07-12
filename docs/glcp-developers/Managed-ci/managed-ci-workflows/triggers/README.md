# Triggers

The Workflow has 3 Triggers which are **workflow_dispatch** to enable developers to execute the workflow in feature branches, **pull_request** to enable the workflow to get triggered when a PR is opened, **push** to enable the workflow to trigger on merge to deafult_branch or when a release tag is created.

**workflow_dispatch:**  To enable the teams make use of the Managed CI workflow in feature/non-default branches for manual CI

**pull_request:**       To trigger the Managed CI workflow when a PR is opened, updated.

**push:**               [branch: main, master, mainline]: To Trigger the Managed CI workfow when PR is merged to default branch.<br>[tags: [0-9]+.[0-9]+.[0-9]+]: To Trigger the Managed CI workfow when a tag is created for the release |
