# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

Release `0.14.0` functionality is already merged through #74. The saved-design
numeric change prerequisite that previously blocked the final Forge declarative
migration is complete.

The only open repository issue is #48: repository-identity cleanup after the
rename from `lib.py.cad.verfication` to `lib.py.cad.verification`.

## Current goal

Complete #48 without changing the Python package or distribution identity.

The cleanup is documentation/configuration only:

- replace stale repository-name references with
  `lib.py.cad.verification`;
- keep import package `cad_verification` unchanged;
- keep distribution `brainboxemb-cad-verification-lib` unchanged;
- inspect active workflow/configuration metadata for stale repository names.

## Execution order

1. Update this plan and reassess all open issues.
2. Correct stale repository-name references in primary documentation.
3. Inspect active workflow/configuration/package metadata for the old name.
4. Run/review the repository's normal Python-library CI.
5. Merge #48 and remove the completed work from this plan.

## Open issue assessment — 2026-11-21

| Issue | Status | Assessment |
| --- | --- | --- |
| #48 Replace remaining lib.py.cad.verfication repository-name references | now | Only remaining open issue; documentation/repository-identity cleanup with no Python API rename. |

Immediate chain:
`#48 repository-name cleanup -> no currently planned verification-library work`.
