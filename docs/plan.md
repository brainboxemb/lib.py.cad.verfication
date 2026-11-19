# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verfication`.

Detailed requirements live in `docs/requirements.md`. Technical design lives
in `docs/design.md`.

The repository's own CI migration is complete, and reusable mesh geometry
verification (#7) is merged. Do not reintroduce repository-local CAD-CI/SCons
package-test infrastructure.

## 1. Add numeric and measured-body comparison primitives — #8

Current implementation: this branch.

Complete and release:

- scalar comparison;
- vector comparison;
- XYZ bounds comparison;
- immutable measured-body envelopes;
- order-independent one-to-one envelope matching;
- deterministic structured evidence;
- `VerificationFailure` integration through `verify()`;
- explicit rejection of invalid/non-finite numeric input and negative tolerance;
- no CAD-engine imports in the comparison module;
- built-wheel tests for issue #8 R1-R6.

After green CI:

1. merge the implementation;
2. verify release 0.3.0 comes from the tested main commit;
3. close #8;
4. remove this section.

## 2. Add visual regression and expected-shape primitives — #9

Implement deterministic image normalization, baseline encode/decode, pixel
regression, diff evidence, generic orthographic projection, expected geometry
drawing, and goal/overlay composition.

Keep model cameras, baselines and CAD rendering consumer-owned. Test the built
wheel, release, then close #9.

## 3. Add semantic verification result composition — #10

Implement generic semantic check records, deterministic overall-status
composition, evidence/order preservation, require-pass validation, aggregate
composition and adapter support for existing verification reports.

No Forge-specific check names or CAD-CI publication behavior belong here.

## 4. Final reusable-verification audit — #4

After #8, #9 and #10 are released:

- compare implementation against the historical ownership map in #4;
- confirm every reusable historical verification mechanic has moved here or has
  an explicit non-library owner;
- confirm public APIs and requirement-to-test mappings are complete;
- confirm downstream repositories only need released library versions.

Close #4 when the audit passes.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #8 Add reusable numeric and measured-body comparison primitives | now | Active implementation. Complete, test through the installed wheel, release 0.3.0, then close. |
| #9 Add reusable visual regression and expected-shape overlay primitives | next | Required to restore Forge visual/baseline/goal evidence generically. |
| #10 Add reusable semantic verification result composition | after #9 | Required for deterministic aggregate verification results and fan-in. |
| #4 Expand reusable CAD verification mechanics beyond the foundation | final audit | Close only after #8/#9/#10 are released and the historical ownership map is fully accounted for. |

Immediate execution chain:
`#8 -> #9 -> #10 -> #4 -> Forge #378`.
