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
