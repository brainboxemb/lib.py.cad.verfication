# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

`lib.py.cad.verification 0.11.0` is released at exact commit
`9f2802816637d944c88815352ecadb72e78027f5`.

The complete generic prerequisite set for the first post-proof Forge
qualification batch is released:

- partial parameter expectations;
- partial sketch expectations;
- declarative sketch/timeline/face-type counts;
- multi-body prefix groups;
- projected/tolerant inspection expectations.

Issues #44, #45, #51, #52 and #53 are complete and closed.

## Current goal

No active library implementation work.

The next step is outside this repository:

1. inspect `docker.cad.solidcraft` for ownership of the verification-library pin;
2. if owned there, adopt exact verification 0.11.0 and release a new immutable runtime;
3. then resume Forge #432 first ~10-case migration batch.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Independent naming/documentation cleanup; not a blocker for Forge qualification migration. |
| #63 Update repository plan after verification 0.11.0 release | now | Administrative closeout after the confirmed immutable release. |

Immediate chain:
`runtime ownership/pin -> Forge #432 batch 1`.
