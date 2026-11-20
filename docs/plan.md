# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

The complete first-batch SolidCraft prerequisite set is merged on `main`:

- #44 partial parameter expectations;
- #45 partial sketch expectations;
- #51 declarative count expectations;
- #52 multi-body prefix groups;
- #53 projected/tolerant inspection expectations.

Each feature was implemented and tested in its own issue/PR. No intermediate
release was cut.

## Current goal

Complete #59 and release `0.11.0` once for the complete prerequisite set.

## Required proof

- `VERSION`, `pyproject.toml` and changelog all declare 0.11.0;
- complete installed-wheel CI is green on the exact release head;
- GitHub release/tag `v0.11.0` exists after merge;
- #44/#45/#51/#52/#53 can then close as delivered;
- no additional verification semantics are added in the release PR.

## Execution order

1. Release 0.11.0.
2. Inspect `docker.cad.solidcraft` ownership/pin before Forge adoption.
3. If required, release a new immutable SolidCraft runtime containing
   verification 0.11.0.
4. Resume Forge #432 first ~10-case qualification batch.
5. Keep broader Pages cut-over blocked until current durable evidence covers the
   existing public Qualification catalog.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #59 Release lib.py.cad.verification 0.11.0 for the first Forge qualification batch | now | All five generic prerequisite PRs are merged and green; one feature release remains. |
| #44 Allow partial SolidCraft parameter expectations | effectively complete but still open | Merged; close after v0.11.0 exists. |
| #45 Allow partial SolidCraft sketch expectations | effectively complete but still open | Merged; close after v0.11.0 exists. |
| #51 Add declarative SolidCraft count expectations for measured model/body evidence | effectively complete but still open | Merged; close after v0.11.0 exists. |
| #52 Allow declarative expectations for multiple SolidCraft bodies sharing a name prefix | effectively complete but still open | Merged; close after v0.11.0 exists. |
| #53 Add projected and tolerant declarative SolidCraft inspection expectations | effectively complete but still open | Merged; close after v0.11.0 exists. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Independent naming/documentation cleanup. |

Immediate chain:
`v0.11.0 -> runtime ownership/pin -> Forge #432 batch 1`.
