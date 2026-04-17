# Runtime Reference

Dispatch mechanics for the skill. Authoritative semantics live in [`vibeloom-implementation.md`](../vibeloom-implementation.md). This file is a load-on-demand condensation focused on what the orchestrator needs at runtime.

---

## Runtime loop

Every operation follows the same high-level loop:

1. Load only the minimal planning state needed for the current operation.
2. Compute the affected set and build the initial dispatch plan from accepted state.
3. Dispatch the current ready set as scoped subagent tasks when decomposition is useful.
4. Validate subagent results from summaries plus allowed spot reads.
5. If a task surfaces one narrow missing dependency, re-invoke that task once with an approved late-fetch slice.
6. Accept successful task results, retire superseded ones, recompute the remaining dispatch plan, and continue to the next ready set.
7. Finish any shared/root/orchestrator-local work and return target-level findings or outputs.

---

## Subagent execution contract

Subagents are a general execution primitive for scoped `import`, `generate`, `eval`, `review`, `reconcile` work when decomposition is useful.

Two modes:

- **read-only analysis** — scoped `import` analysis, `eval`, advisory `review`, drift analysis inside `reconcile`. No write scope.
- **write-capable generation / reconciliation** — contract, context, code generation; bounded-fix phases of `review`; fix phases of `reconcile`. Explicit write scope.

Each invocation starts from a fresh prompt built from:

- the task header (operation + target + scope + objective + write permissions + prerequisites + validation contract + result-shape)
- the scoped load set (baseline + owned scope + foreign slice + relevant context)
- minimal accepted prior-wave summaries needed for prerequisites or unresolved findings

Subagents may not treat same-wave outputs as input. Same-wave outputs become eligible inputs only after the wave is accepted and the dispatch plan is recomputed.

---

## Parallel dispatch

### Contract tiers

Sequential across tiers, but three phases inside a tier:

1. **Root forward-back pass** — root artifacts generate in dependency order (e.g., `prd` → `usm` → `dm`). Back-pass reopens affected earlier artifacts until stable.
2. **Container wave** — affected `container.md` files generate in parallel. Writes disjoint by directory.
3. **Component wave** — affected `component.md` files generate in parallel after the container wave completes. `component.md` reads its own `container.md` (per DAG), so the component wave follows container wave.

### Context

Single parallel wave:

- one task for root config
- one task per affected container config
- one task per affected component — generates both component config and any component-scoped `bdd` in one invocation (shared load set and write scope)

Decision-ledger writes (`pdr`, `adr`) are orchestrator-local, not subagent tasks.

### Code

Dependency-aware waves. Wave computation:

- a component can join the current wave when all its `DEP-####` references resolve to components in already-completed waves (or to none)
- its `owned_paths` are disjoint from every other component's `owned_paths` in the same wave

Computed by topological sort over `DEP-####` → `IF-####` edges. Once a wave completes and cross-scope validation passes, the orchestrator recomputes and dispatches the next ready set.

### Post-wave validation

After each wave, the orchestrator validates from accepted summaries + targeted spot reads:

- interface contracts declared in component specs are satisfied
- dependency references resolve to actual generated outputs
- no conflicting file writes or write-scope violations

If validation fails and failing outputs can be localized, only affected tasks are reopened. If the failure is cross-cutting or ownership-ambiguous, surface findings and stop.

---

## Context loading

### Orchestrator

Loads: skill instructions, status snapshot, graph cache, and only the artifacts needed for planning. After dispatch, retains graph + status + dispatch plan + subagent summaries. Reopens artifacts only for targeted spot validation.

### Subagent load sets (full modes)

| Subagent scope | Baseline | Owned scope | Referenced foreign slice | Relevant context |
|---|---|---|---|---|
| component | root config + `defaults` | component + container config, component spec, container spec, relevant `system`/`containers` summary | directly referenced IF/DEP snippets from siblings or cross-container | component-scoped `bdd`, intersecting `pdr`/`adr` records |
| container | root config + `defaults` | container config, container spec, `system`, `containers`, affected component inventory summary | directly referenced cross-container IF/DEP snippets | intersecting `pdr`/`adr` records |
| root | root config + `defaults` | target root artifact(s), `system`, `containers` as needed | targeted downstream summaries when required for planning/merge | intersecting `pdr`/`adr` records |

### Subagent load sets (vibe)

All subagents load root config + `defaults` + approved `intent.md` as baseline. If internal component-level dispatch is used, each subagent also receives the targeted component slice from flat `system.md` plus directly referenced compact IF/DEP excerpts. If the compact inventory is too ambiguous for safe partitioning, fall back to single-agent execution.

### Operation overlays

Scope base is filtered by operation:

- **contract gen / eval / review** — contract target + approved upstream basis; omit `bdd`; include config only when validation explicitly depends on it
- **context gen / eval / review** — governing contract slice + context artifacts at the target scope
- **code gen / eval / review / reconcile** — contract + config + relevant context + foreign dependency slice
- **import analysis** — code + inferred-scope hints + minimal reconstruction guidance; no generated context artifacts as inputs

### Intent is not a subagent load

Intent persistence is orchestrator-level, not a subagent concern. Once each tier is approved, it captures everything downstream needs. Subagents work from the approved contract slice. If a subagent would need intent directly, that signals insufficient upstream capture — fix the contract, not the load set.

---

## Late-fetch

A subagent may surface a late-fetch request in its result summary when it discovers a narrow missing dependency. The orchestrator evaluates:

- if a slice can be supplied without broadening the subagent's ownership or write scope, the orchestrator re-invokes the same task once with the additional slice added to its fresh prompt
- if the re-invocation's result summary still requests missing slices, the orchestrator treats this as a finding and exits the task

At most **one late-fetch re-invocation per task**.

---

## Spot reads

Spot reads are targeted rereads of specific files triggered by a concrete validation need. Typical triggers:

- verifying a reported interface/provider match
- inspecting a file implicated by a failed validation
- inspecting a file in a declared write set
- inspecting a file or artifact referenced by an unresolved finding

Broad rereads of whole scopes or entire waves are not part of normal execution. If a broad reread seems necessary, surface findings and stop rather than silently expand context.

---

## Context efficiency

The implementation does not promise a fixed token budget. Efficiency comes from four mechanisms:

- **targeted slices** — subagents receive only the contract + context intersecting their scope
- **one-template-at-a-time loading** — the agent loads one template per artifact, unloading between artifacts
- **bounded late-fetch** — at most one re-invocation per task
- **dependency-aware waves** — subagents share a wave only when write scopes are disjoint and declared dependencies are already satisfied

For reference, a component subagent typically receives 6–12K tokens of contract + config + context slice.

---

## Accepted state

`accepted` is operation-local runtime state, not artifact metadata:

- for write-capable tasks, an accepted result is a validated set of writes retained in the active operation state
- for read-only tasks, an accepted result is a validated scoped findings/evidence package
- accepted is distinct from `approved`
- superseded accepted results are retired from the active plan

Dispatch plans and subagent summaries are ephemeral by default. They are not governed repo truth and are not normal prompt inputs outside the current operation.

---

## Orchestrator writes

The orchestrator may write only:

- shared/root/runtime artifacts
- decision ledgers (`pdr`, `adr`)
- `.vibeloom/` runtime state

Component-owned outputs are changed only through subagent rerun/reconcile flow, not direct orchestrator patching.
