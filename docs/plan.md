# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verfication`.

## Current goal

Complete #40: allow a SolidCraft timeline expectation to declare only the
timeline fields that belong to the model contract.

This is required by the first declarative Forge consumer: simple-box checks
feature type plus error/warning state, but does not own SolidCraft's generated
feature name.

## Execution order

1. define partial timeline semantics in requirements/design;
2. add built-wheel tests;
3. implement the smallest adapter change;
4. release the library;
5. update the pending Forge runtime issue to that released version;
6. resume the simple-box consumer proof.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #40 Allow partial SolidCraft timeline expectations | now | Required to preserve simple-box's existing timeline contract without hard-coding generated SolidCraft names. |

Immediate chain:
`#40 -> release -> Forge runtime #438 -> simple-box proof`.
