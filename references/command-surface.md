# Command Surface Reference

This file defines the exact `/vibeloom` command grammar.

## Grammar

All commands start with:

```text
/vibeloom <verb> <noun> [tail]
```

Rules:
- `<verb>` is required
- `<noun>` is required unless the user invoked bare `$vibeloom`
- `[tail]` is freeform
- if `<noun>` is missing, return the valid grammar for that verb instead of guessing

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
| `/vibeloom help command <verb>` | Explain one verb |
| `/vibeloom help topic <methodology|profiles|evals|templates|commands>` | Load one guided documentation topic |

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

Normalize internally:
- `product` -> `prd+usm+dm`
- `tech` -> `spec`
- `module-spec` -> module-scoped spec generation

## Bare Invocation

Bare `$vibeloom` with no command returns:
- current governed state
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
/vibeloom review artifact usm
/vibeloom develop change add workspace sharing with invite approval
/vibeloom fix issue invite links expire one hour too early
/vibeloom eval scope module billing
/vibeloom approve scope product
/vibeloom help topic profiles
```
