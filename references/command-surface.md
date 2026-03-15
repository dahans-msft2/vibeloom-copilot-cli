# Command Surface Reference

This file defines the runtime command grammar consumed by the skill.

- `docs/` owns methodology truth.
- This file owns parsing, normalization, and examples for the runtime interface.

## Grammar

Canonical commands follow the conceptual shape:

```text
/vibeloom <action> <target> <context>
```

Rules:
- `<action>` is required
- `<target>` identifies the object, scope, or mode when present
- `<context>` carries selectors, names, or freeform request details when present
- each action has one documented surface shape
- some actions omit the target or context token when the meaning is unambiguous
- normalize documented target expansions before routing
- if a required target or context segment is missing, return the valid grammar for that action instead of guessing
- use canonical forms in responses after normalization

## Core Commands

| Command | Meaning |
| --- | --- |
| `/vibeloom init [intent seed]` | Initialize a governed project |
| `/vibeloom import [path-or-current]` | Bootstrap governance for an existing repo |
| `/vibeloom status` | Report overall governed state |
| `/vibeloom status artifact <selector>` | Report one canonical artifact |
| `/vibeloom status module <module-name>` | Report one module |
| `/vibeloom review <target> [context]` | Review one artifact or module |
| `/vibeloom develop <request>` | Run feature or enhancement flow |
| `/vibeloom fix <repro-or-bug>` | Run bugfix flow |
| `/vibeloom reconcile` | Reconcile repo-wide drift |
| `/vibeloom reconcile artifact <selector>` | Reconcile one artifact |
| `/vibeloom reconcile module <module-name>` | Reconcile one module |

## Expert Commands

| Command | Meaning |
| --- | --- |
| `/vibeloom generate <selector>` | Generate a canonical or derived artifact |
| `/vibeloom approve <target> [context]` | Approve an allowed target |
| `/vibeloom eval <target> [context]` | Evaluate an allowed target |
| `/vibeloom surface <product-first|code-first>` | Set the current session surface |
| `/vibeloom help command <action>` | Explain one action |
| `/vibeloom help <methodology|profiles|surfaces|evals|templates|commands>` | Load one guided documentation topic |

## Targets And Selectors

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

### Review Targets

Allowed values:
- `constitution`
- `intent`
- `prd`
- `usm`
- `dm`
- `spec`
- `module`

`module` requires the module name in the command context:
- `/vibeloom review module <module-name>`

### Approval Targets

Allowed values:
- `intent`
- `product`
- `spec`
- `module`
- `change`

`module` requires the module name in the command context:
- `/vibeloom approve module <module-name>`

### Eval Targets

Allowed values:
- `intent`
- `product`
- `spec`
- `module`
- `change`
- `repo`
- `artifact`

Target forms with required context:
- `/vibeloom eval module <module-name>`
- `/vibeloom eval artifact <artifact-selector>`

## Normalization

Target and selector expansions:
- `product` -> `prd+usm+dm`
- `tech` -> `spec`
- `module-spec` -> module-scoped spec generation

Constraints:
- `approve` supports `intent`, `product`, `spec`, `change`, and `module <module-name>`
- `eval` supports `intent`, `product`, `spec`, `change`, `repo`, `artifact <artifact-selector>`, and `module <module-name>`
- `status` supports the repo default plus `status artifact <artifact-selector>` and `status module <module-name>`
- `generate` accepts artifact selectors directly
- `review` accepts canonical artifact targets directly; module review requires `review module <module-name>`
- `develop` accepts freeform feature or enhancement requests
- `fix` accepts freeform repro or bug descriptions
- `help` accepts documented help topics directly; command-specific help uses `help command <action>`

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
- show the exact expected syntax for that action

## Examples

Canonical forms:

```text
/vibeloom status
/vibeloom review usm
/vibeloom develop add workspace sharing with invite approval
/vibeloom fix invite links expire one hour too early
/vibeloom eval module billing
/vibeloom surface code-first
/vibeloom generate dm
/vibeloom approve product
/vibeloom help evals
```
