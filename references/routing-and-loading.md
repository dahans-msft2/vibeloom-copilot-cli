# Routing And Loading Reference

This file defines what to load for each command and how to choose the next valid action.

## State Detection

Inspect the current repo for:
- canonical artifacts
- frontmatter status
- selected profile
- module specs
- stale markers
- last meaningful eval summary when present
- current worktree state relevant to governed files

## Bare Triage

Bare `$vibeloom` is a smart entry point. Detect the governed state first, then route the user toward the next safe command instead of dumping the full command catalog.

Return:
- current state
- blockers
- profile when known
- next 3 valid commands

Recommended next commands by state:

| State | Next commands |
| --- | --- |
| No governed project | `init project`, `import repo`, `help command init` |
| Intent draft | `review artifact intent`, `eval scope intent`, `approve scope intent` → triggers sequential product generation |
| Product drafts | `review artifact prd`, `review artifact usm`, `approve scope product` |
| Spec draft | `review artifact spec`, `eval scope spec`, `approve scope spec` |
| Governed active repo | `status repo`, `develop change ...`, `fix issue ...` |
| Drift detected | `reconcile repo`, `reconcile artifact <name>`, `eval scope repo` |

### Post-Intent Approval: Sequential Product Generation

When `approve scope intent` succeeds:

1. Generate `prd.md` from the approved intent
2. Generate `usm.md` from the approved intent + generated PRD
3. Generate `dm.md` from the approved intent + generated PRD + generated USM

Each artifact is generated sequentially — the next uses the previous as input. All three are created in `draft` status. The agent does not pause for intermediate approvals between them.

The next valid command after generation completes is `approve scope product`, which evaluates and approves all three as a batch (`prd + usm + dm`).

When the state is incomplete or ambiguous:
- prefer the narrowest next command that resolves the ambiguity
- recommend `help topic profiles` before guessing a profile
- recommend `review artifact dm` before proposing new module boundaries

When possible, present each suggested next command with one short reason.

## Profile Selection Heuristic

After `approve scope product`, propose a profile using the current approved product slice:

1. load `dm.md`
2. count bounded contexts and total entities
3. propose `lite` when there is one bounded context and roughly <= 15 entities
4. propose `full` when there are multiple bounded contexts, ambiguous ownership, or a larger entity surface
5. show the counts and the reasoning in the response
6. let the user confirm or override

This heuristic is session-local and recommendation-only. Do not persist profile choice to any external state file.

## Command Routing

### `init project`

Load:
- `references/methodology.md`
- `references/evals-and-templates.md`
- templates for `intent`
- the overview sections of `../docs/vibeloom-methodology.md`

If the freeform seed is missing, short, or obviously incomplete, enter a brief init interview and gather:
- system goal
- project type
- expected scope size and expected lifetime
- primary users
- hard constraints
- first success signal
- whether the repo is greenfield or brownfield
- likely bounded contexts if the workflows already imply them

Useful prompt wording:
- What are you building?
- Is this a small single-context product, or do you expect several major capability areas?
- Who are the primary users?
- What are the 3-5 most important outcomes?
- Are there technologies you want to use or avoid?
- Are there scale, performance, compliance, or platform constraints?
- Does this need to stay small, or do you expect a larger long-lived codebase with multiple ownership boundaries?

Draft `intent.md` first. Do not infer downstream approvals or a profile automatically.
If a provisional profile recommendation is useful, explain it as session-local guidance only and wait for product approval before treating it as selected.

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
- latest structural and semantic summaries if already present in repo-tracked artifacts or the current session
- module selectors if the noun is `module`

Present:
- profile
- artifact health
- module and interface warnings when relevant
- blockers
- next 3 valid commands

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

Execute conceptually as:
1. one up-pass against upstream truth
2. one down-pass through affected downstream artifacts
3. one final structural validation

Do not loop indefinitely.

### `generate`, `approve`, `eval`

Load:
- `references/evals-and-templates.md`
- only the target templates or eval docs needed for the requested scope

### `help topic`

Load only the relevant reference set:
- `methodology` -> `../docs/vibeloom-methodology.md`
- `profiles` -> `../docs/profile-selection.md`
- `evals` -> `../eval/structural-checks.md`, `../eval/semantic-checks.md`
- `templates` -> `../templates/`
- `commands` -> `references/command-surface.md`

## Selector Resolution

For invalid artifact or module selectors:
- inspect repo files and module directories
- return explicit valid selectors
- do not invent missing modules or artifacts
