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
- 0.6.0 — generic single-view visual verification orchestration (#26);
- 0.7.0 — exact-value and predicate verification helpers (#29).

Release 0.7.0 is published at exact commit
`a7b2eede634508d3c04a115a201ea91b9d0e2714`.

No additional reusable implementation is currently known to be missing.

## Current work: final migration audit — #4

Forge #378 is consuming the released APIs and removing generic verification
mechanics that remained in consumer code.

Current execution chain:

1. Forge #434 publishes an immutable runtime containing library 0.7.0.
2. Forge #432 finishes replacing local comparison/equality/predicate helpers
   with released library APIs.
3. Forge #430 resumes visual verification using released
   `verify_visual_view()`.
4. Forge completes visual expansion, diagrams and the final verification
   summary.
5. Return here for the final ownership-map audit.

Final closure of #4 requires confirming that Forge retains only consumer-owned
behavior:

- SolidCraft/CAD-engine command adapters and measurement-schema parsing;
- model-specific expected geometry, parameters, history and mutations;
- reference source selection/execution;
- camera/view/baseline/model policy;
- diagram and publication behavior.

Generic comparisons, evidence/failure mechanics, mesh verification, visual
verification and semantic composition must come from this library.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #4 Expand reusable CAD verification mechanics beyond the foundation | blocked on Forge #378 / final audit | #7/#8/#9/#10/#26/#29 are implemented, directly tested and released. Closure depends only on complete Forge consumption and the final ownership audit. |

Immediate execution chain:
`Forge #434 -> Forge #432 -> Forge #430 -> Forge #378 remainder -> verification-library #4 final audit -> Forge #366`.
