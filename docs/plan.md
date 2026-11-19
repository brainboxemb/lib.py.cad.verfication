# Repository plan

This file contains only current unfinished work for
`lib.py.cad.verfication`.

Detailed requirements live in `docs/requirements.md`. Technical design lives
in `docs/design.md`. Issues contain discussion and history. This file is the
single current execution plan.

Completed sections are removed after their PR and release are finished.

## 1. Complete reusable mesh geometry verification — #7

Current implementation PR: #12.

Finish and release the geometry/mesh primitives defined by issue #7:

- immutable geometry contract and surface-distance probes;
- STL loading including measurable multi-part input;
- bounds, volume, watertightness and surface-distance verification;
- `bounds_sufficient=False` guard;
- deterministic structured evidence;
- pass/fail/error integration with the existing verification report;
- built-wheel tests for every R1-R12 requirement.

After CI passes:

1. merge #12;
2. verify the `0.2.0` release was created from the tested main commit;
3. close #7;
4. remove this section.

## 2. Add numeric and measured-body comparison primitives — #8

Implement the concrete requirements in #8:

- scalar comparison;
- vector comparison;
- bounds comparison;
- order-independent body-envelope matching;
- structured deterministic evidence;
- integration with `verify()`;
- no CAD-engine dependency.

Add the corresponding requirements/design/tests before implementation, test the
built wheel, release the next library version, close #8 and remove this section.

## 3. Add visual regression and expected-shape primitives — #9

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

## 4. Add semantic verification result composition — #10

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

## 5. Final reusable-verification audit — #4

After #7, #8, #9 and #10 are released:

- compare the implemented library against the complete historical ownership map
  in #4;
- confirm every generic historical qualification mechanic has either moved to
  this library or has an explicit non-library owner;
- confirm all public APIs are documented;
- confirm all requirement-to-test mappings are present and green against built
  wheels;
- confirm consumers only need released library versions.

Close #4 when this audit passes and remove this section.

Consumer-specific Forge migration remains tracked in
`lib.py.solidcraft.forge#378` and is not duplicated in this repository plan.
