# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verfication`.

Detailed requirements live in `docs/requirements.md`. Technical design lives
in `docs/design.md`.

## Current status

The reusable verification library is functionally complete for the current
Forge migration and released as:

- 0.2.0 — mesh geometry verification (#7);
- 0.3.0 — numeric and measured-body comparison (#8);
- 0.4.0 — visual regression and expected-shape primitives (#9);
- 0.5.0 — semantic result composition (#10).

Repository CI uses the externally tested `tool.py.lib.ci` path. Do not
reintroduce repository-local CAD-CI/SCons package-test infrastructure.

## Current work: final migration audit — #4

No new reusable implementation is currently required here.

Issue #4 remains open as the completeness audit and is blocked on Forge #378,
because its completion rule requires Forge to:

- consume released library versions;
- migrate the corresponding consumer-owned verification behavior;
- leave no reusable mechanics stranded in Forge solely because library
  extraction was skipped.

During Forge #378, return here only if a genuinely reusable mechanic from the
historical ownership map is still missing. Add it through a focused requirement,
design, test and release before Forge consumes it.

After Forge #378 is complete:

1. compare the final Forge ownership against the historical map in #4;
2. confirm all generic mechanics are provided by released library APIs;
3. confirm model/tool-specific policy remains consumer-owned;
4. confirm no CAD-CI/publication behavior entered this library;
5. close #4 when the audit passes.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #4 Expand reusable CAD verification mechanics beyond the foundation | blocked on Forge #378 / final audit | #7/#8/#9/#10 are implemented, tested and released. Completion now depends on Forge consuming the released APIs and the final ownership-map audit. |

Immediate execution chain:
`Forge #378 -> verification-library #4 final audit -> Forge #366`.
