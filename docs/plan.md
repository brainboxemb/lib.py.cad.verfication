# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verification`.

## Current status

Release 0.10.0 contains the SolidCraft adapter, declarative SolidCraft
verification and partial timeline expectations.

Forge's measured cold simple-box path now shows runtime packaging—not
verification logic—is the dominant cost:

- immutable SolidCraft image pull: 13.307 s in the latest clean run;
- container start to entry shell: 7.480 s;
- actual in-runtime verification: 0.747 s.

The package root currently imports geometry and visual modules eagerly even
when a consumer requests only the SolidCraft API. That unnecessarily couples
SolidCraft-only runtime packaging to geometry/visual dependencies.

## Current goal

Complete #49 as release 0.10.1 by keeping the existing top-level public API
while loading geometry and visual implementation modules only when one of their
public names is requested.

Dependency declarations are intentionally unchanged in this issue.

## Required proof

- isolated import of the public SolidCraft API succeeds while imports of
  trimesh and Pillow are deliberately blocked;
- geometry and visual implementation modules are absent from sys.modules after
  that SolidCraft-only import;
- existing top-level geometry and visual names still resolve correctly;
- all existing library tests remain green;
- release 0.10.1 points to the exact tested main commit.

## Execution order

1. Complete and release #49.
2. Let docker.cad.solidcraft consume exact 0.10.1 and independently define a
   lean SolidCraft role dependency set.
3. Measure the resulting immutable image cold pull/start.
4. Only then update Forge #484 to the new runtime release.
5. Complete #44/#45 later when staged model migration reaches those contracts.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #49 Avoid loading geometry and visual stacks for SolidCraft-only verification | now | Required import boundary before the SolidCraft runtime can safely omit unrelated heavy packages. |
| #48 Replace remaining lib.py.cad.verfication repository-name references | later | Naming/documentation cleanup; unrelated to runtime performance. |
| #44 Allow partial SolidCraft parameter expectations | next | Required only before a model needs subset parameter checks. |
| #45 Allow partial SolidCraft sketch expectations | next | Required only before a model needs subset sketch checks. |

Immediate chain:
`#49 lazy imports -> lean docker.cad.solidcraft role -> Forge #484 timing`.
