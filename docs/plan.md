# Repository plan

This file contains only current unfinished work for
`lib.py.cad.verfication`.

Detailed requirements live in `docs/requirements.md`. Technical design lives
in `docs/design.md`. Issues contain discussion and history. This file is the
single current execution plan.

Completed sections are removed after their PR and release are finished.

## 1. Migrate this repository to Python library CI — #14

Current implementation branch uses:

- `tool.py.lib.ci` 0.1.2;
- exact commit `9045367540102ba2208c517e45a52ddad4bb60ea`;
- the same commit is green in `tool.py.lib.ci.test`.

This step removes the old repository-level CAD-CI wrapper:

- `cad-ci.yml`;
- `ci/library/ci.yml`;
- `scripts/library_ci.py`.

The complete installed-wheel test suite must pass through the released
`tool.py.lib.ci` workflow. Release publication remains after that test job.

Remove this section and close #14 after the new package-test path is green.

## 2. Complete reusable mesh geometry verification — #7

Current implementation PR: #12. This PR is blocked until #14 is complete.

Finish and release the geometry/mesh primitives defined by issue #7:

- immutable geometry contract and surface-distance probes;
- STL loading including measurable multi-part input;
- bounds, volume, watertightness and surface-distance verification;
- `bounds_sufficient=False` guard;
- deterministic structured evidence;
- pass/fail/error handling in the existing verification report;
- built-wheel tests for every R1-R12 requirement.

After the released `tool.py.lib.ci` path is in use and CI passes:

1. merge #12;
2. verify the `0.2.0` release was created from the tested main commit;
3. close #7;
4. remove this section.

## 3. Add numeric and measured-body comparison primitives — #8

Implement the concrete requirements in #8:

- scalar comparison;
- vector comparison;
- bounds comparison;
- order-independent body-envelope matching;
- structured deterministic evidence;
- use with `verify()`;
- no CAD-engine dependency.

Add the corresponding requirements/design/tests before implementation, test the
built wheel, release the next library version, close #8 and remove this section.

## 4. Add visual regression and expected-shape primitives — #9

Implement the concrete requirements in #9:

- deterministic image normalization;
- visual baseline encode/decode;
- pixel regression metrics;
- deterministic diff evidence;
- generic orthographic projection;
- expected-box drawing;
- through-hole and through-slot drawing;
- goal and overlay composition;
- structured visual evidence;
- no model/SolidCraft/CADCraft policy.

Add requirements/design/tests first, declare Pillow explicitly, test the built
wheel, release the next library version, close #9 and remove this section.

## 5. Add semantic verification result composition — #10

Implement the concrete requirements in #10:

- generic semantic check records;
- deterministic overall-status composition;
- evidence/order preservation;
- require-pass validation;
- aggregate composition of already-produced item results;
- adapter from existing verification reports;
- no Forge-specific check names;
- no CAD-CI publication/materialization behavior.

Add requirements/design/tests first, test the built wheel, release the next
library version, close #10 and remove this section.

## 6. Final reusable-verification audit — #4

After #7, #8, #9 and #10 are released:

- compare the implemented library against the complete historical ownership map
  in #4;
- confirm every generic historical verification mechanic has either moved to
  this library or has an explicit non-library owner;
- confirm all public APIs are documented;
- confirm all requirement-to-test mappings are present and green against built
  wheels;
- confirm repositories only need released library versions.

Close #4 when this audit passes and remove this section.

Forge-specific migration remains tracked in
`lib.py.solidcraft.forge#378` and is not duplicated in this repository plan.

## Open issue assessment — 2026-11-19

| Issue | Status | Assessment |
| --- | --- | --- |
| #14 Create and adopt tool.py.lib.ci for Python library CI | now | The repository is being migrated to tested tool.py.lib.ci 0.1.2; the old CAD-CI wrapper is removed on the current branch. |
| #7 Add reusable geometry and independent-reference verification primitives | blocked / next | PR #12 exists and is green, but merge/release waits for #14 so it is verified through the correct Python-library CI path. |
| #8 Add reusable numeric and measured-body comparison primitives | next after #7 | Required reusable comparison layer for Forge verification. |
| #9 Add reusable visual regression and expected-shape overlay primitives | next after #8 | Required to restore Forge visual/baseline/goal evidence without Forge-specific generic code. |
| #10 Add reusable semantic verification result composition | next after #9 | Required for deterministic aggregate verification results/fan-in. |
| #4 Expand reusable CAD verification mechanics beyond the foundation | final audit | Close only after #7/#8/#9/#10 are released and the historical ownership map is fully accounted for. |

Immediate execution chain:
`#14 -> #7 -> #8 -> #9 -> #10 -> #4`.

Forge #378 remains blocked until the required released verification capabilities
from this chain exist.

