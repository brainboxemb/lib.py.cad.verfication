# AGENTS.md

## Purpose

`lib.py.cad.verification` is the reusable Python library for CAD/model
verification mechanics.

## CI boundary

This repository is an ordinary Python library.

Its own CI uses `tool.py.lib.ci` 0.1.2 at exact commit
`9045367540102ba2208c517e45a52ddad4bb60ea`, after that revision passed
`tool.py.lib.ci.test`.

Do not make this repository depend on `tool.cad.ci`, `lib.py.cad.ci` or
SCons merely to build/test the Python package.

`tool.cad.ci` is for CAD/Forge repositories that need CAD item
selection, dependency graphs, incremental rebuilds and durable CAD build
output.

## Domain boundary

This repository owns CAD verification behavior.

It contains reusable verification mechanics and CAD-engine-specific verification
adapters when those adapters are required to inspect or verify a CAD result.
Shared SolidCraft result schemas, measurement parsing and verification commands
belong here rather than in Forge.

Consumer repositories such as Forge own only the code/models being verified and
their model-specific verification data: expected values, tolerances, mutations,
views and other model policy. They do not own the shared logic that interprets
or checks those values against SolidCraft.

CI selection, SCons execution, caching, repository orchestration and
publication remain outside this library.

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

