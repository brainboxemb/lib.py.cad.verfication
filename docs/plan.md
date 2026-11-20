# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

Release `0.13.0` is complete at
`086c5370f5247562bf302c589297cc470d555e49`.

It added generic SolidCraft expectations for total body face count, full XYZ
center of mass and sketch DOF. The next Forge migration audit found one
precision issue before adoption: some existing model contracts intentionally
assert only one center-of-mass axis. Requiring all three axes would strengthen
those contracts accidentally.

## Current goal

Complete #71 and release sparse center-of-mass axis expectations as `0.13.1`.

## Required proof

- existing full XYZ center-of-mass expectations behave unchanged;
- a three-position center tuple may use `None` for omitted axes;
- at least one axis must be requested;
- omitted axes are not parsed, compared or emitted as contract evidence;
- requested malformed/missing axis evidence is a typed SolidCraft evidence
  error;
- mismatches are normal verification failures;
- complete installed-wheel CI passes;
- immutable `0.13.1` is published from the exact green main commit;
- Forge #542 consumes 0.13.1.

## Execution order

1. Define #71 behavior in requirements/design.
2. Add compatibility and sparse-axis unit tests.
3. Implement the smallest adapter refinement.
4. Release immutable `0.13.1`.
5. Resume Forge #542.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #71 Allow sparse center-of-mass axis expectations | now | Backward-compatible precision fix required before Forge #542 consumes the new center expectation. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to Forge #542. |

Immediate chain:
`#71 verification 0.13.1 -> Forge #542 next ten declarative cases`.
