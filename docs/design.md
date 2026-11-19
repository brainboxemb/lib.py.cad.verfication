# CAD verification library design

This document is the normative technical design for
`lib.py.cad.verfication`.

`docs/requirements.md` defines observable behaviour. If implementation needs
a semantic choice not described here, update this document before coding it.

## 1. Architecture

The library has one narrow responsibility:

> Execute one explicit verification request and describe its result.

It sits below a consumer-owned `model_verify` command and above
consumer/engine-specific check functions.

~~~text
CAD-CI model_verify step
        |
        v
consumer verification definition
        |
        v
cad_verification.verify()
        |
        +--> consumer check
        +--> consumer check
        +--> consumer check
        |
        v
verification.json
~~~

There is no repository planner, scheduler, dependency graph or cache.

## 2. Package layout

~~~text
cad_verification/
  __init__.py
  errors.py
  evidence.py
  model.py
  process.py
  verification.py
~~~

### model.py

Owns immutable public data objects:

- `VerificationContext`;
- `CheckOutcome`;
- `VerificationCheck`;
- `CommandResult`.

### errors.py

Owns public exception classes and keeps domain failure distinct from
infrastructure/process failure.

### evidence.py

Validates output artifacts and produces deterministic file/directory records.

### process.py

Executes one explicit external argv command. It has no knowledge of CAD-CI or
verification plans.

### verification.py

Validates one request, executes checks sequentially and writes the final report.

## 3. Public API

~~~python
context = VerificationContext(
    verification_id="simple-box",
    input_path=Path("solidcraft.json"),
    output_dir=Path("build/model_verify"),
)

checks = (
    VerificationCheck("build", build_check),
    VerificationCheck("geometry", geometry_check),
)

report = verify(context, checks)
~~~

A check receives the immutable context and returns either:

- `None`, meaning pass with no extra evidence;
- `CheckOutcome.passed(...)`;
- `CheckOutcome.skipped(reason, ...)`.

For an expected mismatch it raises `VerificationFailure`.

Any other exception is an infrastructure/error result.

## 4. Sequential semantics

A verification request contains at least one check. A zero-check request is a
configuration error rather than a vacuous pass.

Checks are deliberately sequential because later CAD verification operations
often consume artifacts from earlier operations.

The library executes exactly the supplied order.

It does not:

- discover prerequisites;
- skip current work;
- restore cached work;
- rerun subsets by itself.

Those concerns remain outside this library.

On the first `fail` or `error`, execution stops and the final report is
written immediately.

## 5. Artifact evidence

All check artifacts are interpreted relative to or resolved beneath
`context.output_dir`.

For a regular file, evidence contains:

~~~json
{
  "path": "native/model.step",
  "kind": "file",
  "size": 1234,
  "sha256": "..."
}
~~~

For a directory:

~~~json
{
  "path": "native/renders",
  "kind": "directory",
  "entries": 4,
  "sha256": "..."
}
~~~

Directory digest input is a lexical sequence of records containing entry type,
relative path and file content hash. Empty directories participate. Symlinks
are rejected.

The library report itself is not a check artifact.

## 6. Report schema

Schema 1:

~~~json
{
  "schema": "cad-verification",
  "schema_version": 1,
  "verification_id": "simple-box",
  "status": "pass",
  "input": "solidcraft.json",
  "metadata": {},
  "checks": [
    {
      "id": "build",
      "status": "pass",
      "reason": null,
      "error": null,
      "evidence": {},
      "artifacts": []
    }
  ]
}
~~~

Allowed check statuses:

- `pass`;
- `skipped`;
- `fail`;
- `error`.

Allowed overall statuses:

- `pass`;
- `fail`;
- `error`.

The report deliberately contains no start/end timestamps.

## 7. Expected failure

`VerificationFailure` means:

> The verification mechanism worked and proved that the model does not satisfy
> an expected condition.

The exception carries a human-readable message and optional JSON-compatible
evidence.

The verification operation records a `fail` row and stops.

## 8. Unexpected error

Configuration errors, unsafe artifacts, missing artifacts, process failures
not explicitly converted by the consumer, and unexpected exceptions are
`error`.

The report records the exception class and message. Python tracebacks are not
embedded in durable JSON evidence.

The original exception is re-raised only when the caller requests
`raise_on_error=True`; the default API returns the structured report so a
consumer can choose its own exit handling.

Expected verification failure is never re-raised by `raise_on_error`.

## 9. Process helper

`run_command()` calls `subprocess.run(..., shell=False)`.

Environment behaviour:

- start from the current process environment;
- overlay caller-provided values;
- stringify keys/values.

Timeout must be a positive number when supplied.

Success returns `CommandResult` with argv, return code, stdout and stderr.

Non-zero exit raises `CommandFailed`.

Timeout raises `CommandTimedOut`.

## 10. CAD-engine verification boundary

The verification library may provide an engine-specific adapter that calls or
reads a CAD engine when that behavior is part of reusable verification.

A consumer may still supply the engine input and model-specific expectation
data. For example:

~~~python
def build_check(ctx):
    run_command(
        ["solidcraft-cli", "run", str(ctx.input_path), ...],
        cwd=ctx.work_dir,
    )
    return CheckOutcome.passed(
        artifacts=(ctx.output_dir / "native/model.sc",)
    )
~~~

Shared SolidCraft inspection/parsing/checking behavior belongs in this library.

Geometry expectations such as body counts, bounds, parameter values, mutation
targets and required views stay with the model in Forge and are passed into the
library as data.

The boundary is therefore:

- Forge knows **what this model should be**;
- this library knows **how to prove that against SolidCraft**;
- neither side duplicates the other's responsibility.

## 11. Relationship with CAD-CI

CAD-CI sees one ordinary consumer command:

~~~yaml
- id: model_verify
  run: [python, verify_model.py]
  outputs:
    - model_verify
~~~

CAD-CI owns whether that command runs. If it runs, this library owns only the
verification operation inside that command.

The library never reads `CAD_CI_*` variables itself. A consumer may use those
variables to construct `VerificationContext`.

## 12. Implementation order

1. requirements and this design;
2. immutable model/error types;
3. artifact evidence;
4. process helper;
5. sequential verification execution/report;
6. unit tests covering the acceptance list;
7. release only after independent tests pass;
8. only then consume from Forge.

Do not migrate Forge code into this repository before steps 1-7 are complete.


## 13. Geometry verification

### 13.1 Module

Add one module:

```text
cad_verification/
  geometry.py
```

It owns only generic mesh geometry verification.

### 13.2 Public immutable types

`geometry.py` defines frozen dataclasses:

```python
SurfaceDistanceProbe
GeometryContract
```

Their `__post_init__` methods normalize numeric vectors to float tuples and
raise `VerificationConfigError` for invalid configuration.

### 13.3 Mesh library

Use `trimesh>=4,<5` and `scipy>=1.12,<2` as explicit package dependencies. `scipy` is required by trimesh's validated topology-processing path used by the watertightness check.

`validate_mesh_geometry()` loads the supplied STL with trimesh.

If trimesh returns a Scene, concatenate measurable geometries into one mesh.

Reject:

- missing paths;
- empty files;
- load/parse failures;
- geometries without vertices or faces.

Those cases raise `MeshLoadError`, which derives from
`VerificationError`.

### 13.4 Measurements

The validator computes one evidence dictionary in deterministic insertion order.

Bounds:

- use mesh bounds directly;
- compare each min/max coordinate with the configured tolerance.

Volume:

- use absolute mesh volume;
- only evaluate when configured.

Watertightness:

- evaluate `is_watertight` on a copy of the mesh;
- do not mutate the mesh used for other measurements.

Surface probes:

- use trimesh nearest-surface calculation without consumer-specific policy;
- preserve contract probe order.

Contract sufficiency:

- `bounds_sufficient=True` allows a bounds-only contract;
- `bounds_sufficient=False` requires volume or at least one surface probe;
- this preserves the historical rule that internal-feature cases cannot pass
  solely because their outer envelope matches.

### 13.5 Mismatch handling

Do not raise on the first geometry mismatch.

Evaluate every configured geometry check, store all evidence, then raise one
`VerificationFailure` if any check failed.

This preserves passing evidence when a later check fails.

### 13.6 Existing verification integration

No changes to `verify()` semantics are required.

- `VerificationFailure` is already recorded as `fail`;
- `MeshLoadError` is an ordinary unexpected `VerificationError` and is
  recorded as `error`.

### 13.7 Public exports

Export from `cad_verification.__init__`:

```python
GeometryContract
SurfaceDistanceProbe
validate_mesh_geometry
MeshLoadError
```

### 13.8 Test construction

`tests/test_geometry.py` generates small mesh fixtures using trimesh.

The canonical fixture is a centered 10 x 20 x 30 mm box.

An open-box fixture removes one face from the generated mesh.

A disconnected multi-part fixture combines two generated boxes before STL
export.

Tests run through the built wheel using the existing library CI path.

## 14. Numeric and measured-body comparison

### 14.1 Module

Add one CAD-engine-neutral module:

```text
cad_verification/
  comparison.py
```

The generic comparison module accepts only Python numeric values, vectors and
normalized body envelopes. It remains independent of SolidCraft and Forge.

Engine-specific modules may depend on the public generic comparison API, but
must not embed Forge model knowledge.

### 14.2 BodyEnvelope

Expose one frozen `BodyEnvelope` dataclass containing:

- `minimum`: XYZ minimum;
- `maximum`: XYZ maximum;
- optional `label`.

Construction normalizes XYZ values to finite float tuples and rejects inverted
bounds. Labels are descriptive evidence only; bounds determine matching.

### 14.3 Scalar and vector comparison

Expose:

```python
compare_scalar(expected, actual, tolerance, *, label=None)
compare_vector(expected, actual, tolerance, *, label=None)
```

Both functions validate finite numeric input and a non-negative tolerance.

A passing comparison returns deterministic JSON-compatible evidence. A mismatch
raises `VerificationFailure` with exactly that evidence.

Vector comparison requires equal non-empty vectors and records per-element
absolute deltas plus the maximum delta.

### 14.4 Bounds comparison

Expose:

```python
compare_bounds(
    expected_min,
    expected_max,
    actual_min,
    actual_max,
    tolerance,
    *,
    label=None,
)
```

All four vectors are normalized as XYZ values. Expected and actual bounds must
not be inverted. Evidence records expected/actual min/max vectors, six absolute
coordinate deltas, maximum delta, tolerance and pass/fail.

### 14.5 Body-envelope matching

Expose:

```python
match_body_envelopes(expected, actual, tolerance)
```

Inputs contain `BodyEnvelope` values.

Matching is one-to-one and independent of actual input order:

1. normalize and canonically sort actual envelopes by label/bounds;
2. walk expected envelopes in their declared order;
3. for each expected envelope, choose the unmatched in-tolerance actual envelope
   with the smallest maximum bounds delta;
4. break equal-distance ties by canonical actual envelope order.

Evidence contains counts, matched pairs, unmatched expected envelopes, unmatched
actual envelopes and pass/fail. Any unmatched envelope raises one
`VerificationFailure` after the complete evidence has been built.

### 14.6 Existing verification integration

No change to `verify()` is required.

Consumers may return passing comparison evidence from a normal check. A raised
`VerificationFailure` is already mapped to check status `fail` and its
evidence is preserved in `verification.json`.

### 14.7 Public exports and tests

Export:

```python
BodyEnvelope
compare_scalar
compare_vector
compare_bounds
match_body_envelopes
```

Tests cover issue #8 R1-R6 and run through the installed wheel using the
repository's released `tool.py.lib.ci` path.

## 15. Visual regression and expected-shape evidence

### 15.1 Module and dependency

Add one generic module:

```text
cad_verification/
  visual.py
```

Declare Pillow explicitly. The module owns image normalization, baseline
payloads, regression metrics, generic orthographic projection and drawing. It
does not render CAD or know model/view names.

### 15.2 Normalized images

`normalize_image(path, width, height)` loads an image with Pillow, converts it
through RGB to grayscale, resizes with LANCZOS and returns a grayscale
`PIL.Image.Image` with the exact requested size.

Missing, unreadable or invalid images raise `VisualEvidenceError`, derived
from `VerificationError`. Width and height must be positive integers.

### 15.3 Baseline payloads

Expose deterministic baseline helpers using a JSON-compatible payload with:

- encoding: `raw`, `zlib` or `png`;
- width;
- height;
- base64 data.

`encode_baseline(image, encoding=...)` accepts a normalized grayscale image.
`decode_baseline(payload)` returns a grayscale image and validates dimensions
and byte count.

Raw and zlib forms encode grayscale bytes. PNG form encodes a deterministic
Pillow PNG byte stream.

### 15.4 Regression comparison

`compare_images(current, reference, ...)` requires same-size grayscale
images and computes:

- mean absolute pixel difference;
- changed-pixel fraction where absolute difference is greater than or equal to
  the caller-supplied changed-pixel threshold.

The caller supplies a maximum mean difference and maximum changed fraction.
Evidence records both metrics, thresholds and pass/fail. Metrics are rounded to
six decimal places for stable evidence. A mismatch raises
`VerificationFailure` with the complete evidence.

### 15.5 Difference image

`write_diff_image(current, reference, output_path)` creates one deterministic
RGB image with current grayscale information and absolute-difference
information visible side by side. The output is twice the normalized width and
keeps the same height.

### 15.6 Orthographic camera

Expose frozen `OrthographicCamera`:

- target XYZ;
- yaw degrees;
- pitch degrees;
- distance.

Distance is the orthographic half-height scale and must be positive. Projection
uses a stable camera basis. Exact top/bottom pitch uses a fallback up vector so
the basis remains valid.

`project_points(points, camera, width, height)` maps consumer-supplied 3D
points to image-space floats. Front orientation maps X right and Z up; top
orientation maps X right and Y up.

### 15.7 Expected geometry types

Expose frozen generic data types:

- `ExpectedBox(minimum, maximum, label=None)`;
- `ThroughHole(center, diameter, z_min, z_max, label=None)`;
- `ThroughSlot(start, end, width, z_min, z_max, label=None)`.

All values are normalized to finite floats. Bounds/ranges must not be inverted.
Slot start and end may not be identical. Width/diameter must be positive.

### 15.8 Expected drawing

`draw_expected_geometry(image, camera, boxes=(), features=(), ...)` returns an
RGB image copy with deterministic outlines. It accepts only the generic types
above and rejects unknown feature objects.

Boxes draw projected edges. Through holes draw projected top/bottom circles and
their connecting side lines. Through slots draw projected capsule outlines at
both Z levels and connecting side lines.

Labels and translucent fill are optional generic presentation switches; tests do
not depend on fonts.

### 15.9 Goal and overlay

`make_goal_image(size, camera, ...)` creates a blank RGB image and draws only
consumer-supplied expected geometry.

`make_overlay_image(actual, camera, ...)` copies the actual render and draws
the same expected geometry over it, preserving unmodified actual pixels away
from expected geometry.

### 15.10 Visual view evidence

Expose frozen `VisualViewEvidence` containing:

- actual image reference or None;
- baseline status;
- optional regression evidence;
- optional diff image reference;
- goal image reference or None;
- overlay image reference or None;
- expected-shape status.

Its `to_evidence()` output is deterministic JSON-compatible evidence.
Missing baseline is represented explicitly as `missing`. Missing actual,
goal or overlay are represented independently and are not converted into pixel
mismatch.

### 15.11 Boundary and tests

The module must not import or invoke SolidCraft, CADCraft, Forge or a CAD
engine. It owns no required-view list, model camera, baseline or expected
geometry fixture.

Tests cover issue #9 R1-R10 through the installed wheel.

### 15.12 Single-view verification orchestration

Expose one additional generic function:

```python
verify_visual_view(
    actual_path,
    *,
    actual_reference,
    baseline_path=None,
    normalized_size,
    changed_pixel_threshold,
    max_mean_difference,
    max_changed_fraction,
    diff_path,
    diff_reference=None,
    camera=None,
    boxes=(),
    features=(),
    goal_path=None,
    goal_reference=None,
    overlay_path=None,
    overlay_reference=None,
)
```

The function operates on one already-rendered consumer image. It never renders
CAD and does not know a view name.

Behavior:

1. normalize `actual_path` with `normalize_image()`;
2. when `baseline_path` is absent or does not exist, set
   `baseline_status="missing"`, leave regression/diff evidence empty and do
   not create a baseline;
3. when a baseline exists, normalize it, write `diff_path`, then call
   `compare_images()`;
4. if regression fails, retain its evidence and continue composing optional
   goal/overlay evidence before raising one `VerificationFailure`;
5. when `camera` is supplied, at least one expected box/feature and both
   `goal_path` and `overlay_path` are required; create both through the
   existing generic drawing APIs;
6. when `camera` is absent, expected geometry and goal/overlay paths must also
   be absent, and `expected_shape_status="missing"`;
7. return one `VisualViewEvidence` on pass/missing-baseline;
8. on regression mismatch raise `VerificationFailure` with
   `VisualViewEvidence.to_evidence()` as failure evidence.

Evidence references are caller-controlled strings. The library never rewrites
them relative to a repository or output tree. If a produced artifact reference
is omitted, the corresponding evidence reference is `None`.

This function composes only existing visual primitives. It does not introduce a
view loop, required-view policy, model camera conversion, baseline approval or
CAD-engine adapter.

### 15.13 Single-view validation rules

- `normalized_size` contains two positive integers;
- `actual_reference` is a string or `None`;
- diff/goal/overlay references are strings or `None`;
- `diff_path` is required when an existing baseline is compared;
- expected geometry without a camera is invalid;
- a camera without expected geometry is invalid;
- a camera requires both goal and overlay output paths;
- invalid image paths/data retain `VisualEvidenceError` semantics from
  `normalize_image()`;
- invalid numeric/image/drawing configuration retains existing
  `VerificationConfigError` semantics.

Direct tests cover issue #26 without a consumer repository or CAD engine.

## 16. Semantic result composition

### 16.1 Module

Add one execution-free module:

```text
cad_verification/
  semantic.py
```

It composes consumer-supplied records and existing report data. It does not
execute checks, read repository state or move artifacts.

### 16.2 SemanticCheck

Expose frozen `SemanticCheck` with:

- `name`;
- `status`;
- `required`;
- optional `reason`;
- JSON-compatible `evidence`.

Names use the same lowercase engineering identifier rule as verification IDs.
Allowed statuses are:

`pass`, `fail`, `error`, `missing`, `review`, `blocked`,
`not-required`, `skipped`.

### 16.3 Composition

`compose_semantic_result(checks)` preserves supplied order and returns:

- overall `status`;
- ordered check records.

Only required checks determine overall status. Precedence is:

1. `error`;
2. `fail`;
3. `missing` -> overall `incomplete`;
4. `review`;
5. `blocked`;
6. otherwise `pass`.

Optional checks remain evidence but never lower the overall status.

### 16.4 Pass requirement

`require_semantic_pass(result)` accepts only a composed `pass` result.
Every other overall status raises `SemanticResultError`, a
`VerificationFailure` subclass carrying the complete semantic result as
evidence.

### 16.5 Aggregate

`compose_item_results(items)` accepts an ordered sequence of
`(item_id, semantic_result)` pairs. It does no work beyond validation and
composition.

Aggregate overall precedence is `error`, `fail`, `incomplete`, `review`,
`blocked`, then `pass`. Input item order is preserved.

### 16.6 Existing report adapter

`semantic_checks_from_report(report)` validates an existing
`cad-verification` report and maps its ordered rows:

- pass -> pass;
- fail -> fail;
- error -> error;
- skipped -> skipped.

The report row ID becomes the semantic check name. Row reason, evidence and
artifact records are preserved in the semantic evidence object. The adapter
does not invent paths or consumer policy.

### 16.7 Boundary and tests

The module contains no consumer-domain check names and no CAD-CI, publication,
materialization or repository-state behavior.

Tests cover issue #10 R1-R8 through the installed wheel.


## 17. Exact-value and predicate verification

### 17.1 Module

Add one engine-neutral module:

```text
cad_verification/
  assertions.py
```

It contains only generic expected/actual evidence and failure mechanics.

### 17.2 Public API

Expose:

```python
require_equal(expected, actual, *, label=None)
require_condition(condition, *, expected, actual, label=None)
```

Both return a JSON-compatible evidence object:

```json
{
  "label": "optional label or null",
  "expected": "...caller value...",
  "actual": "...caller value...",
  "pass": true
}
```

On failure the same object is attached to `VerificationFailure` with
`pass=false`.

### 17.3 Equality semantics

`require_equal()` performs exactly `actual == expected`. It does not
normalize numbers, apply tolerance, reorder collections or interpret CAD data.
Consumers use numeric comparison APIs when tolerance is required.

### 17.4 Predicate semantics

`require_condition()` requires `condition` to be exactly `bool`.
Truthiness of numbers, strings, containers or custom objects is rejected.

The consumer constructs the condition from model/domain semantics and supplies
the expected/actual evidence. The library does not inspect or understand that
semantic meaning.

### 17.5 Validation

Expected and actual values must serialize through deterministic
`json.dumps(..., sort_keys=True)`. Labels are `str | None`; empty strings
are allowed as literal descriptive values and are not interpreted.

Invalid inputs raise `VerificationConfigError`. A normal false result raises
`VerificationFailure`.

### 17.6 Boundary

The module must not import CAD libraries, Forge, SolidCraft, repository state,
CI code or publication code. It does not replace toleranced comparison helpers
or semantic-result composition.

Direct built-wheel tests cover issue #29.


## 18. CAD-tool adapter architecture

### 18.1 Package structure

CAD-tool-specific verification lives below:

```text
cad_verification/
  adapters/
    __init__.py
    solidcraft.py
```

Future OpenSCAD, FreeCAD or other adapters use sibling modules. They are added
only when a consumer requires them.

Generic modules such as `comparison.py` and `assertions.py` remain
CAD-tool independent. Adapter modules may call those generic APIs.

### 18.2 Public SolidCraft types

The initial SolidCraft adapter exposes immutable expectation types:

```python
SolidCraftModelExpectation
SolidCraftBodyExpectation
SolidCraftTimelineExpectation
SolidCraftSketchExpectation
```

`SolidCraftModelExpectation` contains only model-specific expected data. It
does not contain callables.

Body-envelope expectations use the existing `BodyEnvelope` type and one
caller-supplied bounds tolerance.

A named-body expectation selects exactly one SolidCraft body by native-name
prefix and may request:

- expected bounds with a tolerance;
- expected volume with a tolerance;
- exact sheet-metal state;
- exact closed/open state.

A timeline expectation contains semantic fields exposed by SolidCraft:
feature type, optional name, expected error and expected warning.

A sketch expectation identifies one sketch by name and may request profile
count, curve count and solver status.

### 18.3 SolidCraft evidence normalization

The adapter validates and normalizes the measurement object before performing
requested comparisons.

Required structure is checked only when the corresponding expectation needs it.
When body verification is requested, `bodies` must be a list and each used
body must contain a valid `bbox.min` and `bbox.max`.

When parameter verification is requested, `params` must be a list of rows
with string `name` and finite numeric `value`.

Timeline/sketch verification follows the same rule: malformed requested
evidence raises `SolidCraftEvidenceError`, derived from `VerificationError`.

No malformed row is silently skipped.

### 18.4 Measurement verification

Expose:

```python
verify_solidcraft_measurements(measurements, expectation)
```

The function builds deterministic section evidence in this order:

1. body envelopes;
2. parameters;
3. named bodies;
4. timeline;
5. sketches.

Only sections present in the expectation are evaluated.

Implementation reuses:

- `match_body_envelopes()`;
- `compare_bounds()`;
- `compare_scalar()`;
- `require_equal()`;
- `require_condition()` where required.

A comparison mismatch remains `VerificationFailure`. Schema/parse errors are
`SolidCraftEvidenceError`.

### 18.5 SolidCraft command functions

Expose:

```python
evaluate_solidcraft_model(model_path, destination)
mutate_solidcraft_model(model_path, command_path, destination)
inspect_solidcraft_model(model_path, command_path, destination)
```

The exact commands are:

```text
solidcraft-cli eval <model> --json-out <destination>
solidcraft-cli run <command> --in <model> --param-check strict --save <destination>
solidcraft-cli run <command> --in <model> --param-check strict --results --json-out <destination>
```

All processes go through `run_command()`.

JSON produced by evaluate/inspect is loaded by the adapter. Invalid JSON or an
unexpected top-level shape is a `SolidCraftEvidenceError`.

### 18.6 Consumer boundary

Forge keeps declarations such as:

```python
SolidCraftModelExpectation(
    bodies=(...model-specific expected bounds...),
    parameters={...model-specific expected values...},
    timeline=(...model-specific expected features...),
)
```

Forge does not parse `bodies[].bbox`, `params`, `timeline` or
`sketches` and does not implement shared SolidCraft eval/mutate/inspect
helpers.

The SolidCraft adapter does not compile Forge/SCPF source and does not import
Forge. Initial Forge-to-SolidCraft replay remains a producer concern before the
adapter verifies the produced native design.

### 18.7 Tests

Direct built-wheel tests prove:

- valid body/parameter/timeline/sketch expectations pass;
- numeric mismatches produce `VerificationFailure`;
- malformed requested SolidCraft evidence produces
  `SolidCraftEvidenceError`;
- malformed bodies are never skipped;
- named-body selection requires exactly one match;
- command argv for evaluate/mutate/inspect is exact;
- the adapter imports no Forge/SCPF, SCons or CAD-CI implementation.
