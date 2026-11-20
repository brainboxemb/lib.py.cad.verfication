# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

Release `0.11.0` is complete at exact commit
`9f2802816637d944c88815352ecadb72e78027f5`.

A full audit of the first post-proof Forge #432 batch found one additional
existing consumer contract that 0.11.0 cannot express without adding
incidental policy: several one-body models verify volume/face/sheet properties
of the sole body without asserting its generated native body name.

## Current goal

Complete #65: allow `SolidCraftBodyExpectation` to select the sole measured
body without requiring or validating a native body name.

This is the final prerequisite found by the complete batch-1 contract audit.

## Required proof

- existing non-empty `name_prefix` selection remains unchanged;
- `name_prefix=None` selects the sole body and requires exactly one body;
- sole-body selection does not read or validate the body's `name` field;
- zero/multiple bodies are normal verification mismatches;
- requested bounds, volume, face-type, sheet-metal and closed checks reuse
  existing semantics;
- deterministic evidence identifies the selector as `sole` without adding a
  body name to expected policy;
- malformed requested property evidence remains typed;
- complete installed-wheel suite stays green.

## Execution order

1. Define sole-body semantics in requirements/design.
2. Add focused adapter tests.
3. Implement the smallest backward-compatible selector extension.
4. Run the complete library suite.
5. Release the resulting API as 0.12.0.
6. Update docker.cad.solidcraft runtime patch release to the exact 0.12.0 pin.
7. Resume Forge #537 batch 1.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #65 Allow declarative expectations for the sole SolidCraft body without naming it | now | Final generic gap found by full Forge batch-1 contract audit. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to qualification migration. |

Immediate chain:
`#65 -> verification 0.12.0 -> runtime pin -> Forge #537 batch 1`.
