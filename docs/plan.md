# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

Release `0.10.1` is complete. It preserves the public verification API while
lazy-loading geometry and visual implementation modules for SolidCraft-only
consumers.

Forge's five-case staged proof is complete. The next Forge #432 migration batch
contains ten existing Qualification cases whose procedural contracts expose the
remaining reusable SolidCraft semantics needed before the broader catalog can
move to data-only `verification/verify.py`.

The required generic prerequisite set is now explicit:

- #44 — partial parameter expectations;
- #45 — partial sketch expectations;
- #51 — declarative count expectations for model/body evidence;
- #52 — multiple bodies sharing one name prefix;
- #53 — projected/tolerant inspection expectations.

These are existing consumer contracts, not speculative API expansion.

## Current goal

Complete #60 and release the merged first-batch prerequisite set as 0.11.0.

The release contains no new behavior beyond already merged #44, #45, #51, #52
and #53. It exists to make that complete generic contract available as one
immutable downstream dependency.

## Required proof

- VERSION and pyproject.toml declare 0.11.0;
- CHANGELOG documents the merged generic behavior;
- complete installed-wheel CI passes;
- main publishes immutable v0.11.0 from the exact green release commit;
- #44/#45/#51/#52/#53 close as released;
- docker.cad.solidcraft pin adoption happens in its own repository.

## Execution order

1. Prepare 0.11.0 release metadata only.
2. Run complete library CI.
3. Merge and verify immutable v0.11.0 publication.
4. Close the released prerequisite issues.
5. Update docker.cad.solidcraft to the exact 0.11.0 commit in its own PR.
6. Resume Forge #432 batch 1.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #60 Release SolidCraft declarative prerequisite set as 0.11.0 | now | All five prerequisite behaviors are merged and green; publish them once as the immutable downstream contract. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to the qualification migration. |

Immediate chain:
`#60 release 0.11.0 -> runtime pin -> Forge #432 batch 1`.
