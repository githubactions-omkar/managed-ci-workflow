To update the documentation, make changes in
[managed-ci-workflow](https://github.com/glcp/managed-ci-workflow/blob/main/docs)

# Changelog

* [Version 1.6.0](#version-1-6-0)
* [Version 1.5.0](#version-1-5-0)
* [Version 1.4.2](#version-1-4-2)
* [Version 1.4.1](#version-1-4-1)
* [Version 1.4.0](#version-1-4-0)
* [Version 1.3.2](#version-1-3-2)
* [Version 1.3.1](#version-1-3-1)
* [Version 1.3](#version-1-3)

## Version 1.6.1
Date: Feb 28, 2024
* Enable FT for dependabot
  ([#1007](https://github.com/glcp/managed-ci-workflow/pull/1007))
* Remote deploy repository support + workaround for GitHub issue 2205
  ([#1002](https://github.com/glcp/managed-ci-workflow/pull/1002))
* Remove OWASP dependency check
  ([#991](https://github.com/glcp/managed-ci-workflow/pull/991))
* SBOM
  * Documentation
    ([#1008](https://github.com/glcp/managed-ci-workflow/pull/1008))
  * Bugfix: Search
    ([#1006](https://github.com/glcp/managed-ci-workflow/pull/1006))
  * Bugfix: MCI sign and sbom skipped if vtn is not configured.
    ([#996](https://github.com/glcp/managed-ci-workflow/pull/996))
* OnPrem
  * Added feature
    ([#977](https://github.com/glcp/managed-ci-workflow/pull/977))
  * Format fix
    ([#1010](https://github.com/glcp/managed-ci-workflow/pull/1010))
  * Documentation
    ([#997](https://github.com/glcp/managed-ci-workflow/pull/997))
* Bugs
  * Add hpe_product_type "internal" for vtn product.
    ([#985](https://github.com/glcp/managed-ci-workflow/pull/985))
  * Fix for golang ft version
    ([#982](https://github.com/glcp/managed-ci-workflow/pull/982))

## Version 1.6.0
Date: TBD
* Integrate CVE scans with Managed-CI to block PR
  ([#823](https://github.com/glcp/managed-ci-workflow/pull/823))
* Deployer
  * Adding optional workflow for schedule (GLCP-159505)
    ([978](https://github.com/glcp/managed-ci-workflow/pull/978))

## Version 1.5.0
Date: Dec 18, 2023
* Split FT/PR workflow into 3: triggered by PR review, label, or PR creation
  ([#808](https://github.com/glcp/managed-ci-workflow/pull/808))
* Update lint workflow to fail only when new if linting fails on new code
  ([#807](https://github.com/glcp/managed-ci-workflow/pull/807))
* Add Maven/Java support to FT workflow
  ([#805](https://github.com/glcp/managed-ci-workflow/pull/805))
* Allow custom stage to be run at the end of MCI
  ([#752](https://github.com/glcp/managed-ci-workflow/pull/752))
* Enable lint exclude regex for super linter
  ([#747](https://github.com/glcp/managed-ci-workflow/pull/747))
* Enable MCI triggering after synchronization of external repo
  ([#730](https://github.com/glcp/managed-ci-workflow/pull/730))

## Version 1.4.2
Date: Nov 14, 2023
* Fix lint errors due to cache issues
  ([#753](https://github.com/glcp/managed-ci-workflow/pull/753))

## Version 1.4.1
Date: Nov 2, 2023
* MCI deployer needs to delete MCI workflows during upgrades 
  ([#727](https://github.com/glcp/managed-ci-workflow/pull/727))
* Fixed the issue with the JIRA UPDATE in python build
* Added exclude regex for Linting in script build
* Updated dependabot condition to skip MCI on PR from `github.actor` to 
  `github.event.pull_request.user.login`

## Version 1.4.0
Date: Oct 18, 2023
* MCI workflow parallelization and Matrix Build for Go and Python 
  ([#669](https://github.com/glcp/managed-ci-workflow/pull/669))
* Build on PR for Java ([#655](https://github.com/glcp/managed-ci-workflow/pull/655))
* Update FT on PR documentation ([#674](https://github.com/glcp/managed-ci-workflow/pull/674))
* Documentation: Rearrange contents and various cleanup 
  ([#670](https://github.com/glcp/managed-ci-workflow/pull/670),
   [#656](https://github.com/glcp/managed-ci-workflow/pull/656))

## Version 1.3.2
Date: Oct 4, 2023
* SonarScan execution fails for the dependabot user in the PR workflow 
  ([#657](https://github.com/glcp/managed-ci-workflow/pull/657))
* Add lint to manual-build.yaml ([#647](https://github.com/glcp/managed-ci-workflow/pull/647))

## Version 1.3.1
Date: Sep 27, 2023
* Refactor FT conditions and check jobs 
  ([#630](https://github.com/glcp/managed-ci-workflow/pull/630))

## Version 1.3 
Date: Aug 29, 2023
* Support Terraform ([#592](https://github.com/glcp/managed-ci-workflow/pull/592),
  [#591](https://github.com/glcp/managed-ci-workflow/pull/591))
* Build on PR for Go and Python ([#590](https://github.com/glcp/managed-ci-workflow/pull/590))
* Support Java Use Cases for CCS in MCI
  ([#587](https://github.com/glcp/managed-ci-workflow/pull/587))
* Scheduled linting ([#550](https://github.com/glcp/org-policies/pull/550))
* Documentation: Add code coverage and rearrange contents
  ([#618](https://github.com/glcp/managed-ci-workflow/pull/618))

