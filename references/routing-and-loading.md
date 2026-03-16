# Routing And Loading Reference

This file defines what to load for each command and how to choose the next valid action.

- Treat `references/` as the default runtime layer.
- Do not load `docs/` during routine commands unless the user asked for deeper explanation, used `help`, or a runtime rule here explicitly escalates.
- Use canonical command forms in suggested next actions.

## Load Ownership

This file owns exact routine load selection for the skill.

- `constitution.md` and `spec.md` preserve the constraints this file must honor; they do not create a second unconditional `always load` bundle.
- command sections below are authoritative for routine loading
- bootstrap and help commands may skip technical-boundary artifacts when the governed slice does not exist yet or the user asked only for explanation

## Cross-Command Slice Rules

- for artifact review, load the target plus only the linked slice needed to explain findings
- for governed execution or technical change work, load the nearest owning technical boundary, the relevant trace slice when IDs or stale impact are in play, and scoped derived `AGENTS.md` only when it exists and reduces ambiguity
- treat derived `AGENTS.md` as optional execution guidance, never as semantic authority
- do not widen to unrelated modules, bounded contexts, or superseded artifacts unless dependency edges, stale analysis, or explicit historical inspection require it

## State Detection

Inspect the current repo for:
- canonical artifacts
- frontmatter status
- selected profile
- module specs
- stale markers
- current-session eval findings when available
- current worktree state relevant to governed files

## Bare Triage

Bare `$vibeloom` is a smart entry point. Detect the governed state first, then route the user toward the next safe command instead of dumping the full command catalog.

Return:
- current state and surface
- blockers
- profile when known
- next 3 valid commands

Recommended next commands by state:

| State | Next commands |
| --- | --- |
| No governed project | `init`, `import`, `help command init` |
| Intent draft | `review intent`, `eval intent`, `approve intent` → triggers sequential product generation |
| Product drafts | `review prd`, `review usm`, `approve product` |
| Spec draft | `review spec`, `eval spec`, `approve spec` |
| Governed active repo | `status`, `develop ...`, `fix ...` |
| Drift detected | `reconcile`, `reconcile <selector>`, `eval repo` |

### Post-Intent Approval: Sequential Product Generation

When `approve intent` succeeds:

1. Generate `prd.md` from the approved intent
2. Generate `usm.md` from the approved intent + generated PRD
3. Generate `dm.md` from the approved intent + generated PRD + generated USM

Each artifact is generated sequentially — the next uses the previous as input. All three are created in `draft` status. The agent does not pause for intermediate approvals between them.

The next valid command after generation completes is `approve product`, which evaluates and approves all three as a batch (`prd + usm + dm`).

When the state is incomplete or ambiguous:
- prefer the narrowest next command that resolves the ambiguity
- recommend `help profiles` before guessing a profile
- recommend `review dm` before proposing new module boundaries

When possible, present each suggested next command with one short reason.

## Profile Selection Heuristic

After `approve product`, propose a profile using the current approved product slice:

1. load `dm.md`
2. inspect bounded contexts, ownership seams, interface needs, and expected coordination risk
3. propose `lite` when the semantics fit one cohesive bounded context and one module can own the write surface safely
4. propose `full` when there are multiple bounded contexts, ambiguous ownership, stable interface needs, or meaningful parallel execution risk
5. show the reasoning in the response; include bounded-context or entity counts only as supporting evidence when helpful, not as thresholds
6. let the user confirm or override

This heuristic is session-local and recommendation-only. Do not persist profile choice to any external state file.

## Command Routing

### `init`

Load:
- `references/methodology.md`
- `references/evals-and-templates.md`
- templates for `intent`

If the freeform seed is missing, short, or obviously incomplete, enter a brief init interview and gather:
- system goal
- expected scope size and expected lifetime
- primary users
- hard constraints
- first success signal
- whether the repo is greenfield or brownfield
- likely bounded contexts if the workflows already imply them

Draft `intent.md` first. Do not infer downstream approvals or a profile automatically.
If the operator asks for methodology background before answering, escalate to `../docs/vibeloom-methodology.md`.
If a provisional profile recommendation is useful, explain it as session-local guidance only and wait for product approval before treating it as selected.

### `import`

Load:
- `references/methodology.md`
- `references/evals-and-templates.md`
- the current repo evidence needed for inference, such as code, tests, schemas, routes, configs, and existing docs

Purpose:
- bootstrap an unmanaged or heavily drifted repo into draft governance

Behavior:
1. inspect code, tests, schemas, routes, configs, and docs
2. infer draft `intent.md`, `prd.md`, `usm.md`, `dm.md`, and `spec.md`
3. attach confidence signals or equivalent uncertainty markers to inferred items
4. require human approval before treating the repo as governed

Constraints:
- import is a bootstrap path, not the default path for routine fixes
- low-confidence semantic inferences must remain visible until corrected or approved
- do not present imported drafts as approved truth

### `status`

Load:
- current artifact frontmatter
- the relevant technical boundary only when needed to explain technical blockers, ownership warnings, or module status
- dependency or stale indicators if present
- relevant trace or ownership slices only when they explain a reported blocker or stale edge
- current-session structural and semantic findings when available
- module selectors if the target is `module`

Do not assume any persisted eval-summary artifact. Only the canonical durable projections defined in `constitution.md` are allowed.

Present:
- surface and profile
- artifact health
- module and interface warnings when relevant
- blockers
- next 3 valid commands

In `code-first`, lead with `spec.md`, module, interface, and ownership state; still mention blocking product artifacts explicitly.

### `review constitution`

Load:
- `references/interaction-contract.md`
- the target `constitution.md`
- linked package-level artifacts only when needed to explain a concrete layering, lifecycle, traceability, or profile contradiction

### `review intent`

Load:
- `references/interaction-contract.md`
- the target `intent.md`
- reconciled `CAP-*` capability index entries when present
- linked downstream `prd` items only when the repo already claims item-level intent trace or the operator asks whether the current intent is ready for downstream generation

### `review prd|usm`

Load:
- `references/interaction-contract.md`
- the target artifact
- linked upstream items
- relevant `dm` slice only when needed to explain implied entities

### `review dm|spec`

Load:
- `references/interaction-contract.md`
- the target artifact
- linked upstream `usm` or `prd` items
- relevant module or interface slices

### `review module <module-name>`

Load:
- `references/interaction-contract.md`
- the target module slice
- relevant interface, ownership, and stale-edge context

### `develop`

Load:
- `references/methodology.md`
- `references/evals-and-templates.md`
- current governed slice selected from the nearest owning technical boundary, trace links, and artifact dependencies

In `code-first`, start from spec/module/interfaces and escalate to `prd/usm/dm` on workflow, semantic, interface, NFR, or boundary risk.

### `fix`

Load:
- `references/methodology.md`
- `references/interaction-contract.md`
- the nearest owning technical boundary and current governed slice for the bug area
- regression-relevant eval guidance

Do not load import bootstrap guidance unless the repo is unmanaged or explicitly requested.

### `reconcile`

Load:
- `references/methodology.md`
- `references/interaction-contract.md`
- current artifact statuses
- the smallest affected slice plus dependency implications and relevant trace edges

Execute conceptually as:
1. one up-pass against upstream truth
2. one down-pass through affected downstream artifacts
3. one final structural validation

Do not loop indefinitely.

### `generate`, `approve`, `eval`

Load:
- `references/evals-and-templates.md`
- only the target templates needed for generation

Do not load the detailed eval docs during routine command execution.

### `surface`
Load `references/methodology.md`. Return the selected surface, remind the user it is session-scoped, and suggest 2-3 fitting next commands.

### `help`

Load only the relevant reference set:
- `methodology` -> `../docs/vibeloom-methodology.md`
- `profiles` -> `../docs/profile-selection.md`
- `surfaces` -> `../docs/surface-modes.md`
- `evals` -> `../docs/evals-structural.md`, `../docs/evals-semantic.md`
- `templates` -> `../templates/`
- `commands` -> `references/command-surface.md`

Treat `help` as the primary path for direct `docs/` loading.

## Selector Resolution

For invalid artifact or module selectors:
- inspect repo files and module directories
- return explicit valid selectors
- do not invent missing modules or artifacts
