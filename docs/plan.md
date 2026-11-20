# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

Release `0.12.0` is complete and is already consumed by Forge through the
released CAD verification wheel dependency.

Forge #542 is the next declarative migration batch. Its procedural contracts
expose three remaining reusable SolidCraft expectation fields that are not yet
represented declaratively:

- total body face count;
- body center of mass with tolerance;
- sketch degrees of freedom (DOF).

These are generic SolidCraft result checks and therefore belong in this library,
not in Forge.

## Current goal

Complete #69 and release the new expectation fields as `0.13.0`.

## Required proof

- `SolidCraftBodyExpectation` supports optional total face count and
  center-of-mass + tolerance;
- `SolidCraftSketchExpectation` supports optional DOF;
- omitted fields remain completely unchecked;
- requested malformed/missing evidence is a typed SolidCraft evidence error;
- value mismatches are normal verification failures;
- deterministic evidence contains only requested fields;
- complete source and installed-wheel CI passes;
- immutable `0.13.0` is published from the exact green release commit;
- Forge #542 consumes the released version before migrating its ten cases.

## Execution order

1. Define #69 behavior in requirements/design.
2. Add adapter unit tests for configuration, pass, mismatch and malformed
   evidence.
3. Implement the smallest adapter change.
4. Release immutable `0.13.0`.
5. Resume Forge #542.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #69 Support body center/face-count and sketch DOF expectations | now | Generic prerequisite for Forge #542; implement/test/release as 0.13.0. |
| #63 Update repository plan after verification 0.11.0 release | probably obsolete | Superseded by later 0.12.0 state and this current plan refresh. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to Forge #542. |

Immediate chain:
`#69 verification 0.13.0 -> Forge #542 next ten declarative cases`.
