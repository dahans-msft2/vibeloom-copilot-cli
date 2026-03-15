# Command Surface Reference

This file defines the runtime command grammar consumed by the skill.

- `docs/` owns methodology truth.
- This file owns parsing, normalization, and examples for the runtime interface.

## Grammar

Canonical commands start with:

```text
/vibeloom <verb> <noun> [tail]
```

Rules:
- `<verb>` is required
- `<noun>` is required unless the user invoked bare `$vibeloom`
- `[tail]` is freeform
- if `<noun>` is missing, return the valid grammar for that verb instead of guessing
- normalize official aliases before routing
- use canonical forms in responses after normalization

## Core Commands

| Command | Meaning |
| --- | --- |
| `/vibeloom init project [intent seed]` | Initialize a governed project |
| `/vibeloom import repo [path-or-current]` | Bootstrap governance for an existing repo |
| `/vibeloom status repo` | Report overall governed state |
| `/vibeloom status artifact <selector>` | Report one canonical artifact |
| `/vibeloom status module <module-name>` | Report one module |
| `/vibeloom review artifact <selector>` | Review one artifact |
| `/vibeloom review module <module-name>` | Review one module |
| `/vibeloom develop change <request>` | Run feature or enhancement flow |
| `/vibeloom fix issue <repro-or-bug>` | Run bugfix flow |
| `/vibeloom reconcile repo` | Reconcile repo-wide drift |
| `/vibeloom reconcile artifact <selector>` | Reconcile one artifact |
| `/vibeloom reconcile module <module-name>` | Reconcile one module |

## Expert Commands

| Command | Meaning |
| --- | --- |
| `/vibeloom generate artifact <selector>` | Generate a canonical or derived artifact |
| `/vibeloom approve scope <selector>` | Approve an allowed scope |
| `/vibeloom eval scope <selector>` | Evaluate an allowed scope |
| `/vibeloom use surface <product-first|code-first>` | Set the current session surface |
| `/vibeloom help command <verb>` | Explain one verb |
| `/vibeloom help topic <methodology|profiles|surfaces|evals|templates|commands>` | Load one guided documentation topic |

## Selectors

### Artifact Selectors

Canonical selectors:
- `constitution`
- `intent`
- `prd`
- `usm`
- `dm`
- `spec`

Derived selectors for generation only:
- `module-spec`
- `agents`
- `plan`

### Scope Selectors

Allowed values:
- `intent`
- `product`
- `spec`
- `module`
- `change`
- `repo`
- `artifact`

## Aliases

Official command aliases:
- `/vibeloom init [intent seed]` -> `/vibeloom init project [intent seed]`
- `/vibeloom import [path-or-current]` -> `/vibeloom import repo [path-or-current]`
- `/vibeloom status` -> `/vibeloom status repo`
- `/vibeloom develop <request>` -> `/vibeloom develop change <request>`
- `/vibeloom reconcile` -> `/vibeloom reconcile repo`
- `/vibeloom approve <selector>` -> `/vibeloom approve scope <selector>`
- `/vibeloom eval <selector>` -> `/vibeloom eval scope <selector>`

Selector and scope aliases:
- `product` -> `prd+usm+dm`
- `tech` -> `spec`
- `module-spec` -> module-scoped spec generation

No shorthand aliases exist for `review`, `help`, `fix`, or `generate`.

## Bare Invocation

Bare `$vibeloom` with no command returns:
- current governed state
- current surface
- blocking issues
- profile when available
- next 3 valid commands

## Corrections

When a command is malformed:
- state the invalid segment
- show the closest valid form
- show the exact expected syntax for that verb

## Examples

```text
/vibeloom status repo
/vibeloom status
/vibeloom review artifact usm
/vibeloom develop change add workspace sharing with invite approval
/vibeloom develop add workspace sharing with invite approval
/vibeloom fix issue invite links expire one hour too early
/vibeloom eval scope module billing
/vibeloom eval module billing
/vibeloom use surface code-first
/vibeloom approve scope product
```
