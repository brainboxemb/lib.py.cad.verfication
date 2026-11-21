# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

Issue #75 implementation is complete and green in PR #76 at main commit
`c04f666118b204d93427be0fc828682258486087`.

The next immutable release is `0.15.0`. It exposes generic
`ThroughPathSlot` expected-shape evidence required by Forge #378 while
preserving existing visual behavior.

## Current goal

Publish `0.15.0` from the exact green main release commit, then let Forge
consume it for full-catalog visual verification.

## Execution order

1. [#75, now] Publish immutable `0.15.0`.
2. Verify the release tag targets the exact tested main commit.
3. Close #75 after the release exists.
4. Resume Forge #378 against released `0.15.0`.

## Open issue assessment — 2026-11-21

| Issue | Status | Assessment |
| --- | --- | --- |
| #75 Support polyline through-slot expected-shape evidence | now | Implementation is merged; immutable 0.15.0 release remains. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to Forge visual restoration. |

Immediate chain:
`verification 0.15.0 release -> Forge #378 full-catalog visual verification`.
