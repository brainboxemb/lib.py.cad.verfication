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
- 0.5.0 — semantic result composition (#10).

The Forge #378 ownership audit found one generic visual mechanic still missing:
single-view orchestration that combines the already released visual primitives.
That work is #26.

Repository CI uses the externally tested `tool.py.lib.ci` path. Do not
reintroduce CAD-CI/SCons package-test infrastructure here.

## Current work: reusable visual view verification — #26

Implement one engine-neutral function for one already-rendered visual view.

Execution order:

1. define observable behavior in requirements and exact semantics in design;
2. add direct tests for pass, mismatch, missing baseline and expected-shape
   evidence;
3. implement the function only from existing generic visual primitives;
4. export and document the public API;
5. release 0.6.0 after library CI is green;
6. only then resume Forge #430 against the exact released library revision.

## Final migration audit — #4

#4 remains open until Forge #378 is complete.

After #26 is released and Forge consumes it, continue the final audit:

1. confirm generic numeric/bounds comparison math is no longer duplicated in
   Forge model verifiers;
2. confirm reference selection/render adapters remain consumer-owned;
3. confirm visual rendering/camera/view/baseline policy remains consumer-owned;
4. confirm no reusable verification mechanics remain stranded in Forge;
5. close #4 only after #378 completes and the ownership map passes.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #26 Add generic single-view visual verification orchestration | now | Missing reusable mechanic discovered by Forge #430. Must be designed, directly tested and released before Forge visual work resumes. |
| #4 Expand reusable CAD verification mechanics beyond the foundation | blocked on #26 and Forge #378 / final audit | Existing #7/#8/#9/#10 releases cover the original primitives. #26 fills one orchestration gap found during consumer adoption; final closure still depends on Forge #378. |

Immediate execution chain:
`verification-library #26 -> release 0.6.0 -> Forge #430 -> Forge #432 boundary cleanup -> Forge #378 remainder -> verification-library #4 final audit`.
