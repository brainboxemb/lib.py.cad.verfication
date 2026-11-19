# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verfication`.

Detailed behavior belongs in `docs/requirements.md`. Technical structure
belongs in `docs/design.md`.

## Current goal

Complete #36: add the declarative SolidCraft model-verification layer above the
released 0.8.0 SolidCraft adapter.

The result must let a consumer keep only model-specific expectation data while
this library owns the repeated SolidCraft verification execution.

The consumer is still responsible for producing the initial native SolidCraft
`.sc` model. For Forge that means compile/replay remains Forge behavior.

## Execution order

1. define the declarative verification contract in requirements/design;
2. add built-wheel tests for baseline, saved-design mutation and inspection
   execution;
3. implement the smallest runner that composes the existing SolidCraft adapter
   and generic verification/reporting APIs;
4. prove the runner has no Forge/SCPF, CAD-CI or SCons dependency;
5. document the consumer shape;
6. release the library;
7. only then resume Forge #432 with one representative model before expanding
   to the catalog.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #36 Add declarative SolidCraft model verification | now | Required to remove repeated procedural verifier code from Forge model directories. |

Immediate chain:
`#36 -> release -> Forge #432 one model -> Forge #432 remaining models`.
