# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verfication`.

Detailed requirements live in `docs/requirements.md`. Technical design lives
in `docs/design.md`.

## Current status

Released reusable verification layers:

- 0.2.0 — mesh geometry verification (#7);
- 0.3.0 — numeric and measured-body comparison (#8);
- 0.4.0 — visual regression and expected-shape primitives (#9);
- 0.5.0 — semantic result composition (#10);
- 0.6.0 — generic single-view visual verification orchestration (#26).

Release 0.6.0 is published at exact commit
`649d22cbcd828952f903b7ed29e6b63b41654c38`.

The continuing Forge #378 ownership audit found one additional generic helper
pair repeated across the consumer model verifiers. That work is #29.

## Current work: exact-value and predicate requirements — #29

Implement two engine-neutral helpers:

- exact expected/actual equality;
- one explicit boolean condition with caller-supplied expected/actual evidence.

Execution order:

1. define stable evidence and failure semantics in requirements/design;
2. add direct built-wheel tests;
3. implement/export/document the helpers;
4. release 0.7.0 only after library CI is green;
5. update Forge #432 to consume the released helpers and remove its local
   `require_equal` / `require_true` copies;
6. update the immutable Forge runtime once to the final audit library release.

## Final migration audit — #4

#4 remains open while Forge #378 consumes released library APIs.

After #29 is released and consumed:

1. finish Forge #432;
2. update Forge runtime to the new library release;
3. resume Forge #430 visual verification;
4. complete visual/diagram/summary migration;
5. return here for the final ownership-map audit.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #29 Add generic exact-value and predicate verification helpers | now | Generic failure/evidence mechanics are still duplicated in all Forge model verifiers. Implement, test and release before #432 closes. |
| #4 Expand reusable CAD verification mechanics beyond the foundation | blocked on #29 and Forge #378 / final audit | #7/#8/#9/#10/#26 are released. Final closure depends on #29 plus complete Forge consumption and ownership audit. |

Immediate execution chain:
`verification-library #29 -> Forge #432 -> Forge runtime update -> Forge #430 -> Forge #378 remainder -> verification-library #4 final audit -> Forge #366`.
