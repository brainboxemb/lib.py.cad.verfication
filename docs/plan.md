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

Complete #45 next.

#44 is merged and preserves exact parameter matching while adding explicit
subset mode.

#45 makes `SolidCraftSketchExpectation` fields independently optional so a
consumer can preserve an existing contract such as “the named sketch is solved”
without inventing profile/curve counts.

## Required proof

- sketch name remains the strict selector;
- `profiles`, `curves` and `status` are independently optional;
- at least one of those properties must be requested;
- only requested fields are required/read/compared;
- expected/actual evidence contains only the requested fields plus selector name;
- duplicate/missing named sketch selection remains a normal verification failure;
- malformed requested fields remain `SolidCraftEvidenceError`;
- existing full sketch expectations remain unchanged.

## Execution order

1. #44 partial parameters.
2. #45 partial sketches.
3. #51 declarative count expectations.
4. #52 body-prefix groups.
5. #53 projected/tolerant inspections.
6. Run the complete installed-wheel verification suite.
7. Release the complete prerequisite set once as the next feature release.
8. Update `docker.cad.solidcraft` only if that immutable runtime owns the
   verification-library pin.
9. Resume the first ~10-case Forge #432 batch.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #45 Allow partial SolidCraft sketch expectations | now | Required by cases that care about named sketch status but not incidental profile/curve counts; #44 is merged. |
| #51 Add declarative SolidCraft count expectations for measured model/body evidence | next | Required for existing face-type, total sketch and timeline-type count contracts. |
| #52 Allow declarative expectations for multiple SolidCraft bodies sharing a name prefix | next | Required to preserve existing occurrence/body identity contracts without replacing them by geometry-only checks. |
| #53 Add projected and tolerant declarative SolidCraft inspection expectations | next | Required for sheet flat-pattern and BOM/component inspections without comparing incidental raw fields. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to the qualification migration. |

Immediate chain:
`#44 -> #45 -> #51 -> #52 -> #53 -> one verification-library release -> Forge #432 batch 1`.
