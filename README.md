# lib.py.cad.verfication

Reusable Python library for CAD/model verification.

Current release candidate: **0.8.0**.

The repository name keeps the existing `verfication` spelling. The Python
package uses the normal spelling: `cad_verification`.

## Purpose

This library provides reusable CAD verification mechanics and CAD-tool-specific
verification adapters without becoming a second CI system.

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

- model definitions and the code that produces them;
- model-specific expected geometry/history/parameter values;
- model-specific mutation, view and tolerance data;
- CI configuration and step selection.

The library owns shared knowledge of how those expectations are checked,
including CAD-tool-specific adapters such as the SolidCraft adapter.

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

The first consumer is Forge. The package remains independent of Forge model
code, but may contain SolidCraft-specific verification behavior in the
SolidCraft adapter.


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


## Visual verification

The library provides generic visual evidence without rendering CAD itself:

~~~python
from cad_verification import (
    ExpectedBox,
    OrthographicCamera,
    compare_images,
    make_goal_image,
    make_overlay_image,
    normalize_image,
)

camera = OrthographicCamera(
    target=(0, 0, 0),
    yaw_deg=0,
    pitch_deg=0,
    distance=100,
)

actual = normalize_image("actual.png", 800, 600)
goal = make_goal_image(
    (800, 600),
    camera,
    boxes=(ExpectedBox((-10, -10, -10), (10, 10, 10)),),
)
overlay = make_overlay_image(
    actual,
    camera,
    boxes=(ExpectedBox((-10, -10, -10), (10, 10, 10)),),
)
~~~

Consumers own view selection, CAD rendering, camera values, approved
baselines and expected model geometry. The library owns only generic image
comparison, projection, drawing and evidence.

For one already-rendered view the library can compose those primitives directly:

~~~python
from cad_verification import verify_visual_view

evidence = verify_visual_view(
    "actual.png",
    actual_reference="visual/actual.png",
    baseline_path="approved.png",
    normalized_size=(96, 72),
    changed_pixel_threshold=12,
    max_mean_difference=6.0,
    max_changed_fraction=0.08,
    diff_path="visual/diff.png",
    diff_reference="visual/diff.png",
    camera=camera,
    boxes=(expected_box,),
    goal_path="visual/goal.png",
    goal_reference="visual/goal.png",
    overlay_path="visual/overlay.png",
    overlay_reference="visual/overlay.png",
)
~~~

The function never renders CAD, selects a view, computes a model camera or
approves a baseline. A missing baseline is reported explicitly; a regression
mismatch raises `VerificationFailure` with complete `VisualViewEvidence`.


## Exact and predicate requirements

Generic model assertions can preserve stable expected/actual evidence without
putting the failure mechanic in consumer code:

~~~python
from cad_verification import require_condition, require_equal

require_equal(
    {"type": "BoxFeature", "warning": None},
    timeline_row,
    label="native timeline row",
)

require_condition(
    feature_count == 4,
    expected=4,
    actual=feature_count,
    label="native feature count",
)
~~~

These helpers do no CAD interpretation. Consumers own the values and condition;
the library only validates evidence and raises `VerificationFailure`
consistently.


## Semantic result composition

Already-produced verification evidence can be composed without rerunning CAD
work:

~~~python
from cad_verification import (
    SemanticCheck,
    compose_semantic_result,
    require_semantic_pass,
)

result = compose_semantic_result((
    SemanticCheck("primary", "pass", required=True),
    SemanticCheck("optional_check", "skipped", required=False),
))
require_semantic_pass(result)
~~~

The consumer owns check names and which checks are required. The library owns
only generic status validation, precedence, evidence preservation and
aggregation.


## SolidCraft adapter

CAD-tool-specific verification lives under `cad_verification.adapters`.

Forge keeps model-specific expectation data. The SolidCraft adapter owns how
that data is checked against SolidCraft measurement/result structures and owns
the reusable `solidcraft-cli` evaluate/mutate/inspect operations.

The adapter does not import Forge/SCPF and does not contain model-specific
dimensions or model names.


## Declarative SolidCraft model verification

Once a consumer has produced a native SolidCraft `.sc` model, the remaining
verification is declarative:

~~~python
from cad_verification import (
    BodyEnvelope,
    SolidCraftModelExpectation,
    SolidCraftSavedDesign,
    SolidCraftVerification,
    run_solidcraft_verification,
)

definition = SolidCraftVerification(
    verification_id="simple-box",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        body_envelopes=(
            BodyEnvelope(
                (-20, -15, 0),
                (20, 15, 10),
            ),
        ),
        bounds_tolerance=0.001,
        parameters={
            "length": 40.0,
            "width": 30.0,
            "height": 10.0,
        },
    ),
    saved_designs=(
        SolidCraftSavedDesign(
            id="length_50",
            command_path="change_length.json",
            expectation=SolidCraftModelExpectation(
                body_count=1,
                body_envelopes=(
                    BodyEnvelope(
                        (-25, -15, 0),
                        (25, 15, 10),
                    ),
                ),
                bounds_tolerance=0.001,
                parameters={
                    "length": 50.0,
                    "width": 30.0,
                    "height": 10.0,
                },
            ),
        ),
    ),
)

report = run_solidcraft_verification(
    "model.sc",
    "verification-output",
    definition,
)
~~~

The consumer does not implement its own SolidCraft eval/mutate/inspect loop,
check construction, artifact handling or report writing. Forge/SCPF remains
responsible only for producing the initial native model and for supplying the
model-specific definition data.


## Repository CI

This repository is an ordinary Python library. Its own package build/test
workflow uses `tool.py.lib.ci` 0.1.2 at exact commit
`9045367540102ba2208c517e45a52ddad4bb60ea`, after that revision passed the
external `tool.py.lib.ci.test` repository.

This does not change how downstream CAD repositories use the library:
`tool.cad.ci` remains the CAD repository runner, while this package only
provides reusable verification functions.
