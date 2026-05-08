# Read-pass 1 — `v03/vibeloom-implementation.md`

Working outline + checklist of every shape, schema, rule, and operation the engine must implement.

## §1 Runtime architecture
Three layers: skill/orchestrator (judgment) — engine (deterministic substrate) — validation runners (project commands). Engine never judges; skill never hand-waves graph/state work.

## §2 Repo layout
- **§2.1 Full mode** (`pm`/`dev`/`ux`/`expert`): `intent.md`, `defaults.md`, `prd.md`, `usm.md`, `dm.md`, `ux.md`, `system.md`, `containers.md`, `validation-registry.md`, `<container>/<component>/`, `.vibeloom/{cache,traces,runs}/`.
- **§2.2 Vibe**: `intent.md`, `defaults.md`, `system.md`, `AGENTS.md`, `CLAUDE.md`, `.vibeloom/traces/{approvals,decisions}.jsonl`. **No cache**, **no graph state**, **no code-sync trace**.

## §3 Cache vs traces
- `.vibeloom/cache/`: regenerable (`contract-graph.json`, `status.json`).
- `.vibeloom/traces/`: durable, append-only JSONL except `id-registry.json` (structured).

## §4 Engine responsibilities
Owns: discovery, frontmatter parse, item extraction, schema validation, ID allocation+registry, Contract Graph DAG validation, indexing, affected-set, status (incl. obsolete heuristics), direct-edit detection, classification (stale/uncovered/dangling/drifted/obsolete), trace I/O, patch staging+atomic apply.

Does **not** own: semantic equivalence, product/UX judgment, approval decisions, freeform generation, conversation, final task decomposition.

## §5 IDs

### §5.1 Prefix registry (canonical)
36 prefixes total. Roots: `CAP`, `CST`. Tier-grouped:
- intent-specs: `CAP`, `CST`, `DEF` (derives from CAP/CST; Tech Stack uses DEF).
- product-specs: `OBJ`, `KR`, `MET`, `FR`, `NFR`, `EPIC`, `FLOW`, `STORY`, `ACC`, `MS`, `TERM`, `BC`, `AGG`, `ENT`, `VO`, `INV`.
- ux-specs: `VIEW`, `INT`, `UXC`, `MOCK`.
- system-specs: `EXT`, `TB`, `SNFR`, `CONT` (carries `layer`), `CMP` (per-CONT), `IF`/`DEP`/`BEH`/`NOTE` (per-CMP, structured-content carriers, **not graph nodes**).
- context: `BDD`, `SCN`.
- runtime (dated form): `RUN`, `TASK`, `PLAN`.
- trace (dated form): `APPROVAL`, `SYNC`, `GEN`, `EVAL`, `DEC` (carries `record_type` ∈ `IDR|PDR|UDR|ADR|general`), `IMP`.

Per-prefix derivation rules embedded in the table. Notably:
- BC **only in domain-layer components** (methodology §6.4).
- DEF: derives from CAP/CST; downstream may reference without explicit edge (universally binding).
- IDR/PDR/UDR/ADR are **NOT** independent prefixes — they are `record_type` on DEC.
- IF/DEP/BEH/NOTE are body carriers within `component.md`, not graph nodes.

### §5.2 Registry
`.vibeloom/traces/id-registry.json` — `{prefix: {next, retired}}`. Append-only. **Retired IDs are never reused.**

### §5.3 Trace+runtime ID allocation
Dated form `<KIND>-<YYYYMMDD>-<NNN>` for `APPROVAL`, `SYNC`, `GEN`, `EVAL`, `DEC`, `IMP`, `RUN`, `TASK`, `PLAN`, plus operation-packet `REVIEW-`, `RECON-`. Registry: `{kind: {date: next_seq}}`. No retirement.

`FIND-####`, `DRIFT-####` are per-invocation counters, not registry-allocated.

## §6 Frontmatter shapes

### §6.1 Contract artifact
Required fields: `artifact_id`, `artifact_type`, `tier`, `approval_unit`, `scope_kind`, `scope_id`, `status` (`draft|approved`), `timestamp`, `derives_from`. **`approval_mode` is event-level on trace, NOT on artifact.**

### §6.2 Context artifact
Same as §6.1 minus `status`, `approval_unit`, `approval_mode`. Carries `derives_from`.

### §6.3 Container
Adds **required `layer`** field (`presentation|application|domain|infrastructure`).

### §6.4 Component
Bare YAML-style frontmatter with `component_id`, `container_id`, `owned_paths`, `owned_interfaces`, `hosted_bounded_contexts`. Rules:
- container hosts multiple components,
- component belongs to exactly one container,
- BCs only in domain-layer components,
- bounded context belongs to exactly one component,
- `hosted_bounded_contexts` **must be empty** for non-domain layers.

## §7 Validation registry
`validation-registry.md` — frontmatter + first ```yaml fence parses as runner records. Each runner: `runner_id`, `command`, `scope`, optional `inputs`/`outputs`. Engine parses; orchestrator invokes.

## §8 Trace schemas (load-bearing)

All schemas carry `schema_version`, `trace_id`, `kind`, `timestamp`. Reconstructability principle.

### §8.1 Approval
Fields: `schema_version`, `trace_id`, `kind="approval"`, `timestamp`, `run_id`, `approval_unit`, `approval_mode` (`user|delegated`), `items: {item_id: sha256}`, `artifacts: {artifact_id: sha256}`. **Non-regenerable approval baseline.**

### §8.2 Code-sync
Fields incl. `scope`, `realizes: [item_ids]`, `basis_hashes: {item_id: sha}`, `owned_paths`, `file_hashes: {path: sha}`, `validation: {runner: status}`. **Source-map shaped.**

### §8.3 Generation
Fields incl. `task_template_id`, `task_template_version`, `scope`, `basis_ids`, `output_artifact_ids`, `output_item_ids`, `result_status`, `late_fetch_events`, `validation_summary`, `cost`.

### §8.4 Eval
Fields incl. `target`, `checks_run`, `findings: [{finding_id, severity, item_id, message}]`, `cost`.

### §8.5 Decision
Fields incl. `record_type` (default `general`), `author`, `topic`, `load_bearing` (default false), `affects: [item_ids]`, `payload`.

#### §8.5.1 Per-record markdown render
At `/decisions/<record_type>/<TRACE_ID>-<slug>.md` — derived view, regenerable from JSONL. Frontmatter mirrors JSONL fields. Body shape = Nygard ADR (Context/Decision/Consequences). Body prose preserved on subsequent regenerations of *other* fields. Idempotent: drop tree → run `vibeloom decisions render` → identical files. Body is regenerated from `payload` on first materialization, then preserved.

### §8.6 Import
Fields incl. `evidence_summary`, `candidates_proposed`, `confidence_distribution`, `payload`.

### §8.7 Schema extension policy
- `schema_version` is a semver string.
- Minor bump = optional fields added; older parsers ignore unknown.
- Major bump = required fields added; parsers must opt in (engine raises typed error on future major).
- Older traces remain readable forever; engine NEVER silently rewrites.

## §9 Graph cache
`.vibeloom/cache/contract-graph.json`: `artifacts`, `items`, `edges`, `ownership`, `scope_index`, `trace_index`. `status.json` is cached compute output.

## §10 Status computation

Six status categories:
| Cat | Engine trigger |
|---|---|
| `current` | derives_from hashes match latest approval AND no eval finding |
| `stale` | hashes don't match latest approval |
| `uncovered` | required downstream realization missing OR upstream lacks downstream realization |
| `dangling` | derives_from references retired-or-missing ID |
| `drifted` | content hash differs from expected, OR direct edit detected (file mtime + hash diff w/o generation trace) |
| `obsolete` | user-marked OR all downstream consumers obsolete (heuristic) |

**Multi-basis lookup protocol**: per-basis-ID resolution. Approved hash from `latest_approval_trace_containing(basis_id).items[basis_id]`. If no approval trace covers it → unapproved. If retired/absent in registry → retired-or-missing. Item resolves to:
- `dangling` if any basis is retired-or-missing,
- `uncovered` if any basis is unapproved AND required by tier rules,
- `stale` if any basis approved-hash ≠ current-hash,
- `current` only if all bases match AND no eval finding.

## §11 Operation packets

### §11.1 Review packet
`packet_type: review`, `packet_id`, `target`, `basis.approved_upstream`, `changes.{added,modified,removed}`, `findings.{blocking,advisory}`, `impact.uncovered_downstream`, `recommendation`, `user_notes`.

### §11.2 Reconciliation packet
`packet_type: reconciliation`, `packet_id`, `target`, `scope`, `stale_items`, `drift_cases: [{drift_id, evidence, directions: [...], recommended_direction}]`, `user_notes`.

Both packets are **write-capable** (user notes).

## §12 Task templates
Markdown (NOT YAML wrappers). 10-section canonical Design-by-Contract structure: Purpose, Inputs, Preconditions, Steps, Output, Postconditions, Constraints, Invariants, Validation, Failure modes. Each carries `task-template-version` trailer. Engine validates result against template via `validate_summary`.

## §13 Dispatch

### §13.1 Dispatch plan structure
`plan_id`, `affected_set`, `waves: [{wave_id, scopes: [{scope_id, kind, owned_paths, allowed_read_paths, task_template_id}], dependencies: [{from, to}]}]`. Plan is logged at `.vibeloom/runs/RUN-.../plan.yaml`.

### §13.2 Wave assembly rules
1. **Disjoint ownership.** Same wave iff `owned_paths` disjoint.
2. **Derivation precedence.** B in strictly later wave than A iff B.derives_from ⊇ A.owned items.
3. **Concurrency cap.** Default `max_wave_size=5`; spillover to next wave.
4. **Reconciliation singletons.** Reconciliation tasks in 1-scope waves.
5. **Eval ordering.** Read-only eval may run alongside generation in same wave only on different scope; otherwise separate wave after.

### §13.3 `execute_plan(plan)`
Single primitive shared by `generate` and `reconcile`. For each wave: spawn subagents (futures), `await all`, process in deterministic `scope_id` order: `validate_summary` against template `## Output`, `validate_scope` against `allowed_paths`, stage, run validators, on success `apply_atomic`, write generation trace; on code scope also write code-sync trace. Failed task does NOT block wave; peers still apply.

### §13.4 Subagent task header schema
Sole orchestrator↔subagent contract. Fields: `task_id`, `run_id`, `wave_id`, `template_id`, `template_version`, `scope.{scope_id,kind,owned_paths}`, `load_set_refs.{contract,context,evidence}`, `foreign_refs`, `allowed_read_paths`, `allowed_write_paths`, `validation_contract`, `result_shape_id`, `budget`. `result_shape_id` references template `## Output` section name.

### §13.5 No direct subagent communication
Wave-ordering issue if needed.

## §14 Patch-based writes
Subagents stage to `.vibeloom/runs/RUN-.../tasks/TASK-.../{patch.diff,summary.yaml,files/}`. Orchestrator validates summary, validates scope, applies to staging tree, runs runners, on success applies atomically, writes generation+code-sync. On failure, staged output preserved.

## §15 Operation pseudocode

- §15.1 `generate`: affected_set → dispatch_plan → execute_plan → status.recompute.
- §15.2 `eval`: structural_eval + (semantic if needed) + (runners if code/context); writes eval trace; returns findings, modifies nothing.
- §15.3 `review`: loop eval → packet → user decision → bounded fix; fixes target only, no propagation.
- §15.4 `reconcile`: walks affected one drift case at a time; user picks direction (preserve_contract / amend_contract / preserve_downstream_behavior / user_defined); each step writes decision trace.
- §15.5 `approve`: structural_eval, raise if blocking, build approval trace, write, set lifecycle, recompute status.
- §15.6 `status`: cache fresh → return; else parse → traces_index → classify → compose report → next-recommendation → cache.write.
- §15.7 `init`: scaffold layout per mode; vibe = compact; full = full layout; initialize id-registry; write decision trace topic="init".
- §15.8 `import`: scan codebase → import_dispatch_plan → run inference subagents (per kind: capabilities, FR, BC, components) → score confidence → write drafts top-down by tier → emit single import trace.

## §16 Acceptance checklist (20 items)
Trace-backed approval baseline; ID registry persists retired+next; trace families have schema_version; code-sync traces with file hashes+validation; review/recon packets w/ user notes; markdown task templates; patch-staged writes w/ atomic apply; dispatch plan per §13.1–§13.3; subagent header is only contract; validation registry parsed; product/UX peer with MOCK; ux mode; verification ladder in eval routing; component/container/BC rules per methodology §6.5; **engine validates `derives_from` per §5.1 + §8.2**; status distinguishes 6 categories; operation semantics per §15; vibe layout truly minimal; templates as fenced blocks only.

## §17 Templates
Templates live as fenced blocks in `vibeloom-templates.md`; `extract-templates.py` materializes to `templates/` (gitignored). Engine never reads templates directly. 41 templates across 5 families.

## §18 See also
Methodology, templates, manifesto, comparison, getting-started, roadmap, examples.
