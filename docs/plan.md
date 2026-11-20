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

Complete #52 next.

#44, #45 and #51 are merged. Partial parameter/sketch contracts and the required
count projections are now declarative.

#52 preserves existing contracts that identify several occurrence bodies by one
shared SolidCraft name prefix while also checking their order-independent
geometry.

## Required proof

- add a dedicated generic body-group expectation; do not change the existing
  exact-one `SolidCraftBodyExpectation` selector;
- group selection uses the caller-supplied `name_prefix`;
- group count is explicit and exact;
- optional expected body envelopes are order-independent and use existing bounds
  tolerance semantics;
- configured envelope count must agree with configured group count;
- deterministic evidence preserves matched body names plus requested count and
  geometry comparison;
- malformed body/name/bounds evidence remains typed;
- existing single-body expectations remain unchanged.

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
| #52 Allow declarative expectations for multiple SolidCraft bodies sharing a name prefix | now | #44/#45/#51 are merged; required for existing Block*/Marker* identity + geometry contracts. |
| #53 Add projected and tolerant declarative SolidCraft inspection expectations | next | Required for sheet flat-pattern and BOM/component inspections without comparing incidental raw fields. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to the qualification migration. |

Immediate chain:
`#44 -> #45 -> #51 -> #52 -> #53 -> one verification-library release -> Forge #432 batch 1`.
