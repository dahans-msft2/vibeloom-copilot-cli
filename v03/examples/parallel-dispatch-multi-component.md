# Example: parallel dispatch across components

A change to `intent.md` cascades through the contract to three independent components. This example shows how the engine assembles a dispatch plan, how a wave runs three subagents in parallel, what the per-task header looks like, and how validation gates fire per task before patches are applied atomically. It is the worked counterpart to [implementation §13](../vibeloom-implementation.md#13-dispatch-and-subagent-execution).

## Scenario

A search system spans three components in two containers:

- `web` (frontend, container `web-app`) — search UI, results page, filters
- `search-api` (backend, container `services`) — query orchestration, ranking
- `indexer` (worker, container `services`) — content ingestion and indexing

The PM adds a new capability: **`CAP-0007: search by tag in addition to text`**. After approving the new intent, the affected set spans all three components — but the components have disjoint owned paths, so they can regenerate in parallel.

## 1. Intent change and approval

```text
$ vim intent.md            # add CAP-0007: search by tag
$ vibeloom review intent-specs
✓ Reviewed; advisory: CAP-0007 should specify case-insensitivity (added).
$ vibeloom approve intent-specs
✓ Approval trace APPROVAL-20260503-001 written.
ℹ Affected downstream:
  product-specs: 3 stale, 2 uncovered
  system-specs:  3 components stale (web, search-api, indexer)
  code:          17 files in 3 components
→ Next: vibeloom generate
```

## 2. Dispatch plan (engine-built)

`vibeloom generate` first asks the engine to compute the dispatch plan. The engine inspects the affected set and builds waves under the rules in [implementation §13.2](../vibeloom-implementation.md#132-wave-assembly-rules):

```yaml
plan_id: PLAN-20260503-002
affected_set: [CAP-0007, FR-0023, STORY-0034, ACC-0089, BC-0002,
               IF-0042, BEH-0031, CMP-0012, CMP-0014, CMP-0017]
waves:
  - wave_id: W1
    scopes:
      - scope_id: product-specs
        owned_paths: ["prd.md", "usm.md", "dm.md"]
        task_template_id: generate-product-specs
    dependencies: []

  - wave_id: W2
    scopes:
      - scope_id: system-specs
        owned_paths: ["system.md", "containers.md"]
        task_template_id: generate-system-specs
    dependencies: [{from: W1, to: W2}]

  - wave_id: W3                                # the parallel wave
    scopes:
      - scope_id: component:web/search
        owned_paths: ["web/src/search/**", "web/tests/search/**"]
        task_template_id: generate-component-code
      - scope_id: component:search-api
        owned_paths: ["search-api/src/**", "search-api/tests/**"]
        task_template_id: generate-component-code
      - scope_id: component:indexer
        owned_paths: ["indexer/src/**", "indexer/tests/**"]
        task_template_id: generate-component-code
    dependencies: [{from: W2, to: W3}]
```

The three component scopes in W3 have **disjoint owned_paths**, so they satisfy the wave-assembly disjointness rule and can run in parallel.

## 3. Wave 3 dispatch — three subagents in parallel

The orchestrator builds three task headers (one per scope) and spawns them concurrently:

```yaml
# header for one of three parallel tasks
task_id: TASK-20260503-014
run_id: RUN-20260503-002
wave_id: W3
template_id: generate-component-code
template_version: 0.3.1
scope:
  scope_id: component:web/search
  kind: component-code
  owned_paths: ["web/src/search/**", "web/tests/search/**"]
load_set_refs:
  contract:
    - web-app/web/component.md          # the component spec for web/search
    - prd.md                            # for FR-0023
    - usm.md                            # for STORY-0034
    - dm.md                             # for BC-0002 (Notes Catalog)
  context:
    - web-app/web/AGENTS.md
    - web-app/web/context/bdd/search.feature
foreign_refs:
  - services/search-api/component.md    # for IF-0042 (the consumed interface)
allowed_read_paths:
  - "web/src/search/**"
  - "web/tests/search/**"
  - "web-app/**/*.md"
  - "services/search-api/component.md"
  - "intent.md"
  - "prd.md"
  - "usm.md"
  - "dm.md"
allowed_write_paths:
  - "web/src/search/**"
  - "web/tests/search/**"
validation_contract:
  - typecheck                           # from validation-registry
  - lint
  - unit
  - contract-conformance
  - bdd
result_shape_id: code-task-summary
budget:
  max_tokens: 80000
  max_wall_ms: 180000
```

The three tasks (`TASK-014` for web, `TASK-015` for search-api, `TASK-016` for indexer) run concurrently. Each writes its staged output to `.vibeloom/runs/RUN-20260503-002/tasks/TASK-XXX/` (patch.diff + summary.yaml + files/).

## 4. Per-task validation in staging

Each subagent's task ends with the orchestrator running the validation contract against the staged output:

```text
TASK-014 (web/search) — staging validation:
  typecheck: passed
  lint: passed
  unit: passed (12/12)
  contract-conformance: passed
  bdd: passed (5/5 scenarios)
  → applied to working tree at scope_id order position 1

TASK-015 (search-api) — staging validation:
  typecheck: passed
  lint: 1 warning (acceptable)
  unit: passed (24/24)
  contract-conformance: passed
  bdd: passed (8/8)
  → applied to working tree at scope_id order position 2

TASK-016 (indexer) — staging validation:
  typecheck: passed
  lint: passed
  unit: passed (18/18)
  contract-conformance: passed
  bdd: skipped (no BDD scenarios for this component)
  → applied to working tree at scope_id order position 3
```

The orchestrator processes results in `scope_id` order (deterministic) even though they completed in arbitrary order — this guarantees reproducibility for the same plan + same approved basis.

## 5. Code-sync traces — one per component

After atomic application, the orchestrator emits one code-sync trace per task:

```json
// SYNC-20260503-014
{
  "schema_version": "1.0",
  "trace_id": "SYNC-20260503-014",
  "kind": "code-sync",
  "run_id": "RUN-20260503-002",
  "scope": "component:web/search",
  "realizes": ["CMP-0012", "FR-0023", "STORY-0034", "ACC-0089", "VIEW-0006"],
  "basis_hashes": {"CMP-0012": "sha256:...", "FR-0023": "sha256:...", ...},
  "owned_paths": ["web/src/search/**", "web/tests/search/**"],
  "file_hashes": {"web/src/search/Filters.tsx": "sha256:...", ...},
  "validation": {"typecheck": "passed", "lint": "passed", "unit": "passed",
                 "contract-conformance": "passed", "bdd": "passed"}
}
// SYNC-20260503-015 for search-api, SYNC-20260503-016 for indexer
```

## 6. Status report

```text
$ vibeloom status

Mode: pm
Last run: RUN-20260503-002 (parallel wave W3, 3 tasks, all passed)

Contract:
  intent-specs   approved (2026-05-03 09:14)
  product-specs  approved (2026-05-03 09:38)
  ux-specs       approved (2026-05-03 09:38)
  system-specs   approved (2026-05-03 09:42)

Code:
  web/search          current  · sync SYNC-20260503-014
  services/search-api current  · sync SYNC-20260503-015
  services/indexer    current  · sync SYNC-20260503-016
  (other components)  current

→ Suggested next operation: ship.
```

## What this example illustrates

- **Disjoint ownership unlocks parallelism.** Three components in separate paths can regenerate in the same wave — there's no race because their patches don't touch the same files.
- **The dispatch plan is itself an artifact.** It's saved to `.vibeloom/runs/RUN-.../plan.yaml` so a future user can answer "why did the engine put X and Y in the same wave?"
- **Per-task validation runs in staging.** Failed tasks don't block the wave — successful peers still apply. A failed task's staged output stays for inspection.
- **Deterministic apply order.** Tasks complete in arbitrary order but apply in `scope_id` order, making the same plan + same basis produce the same working-tree state.
- **One code-sync trace per scope.** Each component gets its own source-map-like record. The contract debugger (roadmap A3) will use these to walk from a code symptom back to the contract.
- **Wave-by-wave handoff.** W1 (product-specs) commits before W2 (system-specs) starts; W2 commits before W3 (code) starts. Within a wave: parallel. Between waves: serial.
