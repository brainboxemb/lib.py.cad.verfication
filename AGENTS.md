# AGENTS.md

## Purpose

`lib.py.cad.verfication` is the reusable Python library for CAD/model
verification mechanics.

## CI boundary

This repository is an ordinary Python library.

Its own CI must use the generic Python-library CI layer:

```text
tool.py.lib.ci
```

Do not make this repository depend on `tool.cad.ci`, `lib.py.cad.ci` or
SCons merely to build/test the Python package.

`tool.cad.ci` is for CAD/Forge repositories that need CAD item
selection, dependency graphs, incremental rebuilds and durable CAD build
output.

## Domain boundary

Keep this repository CAD-engine neutral.

Forge, SolidCraft, OpenSCAD and other repositories own their engine adapters,
commands, expectations and fixtures. Generic execution/result/artifact
mechanics belong here.

## Repository plan

Current unfinished repository work lives in `docs/plan.md`.

Rules:

- keep one general repository plan, not separate CI/verification/release plans;
- the plan contains only unfinished work;
- remove a completed section after its PR/release is finished;
- permanent behaviour belongs in `docs/requirements.md` and
  `docs/design.md`;
- issues provide detailed discussion/history, but the current execution order
  must be readable from `docs/plan.md`;
- when no planned work remains, `docs/plan.md` may be removed.

## Development process

Before changing behaviour:

1. define observable behaviour in `docs/requirements.md`;
2. define exact semantics in `docs/design.md`;
3. add or update tests;
4. implement the smallest code that satisfies the contract.

If a repository exposes an undefined generic behaviour, stop and update the
design before coding it into that repository.

## Change quality

All Python modules and non-obvious logic need concise explanatory
docstrings/comments.

Keep one logical change per branch/PR. Prefer squash merges.

## Repository plan source of truth

`docs/plan.md` is the current source of truth for unfinished repository work.

Keep it as a current snapshot:

- state the current goal and execution order;
- include every open issue in an issue assessment snapshot;
- give each open issue an explicit status such as `now`, `later`, `blocked`, `probably obsolete`, or `effectively complete but still open`;
- explain briefly why that status applies;
- identify dependencies or blockers between issues;
- keep the issue assessment current when issues are opened, closed, merged or superseded.

Issues contain detail and history. README and design/requirements documents describe stable purpose and behavior. The plan tells an agent what work is actually current and what should happen next.

