# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verfication`.

Detailed requirements live in `docs/requirements.md`. Technical design lives
in `docs/design.md`.

The repository's own CI migration to `tool.py.lib.ci` 0.1.2 is complete.
Do not reintroduce CAD-CI/SCons for this library's package tests.

## 1. Complete reusable mesh geometry verification — #7

Current implementation: this branch / replacement for old PR #12.

Finish and release the geometry/mesh primitives already defined in requirements
and design:

- immutable geometry contract and surface-distance probes;
- STL loading including measurable multi-part input;
- bounds, volume, watertightness and surface-distance verification;
- `bounds_sufficient=False` guard;
- deterministic structured evidence;
- pass/fail/error handling through the existing verification report;
- built-wheel tests for every R1-R12 requirement.

After green CI:

1. merge #7 implementation;
2. verify release 0.2.0 is created from the tested main commit;
3. close #7;
4. remove this section.

## 2. Add numeric and measured-body comparison primitives — #8

Implement scalar, vector, bounds and order-independent body-envelope comparison
with deterministic evidence and no CAD-engine dependency.

Define/update requirements and design first, test the built wheel, release, then
close #8.

## 3. Add visual regression and expected-shape primitives — #9

Implement deterministic image normalization, baseline encode/decode, pixel
regression, diff evidence, generic orthographic projection, expected geometry
drawing, and goal/overlay composition.

Keep model cameras, baselines and CAD rendering consumer-owned. Test the built
wheel, release, then close #9.

## 4. Add semantic verification result composition — #10

Implement generic semantic check records, deterministic overall-status
composition, evidence/order preservation, require-pass validation, aggregate
composition and adapter support for existing verification reports.

No Forge-specific check names or CAD-CI publication behavior belong here.

## 5. Final reusable-verification audit — #4

After #7, #8, #9 and #10 are released:

- compare implementation against the historical ownership map in #4;
- confirm every reusable historical verification mechanic has moved here or has
  an explicit non-library owner;
- confirm public APIs and requirement-to-test mappings are complete;
- confirm downstream repositories only need released library versions.

Close #4 when the audit passes.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #7 Add reusable geometry and independent-reference verification primitives | now | Active implementation. The previous CI blocker is gone; complete, test through the installed wheel, release 0.2.0, then close. |
| #8 Add reusable numeric and measured-body comparison primitives | next | Required reusable comparison layer for Forge verification after #7. |
| #9 Add reusable visual regression and expected-shape overlay primitives | after #8 | Required to restore Forge visual/baseline/goal evidence generically. |
| #10 Add reusable semantic verification result composition | after #9 | Required for deterministic aggregate verification results and fan-in. |
| #4 Expand reusable CAD verification mechanics beyond the foundation | final audit | Close only after #7/#8/#9/#10 are released and the historical ownership map is fully accounted for. |

Immediate execution chain:
`#7 -> #8 -> #9 -> #10 -> #4 -> Forge #378`.
