# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verfication`.

Detailed requirements live in `docs/requirements.md`. Technical design lives
in `docs/design.md`.

## Current status

Released verification layers:

- 0.2.0 — mesh geometry verification (#7);
- 0.3.0 — numeric and measured-body comparison (#8);
- 0.4.0 — visual regression and expected-shape primitives (#9);
- 0.5.0 — semantic result composition (#10);
- 0.6.0 — generic single-view visual verification orchestration (#26);
- 0.7.0 — exact-value and predicate verification helpers (#29).

Release 0.7.0 is published at exact commit
`a7b2eede634508d3c04a115a201ea91b9d0e2714`.

The earlier migration audit issue #4 is closed. Forge #432 exposed one remaining
ownership error: shared SolidCraft verification knowledge is still present in
Forge.

## Current work: SolidCraft verification ownership — #32

Goal: keep model-specific verification data in Forge, while moving the shared
knowledge of how that data is checked against SolidCraft into this library.

Execution order:

1. update AGENTS/requirements/design for the corrected ownership boundary;
2. define the smallest public SolidCraft verification API required by current
   Forge model verification;
3. add direct built-wheel tests for valid and malformed SolidCraft evidence;
4. implement SolidCraft parsing/checking here without Forge model knowledge;
5. release the library;
6. update Forge #432 to pass model-specific expectations to the released API
   and delete its local shared SolidCraft verification code;
7. audit Forge again for remaining shared checker knowledge.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #32 Own SolidCraft verification adapters in the CAD verification library | now | Required before Forge #432 can continue with the correct ownership boundary. |

Immediate execution chain:
`verification-library #32 -> release -> Forge #432 -> Forge #430`.
