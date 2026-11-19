# AGENTS.md

## Purpose

`lib.py.cad.verfication` is the reusable Python library for CAD/model
verification mechanics.

## Hard boundary

`tool.cad.ci` is the only CI runner.

Do not add:

- Git changed-path selection;
- SCons graph/rebuild logic;
- cache decisions;
- GitHub Actions orchestration;
- repository dependency scheduling;
- publication or Pages handling.

This library executes one explicit verification request already selected by
the caller.

## Domain boundary

Keep this repository CAD-engine neutral.

Forge, SolidCraft, OpenSCAD and other consumers own their engine adapters,
commands, expectations and fixtures. Generic execution/result/artifact
mechanics belong here.

## Development process

Before changing behaviour:

1. define observable behaviour in `docs/requirements.md`;
2. define exact semantics in `docs/design.md`;
3. add or update tests;
4. implement the smallest code that satisfies the contract.

If a consumer exposes an undefined generic behaviour, stop and update the
design before coding it into the consumer.

## Change quality

All Python modules and non-obvious logic need concise explanatory
docstrings/comments.

Keep one logical change per branch/PR. Prefer squash merges.
