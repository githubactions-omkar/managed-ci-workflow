# Managed CI On Merge

This workflow is triggered:
1. when the event name is `release` and the type is `released`
2. when there are pushes (event name is `push`) to any of these branches:<br>
   1. `main`
   2. `mainline`
   3. `master`

These are the stages in this workflow:

1. pre-lint
2. lint
3. pre-test
4. unit-test
5. build
6. post-build
7. custom-final

For language-specific details, please see the 
[Language-specific steps](../../language-specific-steps/index) section.

