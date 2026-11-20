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

Complete #53 next.

#44, #45, #51 and #52 are merged. Partial parameter/sketch contracts, count
projections and multi-body prefix groups are declarative.

#53 is the final first-batch prerequisite. It must express only stable selected
fields from large SolidCraft inspection objects, including list-object selection,
collection counts and numeric tolerances.

## Required proof

- preserve existing exact whole-result `SolidCraftInspection.expected`;
- preserve retain-only inspection behavior when no expectation is supplied;
- projected checks are data only and have stable IDs;
- paths support object keys, non-negative list indexes and an exact-one list
  selector by field/value;
- one projected check performs exactly one operation: exact value, tolerant
  numeric scalar/vector, or collection count;
- numeric tolerance supports flat numeric vectors of arbitrary finite length,
  including the 2D/3D vectors used by existing contracts;
- list selection is order-independent for keyed rows and requires exactly one
  match;
- missing/malformed requested paths are typed evidence errors; a selector count
  mismatch or value mismatch is a normal verification failure;
- raw inspection JSON remains the published artifact;
- deterministic evidence records only requested projections, not incidental raw
  fields.

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
| #53 Add projected and tolerant declarative SolidCraft inspection expectations | now | Final first-batch prerequisite; #44/#45/#51/#52 are merged. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to the qualification migration. |

Immediate chain:
`#44 -> #45 -> #51 -> #52 -> #53 -> one verification-library release -> Forge #432 batch 1`.
