# Managed CI On Manual Dev Build

This workflow is manually triggered (event name == `workflow_dispatch`).

These are the stages in this workflow:

1. check
2. pre-lint
3. lint
4. pre-test
5. unit-test
6. build
7. post-build
8. custom-final
 
For language-specific details, please see the 
[Language-specific steps](../../language-specific-steps/index) section.

