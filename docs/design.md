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

## 10. Consumer adapter boundary

A consumer check may call an engine directly:

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

The literal SolidCraft command belongs in Forge, not in this library.

Likewise geometry expectations such as body counts, bounds and parameter
values stay in Forge.

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
