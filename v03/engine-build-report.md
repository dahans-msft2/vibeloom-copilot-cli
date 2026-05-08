# v0.3 vibeloom engine — build report

**Engine commit:** `4b4b03a` (worktree branch `worktree-agent-abfa51f7a0784c7f4`).  
**v02 baseline pinned:** `63f0a76` ("Drop PyYAML dependency: engine is now pure-Python with a built-in frontmatter parser").  
**Build profile:** stdlib-only at runtime (Python 3.10+); `pytest` + `pytest-cov` dev-only.  
**Layout:** multi-file package + console-script (`vibeloom-engine`), matching v02's pattern.

## Stages shipped

| Stage | Status |
|---|---|
| 1 — read-only primitives (parser, IDs, graph, cycle detection, layered invariants, parse/graph CLI) | shipped |
| 2 — structural eval + `eval` CLI | shipped |
| 3 — trace I/O + schema-versioning per §8.7 | shipped |
| 4 — staleness, affected-set, direct-edit detection | shipped |
| 5 — dispatch plan + execute_plan | shipped |
| 6 — status classification + decision-trace render + cache management | shipped |

All six verify gates green.

## §16 acceptance checklist

| §16 item | Owner | Status |
|---|---|---|
| `.vibeloom/cache/` and `.vibeloom/traces/` separated | engine | engine-✓ — `cache.py` writes under `.vibeloom/cache/`; `traces.py` under `.vibeloom/traces/`. |
| Approval baseline trace-backed (JSONL append-only) | engine | engine-✓ — `traces.append_trace` is append-only; no in-place rewrite path. |
| ID registry persists retired + next | engine | engine-✓ — `registry.py` stores `{prefix: {next, retired}}` for semantic families and `{prefix: {date: seq}}` for dated families. |
| Trace families have `schema_version` | engine | engine-✓ — every record validated by `_validate_record` per §8.7. |
| Code-sync traces connect IDs to file hashes + validation evidence | engine | engine-✓ — `code-sync` family schema enforces `realizes`, `file_hashes`, `validation`. |
| Review/reconciliation packets have user-notes write capability | skill | skill-deferred — packet shapes documented; user-notes field is a skill-side write surface. |
| Task templates are markdown 10-section, not YAML wrappers | skill | skill-deferred — engine doesn't read templates; they're skill-bundle inputs. |
| Subagent writes patch-staged in `.vibeloom/runs/`, validated, applied atomically | engine | engine-✓ — `patches.stage_task_files` + `apply_atomic` with rollback. |
| Dispatch plan + wave-assembly + parallel semantics match §13.1–§13.3 | engine | engine-✓ — `dispatch.assemble_waves` enforces all 5 rules; `execute_plan` callback contract matches §13.3. |
| Subagent task header schema is the only orchestrator↔subagent contract | skill | skill-deferred — engine emits the header shape from `execute_plan`; skill enforces "only contract" discipline. |
| Validation registry parsed, runners invokable | engine | engine-✓ — `validation_registry.parse_validation_registry` returns runner records; orchestrator invokes them. |
| Product/UX peer generation supports mockup evidence with `MOCK-####` | skill | skill-deferred — engine recognises `MOCK` prefix and its derivation rules; the peer-generation flow is skill-orchestrated. |
| `ux` mode supported as a fifth top-level mode | skill | skill-deferred — modes are skill concerns; engine recognises `ux.md` artifact + `VIEW`/`INT`/`UXC`/`MOCK` prefixes. |
| Verification ladder reflected in eval routing | engine | engine-✓ — engine implements decidable rung (structural eval); validation-registry runners are the mechanical rung; semantic eval (heuristic) is skill-side. |
| Component / container / bounded-context rules match methodology §6.5 | engine | engine-✓ — `_layered_invariants` enforces BC-only-in-domain and BC ⇒ exactly one component. |
| Engine validates `derives_from` per §5.1 + §8.2 (universal-trace) | engine | engine-✓ — `_derives_from_rules` covers (a) non-root needs ≥1 upstream, (b) prefix must be allowed per §5.1, (c) chain must transitively reach `CAP`/`CST`. |
| `status` distinguishes the 6 categories | engine | engine-✓ — `classify_items` covers `current` / `stale` / `uncovered` / `dangling` / `drifted` / `obsolete`; tested per category. |
| Each operation has explicit, traceable execution semantics (§15.1–§15.8) | engine for primitives; skill for orchestration | engine-✓ — primitives (parse, graph, eval, affected, staleness, detect-edits, dispatch, status, decisions render) all live behind CLI verbs with documented JSON shapes; orchestration of `generate`/`reconcile`/`review`/`approve`/`init`/`import` is skill-side. |
| Vibe layout genuinely minimal (no graph cache, no code-sync trace) | engine | engine-✓ — `cache.py` writes only when called; `discover_artifacts` operates fine on a vibe layout (just intent/system/AGENTS); engine never auto-creates cache files. |
| Templates only as fenced blocks; tree is build artifact | skill | skill-deferred — engine never reads `templates/`; `io_.SKIP_DIRS` excludes it. |

20 of 20 checklist items addressed (12 engine-✓, 8 skill-deferred). No `blocked` items.

## Test results

- **Pytest:** `143 passed, 0 failed` (137 baseline + 6 schema/cli-extra).
- **Coverage:** `89% statement coverage` on engine modules (target: ≥85%).
  - Per-module floor: `schema.py` at 82%, `dispatch.py` at 82%, `decisions.py` at 87%, `status.py` at 87%, `cache.py` at 88%. Highest: `affected.py` (100%), `models.py` (96%), `graph.py` (94%).
- Tests cover (named per spec §):
  - `test_status_uncovered_per_section_10` and siblings — all six §10 categories.
  - `test_dispatch.py` — all five §13.2 wave-assembly rules + execute_plan.
  - `test_traces.py` — schema-version transitions per §8.7 (current major OK, future major raises, kind mismatch raises, missing required raises, minor additive fields silently accepted).
  - `test_registry.py` — retired-list invariant per §5.2.
  - `test_decisions.py` — idempotency + body preservation per §8.5.1.
  - `test_cache.py` — cache regenerable from artifacts.
  - `test_eval.py` — `derives_from` validation per §5.1 + §8.2 (missing upstream blocking, invalid upstream prefix blocking, non-transitive-root blocking).

## Smoke test

End-to-end on `/tmp/vibeloom-engine-smoke`. Transcript at the worktree
root: `engine-smoke-transcript.md`. All 6 phases run; all CLI exits ∈ {0}
on the clean trajectory; idempotent decision-trace regeneration is
byte-identical; user-edited decision body preserved across re-render.

Phases:
1. parse / graph / eval (clean) → exit 0.
2. write approval trace via engine API; status reports items as `current`.
3. modify approved prd in-place; `detect-edits` surfaces it; `status`
   reclassifies `FR-0001` → `drifted`.
4. `affected` after CAP-level change; `dispatch` emits plan satisfying
   §13.2 wave-assembly rules.
5. decision-trace markdown render — fresh + delete + re-render
   (byte-identical) + user-edit + re-render (body preserved).
6. `execute_plan` callback harness — verifies §13.3 contract.

## v02 modules — reuse / adapt / rewrite

| v02 module | v03 disposition | Notes |
|---|---|---|
| `parser.py` (481 LOC) | adapted | New `approval_unit`, `layer`, `ux` artifact type, block-style YAML lists, longest-first ID regex. v0.3 carries no separate PDR/ADR ledger parsers (decisions are now traces, not artifacts). |
| `ids.py` (225 LOC) | rewritten | 6-column registry table grew significantly: added `DEF`, ux-specs prefixes (`VIEW`/`INT`/`UXC`/`MOCK`), `BDD`/`SCN`, dated families (`APPROVAL`/`SYNC`/`GEN`/`EVAL`/`DEC`/`IMP`/`RUN`/`TASK`/`PLAN`), operation-packet `REVIEW`/`RECON`. PDR/ADR removed as standalone prefixes; `record_type` now lives on DEC. Two ID forms (semantic + dated) explicit. |
| `graph.py` (185 LOC) | adapted | Cycle detection now emits the full path per §16 acceptance. Iterative DFS to avoid recursion limits. Approved snapshots removed (now trace-backed). |
| `eval_.py` (406 LOC) | rewritten | New `derives_from` rules per §5.1+§8.2 (universal-trace); layered invariants per methodology §6.4/§6.5; lifecycle consistency by approval_unit; dropped v02-specific `_default-as-CST` special case (DEF is now its own prefix). |
| `models.py` (266 LOC) | adapted | `Artifact` gets `approval_unit` and `layer` fields; `ApprovalMode` removed from artifact (now event-level on trace). New `ContainerLayer` enum. |
| `schema.py` (258 LOC) | rewritten | v0.3 required-field set (`approval_unit` for contract; `layer` for container); `Finding` shape moved to `models.py`. |
| `staleness.py` (181 LOC) | rewritten | Was snapshot-based in v02; now trace-backed per §10. Multi-basis lookup protocol per §10. Direct-edit detection compares against approval trace, not snapshot. |
| `affected.py` (48 LOC) | adapted | API simplified; orchestrator wraps with include filters. |
| `cache.py` (65 LOC) | adapted | Path moved from `.vibeloom/state/` → `.vibeloom/cache/`; added `clear_cache`. |
| `cli.py` (223 LOC) | rewritten | New verbs (`dispatch`, `decisions render`); per-command JSON payloads preserved; exit-code semantics 0/1/2 explicit. Removed broad `except Exception` per anti-patterns. |
| `io_.py` (182 LOC) | adapted | New `ux.md` discovery, `validation-registry.md`, `templates/` skip; cache/traces/runs/decisions path helpers. |
| `status.py` (107 LOC) | rewritten | Six categories vs v02's three; per-basis classify per §10 multi-basis protocol; obsolete via registry mark. |
| `indexes.py` (158 LOC) | folded into `graph.py` & `eval_.py` | Indexes weren't pulling weight as a separate module. |

**Net-new modules:**
- `traces.py` (199 LOC) — JSONL append-only I/O for 6 families + schema-version handling.
- `registry.py` (140 LOC) — semantic + dated allocation; retired-list invariant.
- `dispatch.py` (290 LOC) — wave assembly per §13.2; `execute_plan` callback contract per §13.3.
- `decisions.py` (130 LOC) — per-record markdown rendering per §8.5.1.
- `patches.py` (130 LOC) — patch staging + atomic apply with rollback per §14.
- `validation_registry.py` (130 LOC) — runner-record parser per §7.

## Spec ambiguities found (and chosen interpretations)

1. **`derives_from` allowed-upstream sets per §5.1.** The spec table reads "Notes (constraints, derivation)" as prose — for items like FR ("Derives from `CAP`; optionally from `OBJ`/`STORY`") I encoded `("CAP", "OBJ", "STORY")` so all three are valid upstreams (matching v02's per-prefix `DAG_EDGES`). Where the spec says "or" without listing a primary, I included both. Documented in `ids.py` `PREFIX_FAMILIES` per spec; if the spec author intended a stricter set, only that table needs updating.

2. **Approval trace `items` map filtering for direct-edit detection.** §8.1's `items` map covers the entire approval_unit. Per-artifact direct-edit diffing needs to know which items were owned by which artifact at trace time, but that's not stored. Chosen interpretation: when computing direct-edit, restrict the comparison set to items currently owned by the artifact under inspection (or items missing from the graph entirely that the artifact still claims). This avoids false-positive "removed" items for items that simply moved between artifacts. Documented in `staleness.detect_direct_edits` comments.

3. **`obsolete` storage.** §10 says obsolete is "user-marked OR all downstream consumers obsolete". Spec doesn't say where the user mark lives. Chosen interpretation: per-prefix `obsolete` list in `id-registry.json`, parallel to the `retired` list. Engine reads it; orchestrator writes it via `vibeloom mark-obsolete <id>` (skill-side; engine surfaces but doesn't auto-mark).

4. **§10 priority — `drifted` vs `stale`.** Both can apply (a direct edit on an item whose basis also changed). Chosen interpretation: `drifted` (direct edit) takes precedence in the classifier — drift is a stronger signal because it indicates an unvalidated divergence, while staleness is a routine "regenerate" trigger.

5. **CLI top-level catch.** v0.3 catches `(FileNotFoundError, NotADirectoryError, ValueError, RuntimeError)` and exits 2 with a typed JSON error on stderr. Unexpected exceptions (`KeyError`, `IndexError`, etc.) propagate as a real Python crash — that surfaces as a real engine bug rather than being absorbed into "engine error". Per the anti-pattern "no broad `except Exception`."

## Spec bugs surfaced

None. Spec text was internally consistent across §6, §10, §13, §14.1, and §16.

## Known limitations / deferred work

- **Mode auto-inference** is heuristic (vibe vs pm-or-dev vs ux-or-pm). The engine doesn't deterministically distinguish pm from dev or ux — that's a skill-side concern (the user-facing mode routing).
- **Reconciliation packet generation** (`build_reconciliation_packet` per §15.4) is not yet wired up. The engine has the primitives (`compute_staleness`, `affected`, `detect_direct_edits`); the packet assembly is skill-side.
- **Late-fetch tracking** in `generation` traces (§8.3 `late_fetch_events`) — engine schema accepts the field; orchestrator emits when relevant.
- **Brownfield import inference** (§15.8) — engine provides scaffolding (id allocator, trace shape) but the actual inference is skill+subagent.

## After this build

The engine is bundleable: a single `pip install -e .` (dev) or vendoring under `assets/engine/` for the skill release. Console-script entrypoint `vibeloom-engine` is registered; `python -m vibeloom_engine` also works.

Reference engine SHA for `build-skill.md` to start from: **`4b4b03a`** on branch `worktree-agent-abfa51f7a0784c7f4`.
