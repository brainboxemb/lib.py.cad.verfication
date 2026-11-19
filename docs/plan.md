# Repository plan

This file is the current source of truth for unfinished work in
`lib.py.cad.verfication`.

## Current status

Release 0.10.0 is published and contains:

- the SolidCraft CAD-tool adapter;
- declarative SolidCraft model verification;
- partial timeline expectations.

The pre-migration Forge audit found two additional contract gaps. They do not
block the first simple-box proof, but must be resolved in this library before a
Forge model that depends on those semantics is migrated.

## Execution order

1. Let Forge prove the released declarative path with simple-box.
2. Complete #44 before migrating a model that verifies only a subset of native
   parameters.
3. Complete #45 before migrating a model that verifies only selected sketch
   properties.
4. Release each behavior before the corresponding Forge consumer adopts it.
5. Do not add local Forge workarounds for either gap.

## Open issue assessment — 2026-11-20

| Issue | Status | Assessment |
| --- | --- | --- |
| #46 Restore repository plan after SolidCraft expectation audit | now | Administrative update required because #44/#45 reopened unfinished library work. |
| #44 Allow partial SolidCraft parameter expectations | next | Same contract principle as partial timeline fields; implement when the staged Forge migration reaches a model that needs subset parameter checks. |
| #45 Allow partial SolidCraft sketch expectations | next | Prevents incidental profile/curve values becoming fake model contracts; implement before an affected Forge model migrates. |

Immediate chain:
`Forge simple-box proof -> #44/#45 as required by staged model migration`.
