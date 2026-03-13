# Routing And Loading Reference

This file defines what to load for each command and how to choose the next valid action.

## State Detection

Inspect the current repo for:
- canonical artifacts
- frontmatter status
- selected profile
- module specs
- stale markers
- current worktree state relevant to governed files

## Bare Triage

Return:
- current state
- blockers
- next 3 valid commands

Recommended next commands by state:

| State | Next commands |
| --- | --- |
| No governed project | `init project`, `import repo`, `help command init` |
| Intent draft | `review artifact intent`, `eval scope artifact intent`, `approve scope intent` |
| Product drafts | `review artifact prd`, `review artifact usm`, `approve scope product` |
| Spec draft | `review artifact spec`, `eval scope spec`, `approve scope spec` |
| Governed active repo | `status repo`, `develop change ...`, `fix issue ...` |
| Drift detected | `reconcile repo`, `reconcile artifact <name>`, `eval scope repo` |

## Profile Selection Heuristic

After product specs are approved (`approve scope product`), run this algorithm to propose a profile:

1. Load `dm.md` and analyze its structure.
2. Count bounded contexts and total entities.
3. Apply the decision rule:
   - **Single BC** with **≤ 15 entities** → propose **Lite**
   - **Multiple BCs** or **> 15 entities** → propose **Full**
4. Present the proposal to the user with a summary of the counts.
5. User confirms or overrides.
6. Store the chosen profile in `.vibeloom/state.md` under `profile`.

This heuristic runs automatically as part of the `approve scope product` flow. It does not run during `import repo` (which has its own profile proposal step).

## Command Routing

### `init project`

Load:
- `references/methodology.md`
- `references/evals-and-templates.md`
- templates for `intent`

### `import repo`

Load:
- `references/methodology.md`
- `references/routing-and-loading.md`
- `references/evals-and-templates.md`
- import-related sections from `../spec.md`

### `status`

Load:
- current artifact frontmatter
- dependency or stale indicators if present
- module selectors if the noun is `module`

### `review artifact prd|usm`

Load:
- `references/interaction-contract.md`
- the target artifact
- linked upstream items
- relevant `dm` slice only when needed to explain implied entities

### `review artifact dm|spec`

Load:
- `references/interaction-contract.md`
- the target artifact
- linked upstream `usm` or `prd` items
- relevant module or interface slices

### `develop change`

Load:
- `references/methodology.md`
- `references/routing-and-loading.md`
- `references/evals-and-templates.md`
- current governed slice selected from trace and artifact dependencies

### `fix issue`

Load:
- `references/methodology.md`
- `references/interaction-contract.md`
- current governed slice for the bug area
- regression-relevant eval guidance

Do not load import bootstrap guidance unless the repo is unmanaged or explicitly requested.

### `reconcile`

Load:
- `references/methodology.md`
- `references/interaction-contract.md`
- current artifact statuses
- the smallest affected slice plus dependency implications

### `generate`, `approve`, `eval`

Load:
- `references/evals-and-templates.md`
- only the target templates or eval docs needed for the requested scope

## Selector Resolution

For invalid artifact or module selectors:
- inspect repo files and module directories
- return explicit valid selectors
- do not invent missing modules or artifacts
