# lib.py.cad.verfication

Reusable Python library for CAD/model verification.

Current release candidate: **0.3.0**.

The repository name keeps the existing `verfication` spelling. The Python
package uses the normal spelling: `cad_verification`.

## Purpose

This library provides reusable verification mechanics that are useful across
CAD consumers without becoming a second CI system.

`tool.cad.ci` remains the only CI runner. A consumer can call this library
from a normal CAD-CI step such as `model_verify`.

## Responsibilities

The library owns:

- one explicit verification request;
- ordered verification checks inside that request;
- structured pass/skip/fail/error results;
- validation and hashing of produced verification artifacts;
- safe execution of external CAD commands with explicit timeout/failure types;
- a stable JSON verification report.

Consumers own:

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

The first consumer will be Forge, but this repository must remain independent
of Forge and SolidCraft.


## Geometry verification

The library can validate an already-exported STL against a consumer-owned
geometry contract:

~~~python
from pathlib import Path

from cad_verification import (
    GeometryContract,
    SurfaceDistanceProbe,
    validate_mesh_geometry,
)

contract = GeometryContract(
    bounds_min=(-5.0, -10.0, -15.0),
    bounds_max=(5.0, 10.0, 15.0),
    bounds_tolerance_mm=0.01,
    volume_mm3=6000.0,
    volume_tolerance_mm3=0.5,
    watertight=True,
    surface_distance_probes=(
        SurfaceDistanceProbe(
            "outside-x",
            (10.0, 0.0, 0.0),
            5.0,
            0.01,
        ),
    ),
)

evidence = validate_mesh_geometry(Path("reference.stl"), contract)
~~~

A geometry mismatch raises `VerificationFailure`. Missing or unreadable mesh
data raises `MeshLoadError`. Model-specific expected geometry remains in the
consumer repository.


## Numeric comparison

The library can compare already-measured consumer data without importing a CAD
engine:

~~~python
from cad_verification import (
    BodyEnvelope,
    compare_bounds,
    compare_scalar,
    compare_vector,
    match_body_envelopes,
)

compare_scalar(20.0, 20.02, 0.05)
compare_vector((1, 2, 3), (1.01, 2, 3), 0.05)
compare_bounds(
    (0, 0, 0),
    (10, 20, 30),
    (0.01, 0, 0),
    (10, 20, 30),
    0.05,
)

match_body_envelopes(
    (BodyEnvelope((0, 0, 0), (10, 10, 10), "body"),),
    (BodyEnvelope((0.01, 0, 0), (10.01, 10, 10)),),
    0.05,
)
~~~

Passing comparisons return deterministic evidence. A mismatch raises
`VerificationFailure` with the same evidence.


## Repository CI

This repository is an ordinary Python library. Its own package build/test
workflow uses `tool.py.lib.ci` 0.1.2 at exact commit
`9045367540102ba2208c517e45a52ddad4bb60ea`, after that revision passed the
external `tool.py.lib.ci.test` repository.

This does not change how downstream CAD repositories use the library:
`tool.cad.ci` remains the CAD repository runner, while this package only
provides reusable verification functions.
