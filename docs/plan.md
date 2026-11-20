# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

Release `0.13.1` is complete at
`3600fa6145f11d05d6f27a342df0c24e075905eb`.

Forge #543 has proven the next ten declarative Qualification cases against that
release. Only `sketch-pattern-mirror` remains procedural.

Its remaining contract is generic but relational: after one saved-design
mutation, a numeric measurement must differ from the baseline by more than a
configured threshold. Forge must not own that comparison mechanic.

## Current goal

Complete #73 and release saved-design numeric change expectations as `0.14.0`.

## Required proof

- a saved design may request one or more numeric baseline-to-mutated changes by
  JSON measurement path;
- paths use object keys and non-negative list indexes only;
- baseline measurements reuse the baseline artifact already produced in the
  same verification run;
- baseline is not re-evaluated;
- resolved values are finite numbers;
- pass condition is strictly absolute delta greater than the configured minimum;
- malformed path/value evidence is a typed SolidCraft evidence error;
- insufficient delta is a normal verification failure;
- saved designs without change expectations behave unchanged;
- installed-wheel CI passes;
- immutable `0.14.0` is published from the exact green main commit;
- Forge then migrates its final procedural case.

## Execution order

1. Define #73 behavior in requirements/design.
2. Add adapter tests for configuration, pass/fail and malformed evidence.
3. Implement the smallest saved-design relation.
4. Release immutable `0.14.0`.
5. Migrate Forge `sketch-pattern-mirror`.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #73 Support saved-design numeric change expectations | now | Final generic prerequisite for the last Forge procedural Qualification case. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to the final Forge migration. |

Immediate chain:
`#73 verification 0.14.0 -> final Forge procedural case -> Pages coverage work`.
