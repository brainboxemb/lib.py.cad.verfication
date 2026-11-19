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

Repository CI uses the externally tested `tool.py.lib.ci` path. Do not
reintroduce CAD-CI/SCons package-test infrastructure here.

## Current work: final migration audit — #4

No additional reusable implementation is currently known to be missing.

Forge #378 is still consuming the released library APIs and removing generic
verification mechanics that remained in consumer code.

The current audit chain is:

1. Forge #432 replaces duplicated numeric/vector/bounds comparison math with the
   released 0.3.0+ APIs;
2. Forge updates its immutable runtime to library 0.6.0;
3. Forge #430 resumes visual verification using released
   `verify_visual_view()`;
4. Forge completes the remaining visual/diagram/summary migration;
5. return here for the final ownership-map audit.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #4 Expand reusable CAD verification mechanics beyond the foundation | blocked on Forge #378 / final audit | #7/#8/#9/#10/#26 are implemented, directly tested and released. Closure now depends on Forge consuming the APIs and proving no reusable mechanics remain stranded there. |

Immediate execution chain:
`Forge #432 -> Forge runtime 0.6.0 -> Forge #430 -> Forge #378 remainder -> verification-library #4 final audit -> Forge #366`.
