# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

Release `0.11.0` is complete. The full Forge batch-1 contract audit then found
one additional generic selector gap: model contracts that inspect properties
of the sole measured body without asserting its generated native name.

#65 is merged at `7897b553a81c98d0ac93989446959b7156aca61f`.

## Current goal

Complete #67 and release the sole-body selector as 0.12.0.

No verification behavior is added in the release change.

## Required proof

- VERSION and pyproject.toml declare 0.12.0;
- CHANGELOG documents the sole-body selector;
- complete installed-wheel CI passes;
- main publishes immutable v0.12.0 from the exact green release commit;
- docker.cad.solidcraft #12 updates to this exact release;
- Forge #537 starts only after the immutable runtime pin is green.

## Execution order

1. Prepare 0.12.0 release metadata only.
2. Run complete library CI.
3. Merge and verify immutable v0.12.0 publication.
4. Update docker.cad.solidcraft #12 from 0.11.0 to exact 0.12.0.
5. Release runtime v0.3.1.
6. Resume Forge #537 batch 1.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #67 Release sole-body selector as 0.12.0 | now | Final generic batch-1 prerequisite is merged; publish it immutably. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to qualification migration. |

Immediate chain:
`#67 verification 0.12.0 -> runtime v0.3.1 -> Forge #537 batch 1`.
