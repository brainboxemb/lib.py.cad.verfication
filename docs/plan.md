# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

Release `0.14.0` is complete and Forge has completed the procedural-to-
declarative model-verification migration against it.

Forge #378 has now been reopened because full-catalog visual verification was
never completed. The existing generic visual API supports expected boxes,
through-holes and straight through-slots, but one historical Forge model
(`slot-family`) requires a generic through-slot whose centerline contains more
than two points.

Forge must not reimplement that generic outline/projection mechanic.

## Current goal

Complete #75 and release the smallest compatible visual primitive needed for
polyline/arc slot expected-shape evidence.

## Required proof

- expose one frozen generic path-slot expected-shape type;
- centerline contains at least two finite XY points;
- neighbouring duplicate points are rejected;
- width is positive and Z range is ordered;
- two-point input is geometrically compatible with the existing straight
  `ThroughSlot`;
- deterministic tangent-normal outline generation matches the historical
  consumer-independent semantics;
- expected-geometry drawing, goal/overlay generation and
  `verify_visual_view()` accept the new type;
- existing `ThroughSlot` behavior is unchanged;
- the new public symbol is lazy at the package root;
- installed-wheel CI passes;
- publish an immutable release for Forge #378 to consume.

## Execution order

1. [#75, now] Define path-slot behavior in requirements/design.
2. Add visual primitive/drawing/view-evidence tests.
3. Implement the smallest generic type and drawing support.
4. Release the next immutable verification-library version.
5. Resume Forge #378 full-catalog visual verification.

## Open issue assessment — 2026-11-21

| Issue | Status | Assessment |
| --- | --- | --- |
| #75 Support polyline through-slot expected-shape evidence | now | Generic blocker for Forge #378 slot-family visual expected-shape parity. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup unrelated to the Forge visual blocker. |

Immediate chain:
`#75 path-slot visual primitive -> verification-library release -> Forge #378`.
