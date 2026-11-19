# CAD verification requirements

This document is the product contract for `lib.py.cad.verfication`.
Implementation details belong in `docs/design.md`.

## 1. Scope

The library provides reusable mechanics for verifying one already-selected CAD
model or verification case.

The library is not a CI runner. `tool.cad.ci` remains responsible for
repository selection, SCons execution, dependency ordering, incremental
rebuilds and cache reuse.

A normal consumer flow is:

~~~text
tool.cad.ci
  -> selected item
    -> model_verify step
      -> consumer verification definition
        -> lib.py.cad.verfication
~~~

## 2. Consumer ownership

The consumer owns:

- the verification identifier;
- the model/command input;
- the ordered list of checks;
- engine-specific commands;
- expected values and tolerances;
- mutation/inspection definitions;
- engine-specific environment setup.

The library must not contain Forge, SolidCraft, OpenSCAD or other
engine-specific policy.

## 3. Verification request

One verification request contains:

- a stable verification ID;
- an input path;
- an output directory;
- an optional working directory;
- optional JSON-compatible metadata;
- an ordered list of checks.

The caller explicitly invokes the request. The request must contain at least one
check; an empty verification is invalid and may never produce a passing report.
The library performs no repository discovery or changed-file selection.

## 4. Checks

A check has:

- a stable ID;
- one callable supplied by the consumer.

Checks run in declared order.

A check may:

- pass;
- be skipped with an explicit reason;
- fail with an expected verification failure;
- raise an unexpected error.

A failed or errored check stops later checks. This keeps dependent CAD
operations from running on invalid prerequisite evidence.

The library does not decide whether a check is dirty/current and does not cache
check results.

## 5. Verification status

The complete verification status is:

- `pass`: every executed check passed or was explicitly skipped;
- `fail`: a check reported an expected verification failure;
- `error`: verification infrastructure, artifact validation or an unexpected
  exception failed.

Skipped checks are recorded but do not make the complete verification fail.

## 6. Produced artifacts

A passing or skipped check may declare produced artifacts.

Every declared artifact:

- must exist when the check returns;
- must resolve below the verification output directory;
- may be a regular file or directory;
- may not be a symlink;
- receives deterministic size/hash evidence.

Directory evidence recursively includes lexical relative paths and file hashes,
so nested output changes are visible.

A missing, unsafe or unsupported artifact is an `error`, not a model
verification `fail`.

## 7. External commands

The library provides a small reusable process helper for CAD commands.

It must:

- execute an explicit argv sequence without a shell;
- support a working directory;
- support environment overrides;
- capture stdout and stderr;
- support an optional positive timeout;
- distinguish non-zero exit from timeout;
- never reinterpret timeout/network/authentication failures as a domain result.

The caller remains responsible for command meaning.

## 8. Evidence

Every verification writes one JSON report:

~~~text
<output-dir>/verification.json
~~~

The report records at least:

- schema and schema version;
- verification ID;
- overall status;
- consumer metadata;
- ordered check results;
- per-check status/reason/error;
- produced artifact records.

The report is evidence only. It is not rebuild/cache state.

The report must not use the CAD-CI reserved `.cad-ci` namespace.

## 9. IDs and paths

Verification and check IDs use lowercase engineering names containing letters,
digits, `-` and `_`.

Duplicate check IDs are invalid configuration.

The report path is owned by the library. Consumers may not declare
`verification.json` as a check artifact.

## 10. Error model

The public error model distinguishes at least:

- invalid verification/check configuration;
- expected verification failure;
- missing/unsafe artifact;
- command non-zero exit;
- command timeout;
- unexpected consumer exception.

An expected model mismatch must not be reported as an infrastructure error.
An infrastructure error must not be downgraded to a model mismatch.

## 11. Determinism

Given the same consumer-returned evidence and artifact bytes, structural report
content is stable and JSON keys are emitted in deterministic order.

No wall-clock timestamp participates in the report contract.

Timing may be exposed later only through an explicit design change.

## 12. Non-goals

This library does not provide:

- a CLI tool;
- a second CI runner;
- YAML CI configuration;
- SCons integration;
- GitHub Actions workflows;
- Git selection;
- incremental rebuild decisions;
- cache management;
- build/Pages publication;
- CAD-engine installation or image creation;
- model-specific expected values.

## 13. Initial acceptance

Before the first release, unit tests must prove:

1. ordered passing checks produce a passing report;
2. an explicit skip is recorded and remains successful;
3. an expected failure stops later checks and produces `fail`;
4. an unexpected exception stops later checks and produces `error`;
5. duplicate/invalid IDs are rejected;
6. missing/out-of-root/symlink artifacts produce `error`;
7. file and directory artifact hashes change when content changes;
8. external command success captures output;
9. non-zero command exit and timeout are distinct errors.


## 14. Numeric and measured-body comparison

Public reusable behavior:

- compare one scalar against an expected value with a non-negative tolerance;
- compare equally-sized numeric vectors with one tolerance;
- compare expected/actual XYZ bounds;
- match unordered lists of body envelopes by XYZ bounds.

All inputs are consumer-supplied measurements. No CAD-engine object is accepted.

Evidence must include expected value(s), actual value(s), deltas, tolerance and
pass/fail. A mismatch raises `VerificationFailure`.

Body-envelope matching must prove:

- every expected envelope has one matching actual envelope;
- no unmatched actual envelope remains;
- matching is independent of input ordering.

Tests must prove:

- exact / inside tolerance / on tolerance / outside tolerance;
- invalid numeric values and negative tolerance are rejected;
- vector length mismatch is rejected;
- unordered multi-body matching succeeds;
- missing, extra and mismatched bodies fail;
- evidence is deterministic and survives through `verify()`.

This work is tracked by issue #8.

## 15. Mesh geometry verification

Public API:

```python
GeometryContract
SurfaceDistanceProbe
validate_mesh_geometry(mesh_path, contract)
MeshLoadError
```

`GeometryContract` contains:

- expected min/max XYZ bounds;
- bounds tolerance;
- optional expected volume + volume tolerance;
- optional expected watertightness;
- `bounds_sufficient` flag;
- ordered surface-distance probes.

A probe contains:

- stable label;
- XYZ point;
- expected nearest-surface distance;
- tolerance.

Rules:

- vectors contain exactly three finite numbers;
- tolerances are non-negative;
- max bounds may not be below min bounds;
- volume requires a volume tolerance;
- probe labels are unique;
- when `bounds_sufficient=False`, volume or at least one surface probe is
  required.

STL loading must:

- reject missing, empty, malformed and non-measurable files with
  `MeshLoadError`;
- combine measurable parts when trimesh returns a multi-part Scene;
- declare every required mesh-processing dependency explicitly in the package.
  The current implementation requires `trimesh>=4,<5` and `scipy>=1.12,<2`;
  consumer runtime packages may not be relied on transitively.

Verification always checks bounds and optionally checks volume,
watertightness and probes.

A geometry mismatch raises `VerificationFailure` with all already-evaluated
passing and failing evidence. Loading/infrastructure problems remain errors.

Tests must prove:

- contract/probe validation;
- exact and toleranced bounds;
- volume pass/fail;
- watertight pass/fail;
- probe pass/fail and ordering;
- multi-part mesh envelope;
- bounds-insufficient contract validation;
- `verify()` maps geometry mismatch to fail and load failure to error;
- identical input produces identical evidence;
- no Forge/SolidCraft/reference-CAD dependency exists.

This work is tracked by issue #7.

## 16. Visual regression and expected-shape evidence

The library provides generic image verification and projection/drawing helpers.
It never renders CAD itself.

Generic behavior includes:

1. load an image, convert RGB/RGBA to grayscale and normalize to a requested
   target size;
2. encode/decode deterministic approved baseline payloads;
3. compare normalized current/reference images using:
   - mean absolute pixel difference;
   - changed-pixel fraction above a caller-supplied pixel-difference threshold;
4. create a deterministic diff/comparison image;
5. project consumer-supplied 3D points with an orthographic camera containing
   target, yaw, pitch and distance;
6. draw consumer-supplied expected 3D boxes;
7. draw generic through-hole and through-slot expected features;
8. produce goal and overlay images where the actual render remains visible.

The consumer owns:

- required view names;
- actual CAD rendering;
- model cameras;
- approved baselines;
- model boxes/features;
- image thresholds.

Tests must prove:

- RGB/RGBA normalization and resize;
- baseline encode/decode including compressed and PNG payloads;
- identical/changed image metrics and both independent threshold failures;
- deterministic diff output;
- front projection X-right/Z-up;
- top projection X-right/Y-up;
- valid top/bottom camera basis;
- deterministic expected-box drawing;
- through-hole and through-slot drawing;
- invalid/unknown feature input is rejected;
- goal image contains independent expected geometry;
- overlay preserves actual pixels and adds expected geometry;
- missing baseline/image is distinguishable from pixel mismatch;
- no SolidCraft/CADCraft/model policy is embedded.

This work is tracked by issue #9.

## 17. Semantic verification result composition

The library can compose already-produced verification evidence without
executing CAD work.

A consumer supplies ordered semantic checks containing:

- check name;
- status;
- whether the check is required;
- optional reason;
- JSON-compatible evidence.

Generic statuses are:

```text
pass
fail
error
missing
review
blocked
not-required
skipped
```

Overall status precedence for required checks is:

1. error;
2. fail;
3. incomplete when missing;
4. review;
5. blocked;
6. pass.

Optional `not-required` and `skipped` checks do not fail the result.

The library must:

- preserve consumer check order and evidence;
- validate that a composed result is complete/pass when requested;
- aggregate multiple already-composed item results;
- map existing `verification.json` check records into generic semantic input.

The library must not contain Forge-specific semantic names such as
`native_model`, `saved_design`, `visual` or `reference`; Forge supplies
those names.

Tests must prove every status/precedence rule, evidence/order preservation,
pass validation, aggregation, adapter mapping and absence of CAD-CI publication
logic.

This work is tracked by issue #10.

## 18. Migration completeness

Issue #4 is the migration inventory.

The old Forge qualification stack is split as follows:

- generic scalar/vector/body comparison -> section 14 / issue #8;
- generic STL/mesh validation -> section 15 / issue #7;
- generic visual comparison/projection/overlay -> section 16 / issue #9;
- generic semantic result composition -> section 17 / issue #10;
- model-specific geometry, mutations, cameras, baselines and expected shapes
  remain consumer-owned;
- reference-CAD execution remains consumer-owned;
- CAD-CI selection/materialization/publication remains `tool.cad.ci`;
- diagram rendering and site/report publication remain consumer-owned.

No reusable verification behavior is considered migrated merely because Forge
has a local copy. Each reusable area above must be implemented, tested against
the built wheel and released before Forge consumes it.
