# Changelog

## 0.6.0

- add engine-neutral `verify_visual_view()` for one already-rendered view;
- compose normalization, approved-baseline regression and deterministic diff output;
- optionally create generic expected-geometry goal and overlay evidence;
- preserve complete `VisualViewEvidence` on regression failure;
- keep CAD rendering, view selection, camera conversion, baselines and model policy consumer-owned.


## 0.5.0

- add immutable generic semantic check records;
- compose ordered semantic results with deterministic required-check precedence;
- require a complete passing semantic result with typed failure evidence;
- aggregate already-composed item results without executing work;
- adapt existing verification reports while preserving evidence and artifacts.


## 0.4.0

- add deterministic image normalization and baseline payload encoding/decoding;
- add visual regression metrics and comparison image generation;
- add generic orthographic projection and expected box/hole/slot drawing;
- add independent goal and actual-overlay composition;
- add structured per-view visual evidence with explicit missing states;
- declare Pillow as an explicit dependency.


## 0.3.0

- add CAD-engine-neutral scalar, vector and XYZ-bounds comparison helpers;
- add immutable measured-body envelopes and order-independent one-to-one matching;
- preserve deterministic passing/failing comparison evidence through verify();
- reject invalid numeric values, inverted bounds and negative tolerances explicitly.


## 0.2.0

- add reusable immutable geometry contracts and surface-distance probes;
- add STL mesh loading with typed MeshLoadError failures;
- add bounds, volume, watertightness and nearest-surface probe verification;
- preserve structured passing and failing geometry evidence;
- integrate geometry checks with the existing verification report;
- declare trimesh as an explicit library dependency;
- test the installed built wheel together with its declared dependencies.


## 0.1.0

- add the reusable CAD verification request/check/result model;
- add structured pass, skip, fail and error outcomes;
- validate and hash produced verification artifacts;
- add safe external CAD-command execution with explicit timeout/failure types;
- provide a stable JSON verification report;
- keep CI selection, caching, publication and CAD-engine semantics outside the library.
