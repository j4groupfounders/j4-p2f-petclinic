# p2-18-petclinic — RED
Migration: **Spring Boot 2.7.3 → 3.5.0**.
Why meaningful: Boot 2 to 3 requires Java 17, Spring 6, javax to jakarta migration and Hibernate 6; real controller/repository tests and seeded H2 app retained.
Source: https://github.com/spring-projects/spring-petclinic @ 276880edef4c3d1029865d19d6d28e982b9d4d01.
Preregistered jointly before any upgrade branch: https://github.com/j4groupfounders/j4-upgrades-harness/commit/1ce93ac5399d6b1ee6d45e716efd7da315ec20f2.
Frozen baseline SHA 36468171fb8f0493f4ff6da13892ff9e3f7c294e; CI https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37663583376.

## Verdict
Seeded detection criterion failed or seed infrastructure incomplete; no green claimed. Clean upgraded build/replay passed 40 active tests with one unchanged upstream skip and all five frozen HTTP snapshots. Seeds detected 3/5 project and 3/5 combined: missing pet name (0) and missing birth date (2) were missed by both. All five infrastructure=false. Combined 60% is below 80%, and the project miss rate was not halved. Terminal RED at nine runs; no post-hoc probes or seed changes.

Project baseline: 40 passes, 1 unchanged upstream skips. Same named inventory on accepted upgrade; no tests deleted or newly skipped.
Upgrade evidence: https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37702006943.
Seed evidence: https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37702251694.
Independent faults: project tests 3/5; combined 3/5; infrastructure-clean=True. Required >=4/5 combined AND combined miss rate <=half project miss rate. Infrastructure failures never count.
9 workflow runs (cap 12 including screening); 22.18 actual job-minutes. Seed matrix is five fresh-checkout jobs, not one shared mutation loop. Explicit bash -eo pipefail. Public standard Linux Actions only.
Zero human app/test/config edits. No paid APIs/services/model API calls or customer/upstream contact. Codex session token cost unavailable, not represented as zero measured cost.

## Migration and classified behavior
Java 17, Spring Boot 3/Hibernate 6, Jakarta persistence/validation/servlet/XML annotations, MySQL driver coordinates, Jakarta Ehcache classifier, JaCoCo, explicit Jakarta JAXB API and build-info metadata migrated. Cross-domain PetType JPQL was rewritten incorrectly as an empty DTO constructor by Spring Data 3.5; a native id/name entity query preserves the original sorted results without modifying assertions. Test assertions retained; namespace imports migrated by agent only. Surefire class-to-method reporting change for the sole unchanged disabled test is mapped exactly with a source-SHA256 guard; the baseline inventory and skip count are not changed. Maven is the verified build; alternate Gradle path is not claimed.
HTTP classification: None; HTTP snapshots identical.

## Limits and baseline repairs
See PREREG.md in the harness for fixed surfaces, immutable faults and exact baseline dependency/inventory evidence.
Unauthenticated HTTP characterization only; authenticated CRUD is covered by existing Laravel/Express tests, not a frozen differential replay. No broad route/line-coverage claim. Deliberately measured seeded sample, not production certification.
Laravel 10 destination is historical/EOL; not a supported production recommendation. Petclinic is the app used in p2-08 but a different historical major migration; its J4 source fork is detached from the GitHub network, with full source ancestry preserved.
Express baseline required inert OAuth constructor values and explicit test-mode listener. Laravel baseline required PHP 8.1 for old Carbon and removal of dev-latest advisory meta-package, not runtime/test removal; one unavailable Composer version caused an infrastructure failure. Petclinic's milestone/snapshot repositories removed; style/alternate build/database variants not part of default Maven acceptance.

## Seed outcomes
- 0: missing pet name accepted — project=False, HTTP=False, combined=False, infrastructure=False; 
- 1: missing pet type accepted — project=True, HTTP=False, combined=True, infrastructure=False; 
- 2: missing birth date accepted — project=False, HTTP=False, combined=False, infrastructure=False; 
- 3: owner first name corrupted — project=True, HTTP=True, combined=True, infrastructure=False; 
- 4: owner last name corrupted — project=True, HTTP=True, combined=True, infrastructure=False; 

## All CI runs
- https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37663173742 — j4/p2f-baseline, success, 1.63 job-min, SHA df88108085d7eab0c0d4ed270d516b2e58f35ad6.
- https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37663583376 — j4/p2f-baseline, success, 1.43 job-min, SHA 36468171fb8f0493f4ff6da13892ff9e3f7c294e.
- https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37664111094 — j4/p2f-upgrade, failure, 1.25 job-min, SHA 914448bb60ff6d15983f223de465bfed833f8dde.
- https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37664484075 — j4/p2f-upgrade, failure, 1.25 job-min, SHA a7112932aa7cc5a092638f1e865d5bc83aeaaa6c.
- https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37664943904 — j4/p2f-upgrade, failure, 2.38 job-min, SHA ceac5eec2478e412491a44f4f0a6cdac13d62016.
- https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37701278766 — j4/p2f-upgrade, failure, 1.28 job-min, SHA d2d629e082b1f05f2e59e6550a54881a8e40c4fd.
- https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37701689685 — j4/p2f-upgrade, success, 1.68 job-min, SHA 0810b0b7b68b8ffba71631677bbe4073869b7f06.
- https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37702006943 — j4/p2f-upgrade, success, 1.83 job-min, SHA e5152e49d45d96e1a1ed6a66cef3f4e5e513258c.
- https://github.com/j4groupfounders/j4-p2f-petclinic/actions/runs/37702251694 — j4/p2f-seeds, success, 9.43 job-min, SHA 38942261f9d38e9cc65cdf883351707c417fce81.

## Upgrade diff scope

.github/workflows/j4-p2f.yml                       |   7 ++
 j4-test-identity-change.json                       |   7 ++
 j4-upgrade-dependency-tree.txt                     | 116 +++++++++++++++++++++
 j4_verify.py                                       |   9 +-
 pom.xml                                            |  20 ++--
 .../samples/petclinic/model/BaseEntity.java        |   8 +-
 .../samples/petclinic/model/NamedEntity.java       |   4 +-
 .../samples/petclinic/model/Person.java            |   6 +-
 .../samples/petclinic/owner/Owner.java             |  20 ++--
 .../samples/petclinic/owner/OwnerController.java   |   2 +-
 .../samples/petclinic/owner/OwnerRepository.java   |   3 +-
 .../samples/petclinic/owner/Pet.java               |  18 ++--
 .../samples/petclinic/owner/PetController.java     |   2 +-
 .../samples/petclinic/owner/PetType.java           |   4 +-
 .../samples/petclinic/owner/Visit.java             |   8 +-
 .../samples/petclinic/owner/VisitController.java   |   2 +-
 .../samples/petclinic/vet/Specialty.java           |   4 +-
 .../springframework/samples/petclinic/vet/Vet.java |  14 +--
 .../samples/petclinic/vet/Vets.java                |   4 +-
 .../samples/petclinic/model/ValidatorTests.java    |   4 +-
 20 files changed, 203 insertions(+), 59 deletions(-)
