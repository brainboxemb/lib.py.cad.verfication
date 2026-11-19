# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verfication`.

Detailed requirements live in `docs/requirements.md`. Technical design lives
in `docs/design.md`.

The repository's own CI migration is complete. Mesh geometry (#7), numeric /
measured-body comparison (#8), and visual verification (#9) are released.

## 1. Add semantic verification result composition — #10

Current implementation: this branch.

Complete and release:

- immutable consumer-supplied semantic checks;
- generic status validation;
- deterministic required-check precedence;
- evidence/order preservation;
- require-pass validation with typed failure evidence;
- aggregate composition of already-produced item results;
- adapter from existing verification reports;
- no consumer-domain check names;
- no CAD-CI/publication/materialization behavior;
- built-wheel tests for issue #10 R1-R8.

After green CI:

1. merge the implementation;
2. verify release 0.5.0 comes from the tested main commit;
3. close #10;
4. remove this section.

## 2. Final reusable-verification audit — #4

After #10 is released:

- compare implementation against the complete historical ownership map in #4;
- confirm every reusable historical verification mechanic has moved here or has
  an explicit non-library owner;
- confirm all public APIs and requirement-to-test mappings are complete;
- confirm downstream repositories only need released library versions;
- close any obsolete foundation/release issues that remain open.

Close #4 when the audit passes.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #10 Add reusable semantic verification result composition | now | Active implementation. Complete, test through the installed wheel, release 0.5.0, then close. |
| #4 Expand reusable CAD verification mechanics beyond the foundation | final audit | Run after #10 release; reconcile the historical ownership map and remaining open issues before Forge consumes the library. |

Immediate execution chain:
`#10 -> #4 -> Forge #378`.
