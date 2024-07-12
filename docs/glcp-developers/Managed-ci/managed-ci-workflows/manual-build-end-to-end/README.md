# End-to-End Managed CI On Manual Dev Build

This workflow is triggered by 
[glcp-github-mirroring](https://github.com/glcp/glcp-github-mirroring)
when an external repo has a new release, and the repo variable `END_TO_END_WF` is set
to the string `true` at https://github.com/glcp/&lt;repo-name&gt;.

These are the stages in this workflow:

1. check 

    * secret scan
    * malware scan

2. pre-lint
3. lint
4. pre-test
5. unit-test
6. build (specific to each external repo)
7. post-build
8. custom-final
    
For language-specific details, please see the 
[Language-specific steps](../../language-specific-steps/index) section.

