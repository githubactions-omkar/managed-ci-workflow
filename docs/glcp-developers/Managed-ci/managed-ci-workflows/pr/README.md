# Managed CI On PR

This workflow is triggered by pull requests (event name is `pull_request`).

These are the stages in this workflow:

1. pre-lint
2. lint
3. pre-test
4. unit-test
5. build
6. post-build
7. custom-final
8. status-checks

For language-specific details, please see the 
[Language-specific steps](../../language-specific-steps/index) section.

