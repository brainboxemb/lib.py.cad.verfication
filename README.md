# lib.py.cad.verfication

Reusable Python library for CAD/model verification.

Current release: **0.1.0**.

The repository name keeps the existing `verfication` spelling. The Python
package uses the normal spelling: `cad_verification`.

## Purpose

This library provides reusable verification mechanics for CAD repositories
without becoming a CI runner.

CAD repositories can call this library from normal `tool.cad.ci` steps such
as `model_verify`.

## Responsibilities

The library owns:

- one explicit verification request;
- ordered verification checks inside that request;
- structured pass/skip/fail/error results;
- validation and hashing of produced verification artifacts;
- safe execution of external CAD commands with explicit timeout/failure types;
- a stable JSON verification report.

CAD repositories own:

- which checks a model requires;
- CAD-engine-specific commands and adapters;
- expected geometry/history/parameter values;
- model fixtures and mutation commands;
- CI configuration and step selection.

The library does **not** own Git changed-path selection, SCons targets, caching,
GitHub Actions, publication, Pages, repository scheduling or dependency
rebuild decisions.

## Design before implementation

The contract is defined in:

- `docs/requirements.md` — observable behaviour;
- `docs/design.md` — exact library architecture.

If implementation needs behaviour not described there, update the design first.

## Package

~~~python
from cad_verification import (
    CheckOutcome,
    VerificationCheck,
    VerificationContext,
    verify,
)
~~~

The first repository using this library will be Forge, but this library remains independent
of Forge and SolidCraft.


## Repository CI

This repository is an ordinary Python library. Its own package build/test
workflow uses `tool.py.lib.ci` 0.1.2 at exact commit
`9045367540102ba2208c517e45a52ddad4bb60ea`, after that revision passed the
external `tool.py.lib.ci.test` repository.

This does not change how downstream CAD repositories use the library:
`tool.cad.ci` remains the CAD repository runner, while this package only
provides reusable verification functions.
