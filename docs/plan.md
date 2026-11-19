# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verfication`.

Detailed requirements live in `docs/requirements.md`. Technical design lives
in `docs/design.md`.

The repository's own CI migration is complete. Mesh geometry (#7) and numeric /
measured-body comparison (#8) are released. Do not reintroduce repository-local
CAD-CI/SCons package-test infrastructure.

## 1. Add visual regression and expected-shape primitives — #9

Current implementation: this branch.

Complete and release:

- deterministic RGB/RGBA-to-grayscale normalization and resizing;
- raw, zlib and PNG baseline payloads;
- mean absolute pixel difference and changed-pixel fraction;
- deterministic visual difference image;
- generic orthographic projection;
- expected box, through-hole and through-slot drawing;
- independent goal image and actual-overlay composition;
- structured per-view visual evidence with explicit missing states;
- no CAD rendering, required-view policy, model cameras or model baselines;
- built-wheel tests for issue #9 R1-R10.

After green CI:

1. merge the implementation;
2. verify release 0.4.0 comes from the tested main commit;
3. close #9;
4. remove this section.

## 2. Add semantic verification result composition — #10

Implement generic semantic check records, deterministic overall-status
composition, evidence/order preservation, require-pass validation, aggregate
composition and adapter support for existing verification reports.

No Forge-specific check names or CAD-CI publication behavior belong here.

## 3. Final reusable-verification audit — #4

After #9 and #10 are released:

- compare implementation against the historical ownership map in #4;
- confirm every reusable historical verification mechanic has moved here or has
  an explicit non-library owner;
- confirm public APIs and requirement-to-test mappings are complete;
- confirm downstream repositories only need released library versions.

Close #4 when the audit passes.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #9 Add reusable visual regression and expected-shape overlay primitives | now | Active implementation. Complete, test through the installed wheel, release 0.4.0, then close. |
| #10 Add reusable semantic verification result composition | next | Required for deterministic aggregate verification results and fan-in. |
| #4 Expand reusable CAD verification mechanics beyond the foundation | final audit | Close only after #9/#10 are released and the historical ownership map is fully accounted for. |

Immediate execution chain:
`#9 -> #10 -> #4 -> Forge #378`.
