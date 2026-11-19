# Changelog

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
