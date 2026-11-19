# Repository plan

This file contains only current unfinished work for
`lib.py.cad.verfication`.

Detailed requirements live in `docs/requirements.md`. Technical design lives
in `docs/design.md`. Issues contain discussion and history. This file is the
single current execution plan.

Completed sections are removed after their PR and release are finished.

## 1. Create and adopt generic Python library CI — #14

Create and independently qualify:

```text
brainboxemb/tool.py.lib.ci
```

This tool is the generic CI layer for ordinary Python libraries. It must not
depend on CAD-CI or SCons.

Initial responsibilities:

- checkout exact consumer source;
- set up the requested Python version;
- build exactly one wheel;
- install that wheel and declared dependencies in a clean environment;
- run the consumer's complete unit-test suite against the installed wheel;
- expose clear test/build status;
- permit release only after green main CI.

Initial non-goals:

- SCons;
- CAD item selection;
- CAD dependency graphs;
- CAD build/Pages publication;
- Forge/SolidCraft policy;
- GitHub Actions cache.

After `tool.py.lib.ci` is tested and released:

1. create/use `tool.py.lib.ci.test`;
2. pin that exact released tool revision there;
3. black-box prove wheel build, clean install, pass/fail behavior and absence of
   SCons/cache/CAD-CI state.

Only after that acceptance passes:

- replace this repository's current `tool.cad.ci` workflow dependency;
- delete `cad-ci.yml` and `ci/library/ci.yml`;
- confirm CI logs contain no SCons and no `actions/cache`;
- run this library's complete installed-wheel suite through the released
  `tool.py.lib.ci`;
- remove this section when #14 is complete.

## 2. Complete reusable mesh geometry verification — #7

Current implementation PR: #12. This PR is blocked until #14 is complete.

Finish and release the geometry/mesh primitives defined by issue #7:

- immutable geometry contract and surface-distance probes;
- STL loading including measurable multi-part input;
- bounds, volume, watertightness and surface-distance verification;
- `bounds_sufficient=False` guard;
- deterministic structured evidence;
- pass/fail/error integration with the existing verification report;
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
- integration with `verify()`;
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
- confirm every generic historical qualification mechanic has either moved to
  this library or has an explicit non-library owner;
- confirm all public APIs are documented;
- confirm all requirement-to-test mappings are present and green against built
  wheels;
- confirm consumers only need released library versions.

Close #4 when this audit passes and remove this section.

Consumer-specific Forge migration remains tracked in
`lib.py.solidcraft.forge#378` and is not duplicated in this repository plan.
