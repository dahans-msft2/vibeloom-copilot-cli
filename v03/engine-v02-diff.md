# v02 → v03 engine diff inventory

**v02 commit pinned:** `63f0a76b577af05a02edeb70b016bd500c8f5b6b` ("Drop PyYAML dependency: engine is now pure-Python with a built-in frontmatter parser").

## v02 module inventory

| Module | LOC | v03 plan |
|---|---|---|
| `__init__.py` (28) | trivial | rewrite — bump version, new package name `vibeloom_engine` |
| `__main__.py` (6) | trivial | reuse pattern |
| `affected.py` (48) | adapt — affected-set still relevant; expand `include` filters per §15.4 |
| `cache.py` (65) | adapt — paths change (`.vibeloom/cache/` not `.vibeloom/state/`); add `nuke_cache` |
| `cli.py` (223) | rewrite — new verbs (`dispatch`, `decisions render`); per-command JSON shapes preserved |
| `eval_.py` (406) | adapt — keep structural checks; add `derives_from` universal-trace; layered invariants |
| `graph.py` (185) | reuse — DAG primitives, cycle detection; add full-cycle path emission |
| `ids.py` (225) | rewrite — registry table grew (DEF, ux-specs, MOCK, BDD/SCN, dated families); record_type for DEC |
| `indexes.py` (158) | adapt where needed — fold into graph/queries module |
| `io_.py` (182) | adapt — new ux-specs path, container `layer` |
| `models.py` (266) | adapt — Artifact gets `approval_unit`; Container gets `layer`; new `ApprovalMode` lives on trace, not artifact |
| `parser.py` (481) | adapt — supports v03 frontmatter; ledger PDR/ADR sections become DEC `record_type`; new `approval_unit` field; container `layer`; ux-specs |
| `schema.py` (258) | adapt — required fields per v03 §6.1, §6.2, §6.3, §6.4; layered checks |
| `staleness.py` (181) | adapt — multi-basis lookup per §10; trace-backed approval baseline (not snapshots) |
| `status.py` (107) | rewrite — six categories (was three); per-basis classify per §10 |

## Net-new modules in v03

- **`traces.py`** — Trace I/O for 6 families + `id-registry.json` (§8). Append-only JSONL; `schema_version` validation per §8.7.
- **`registry.py`** — ID allocation persisted at `.vibeloom/traces/id-registry.json`; retired-list invariant (§5.2); dated-family allocation per §5.3.
- **`dispatch.py`** — Dispatch plan + wave-assembly (§13.1, §13.2); `execute_plan(plan)` callback shape (§13.3).
- **`decisions.py`** — Per-record markdown rendering (§8.5.1); idempotent regeneration; user-edited body preservation.
- **`patches.py`** — `.vibeloom/runs/` patch staging + atomic apply (§14).

## v02 → v03 delta coverage check

| v02→v03 row from build-engine.md | Coverage |
|---|---|
| `approval_unit` frontmatter field | parser.py + models.py adaptation |
| Decision traces — JSONL canonical + per-record markdown | new `traces.py`, `decisions.py` modules |
| `execute_plan` shared by generate/reconcile | new `dispatch.py` module |
| ID prefixes — 6-column registry | rewrite `ids.py` (table grew significantly) |
| Container `layer` enum | parser.py + models.py + schema.py |
| Modes `ux` | mode-driven concerns are skill-side; engine just allows the layout |
| Task templates 10 sections | engine doesn't read templates; orchestrator does |
| Decisions unified `DEC-` family | rewrite `ids.py` removes PDR/ADR as standalone; add `record_type` |
| Eval ladder explicit | engine implements decidable rung (structural eval) — already present, extend |

## Net-new derive-from validations (per build-engine.md note about §16 acceptance growing)
- non-root item missing `derives_from` → blocking finding,
- chain that doesn't transitively reach `CAP`/`CST` → blocking finding,
- non-allowed upstream prefix → blocking finding (per §5.1).

## Layout decision
v0.3 keeps **multi-file package + console-script** pattern (matches v02's baseline). Package name: `vibeloom_engine`. Layout under `v03/engine/`:

```
v03/engine/
  pyproject.toml
  vibeloom_engine/
    __init__.py
    __main__.py
    cli.py
    parser.py
    ids.py
    models.py
    graph.py
    schema.py
    eval_.py
    traces.py
    registry.py
    dispatch.py
    decisions.py
    patches.py
    affected.py
    staleness.py
    status.py
    cache.py
    io_.py
  tests/
    conftest.py
    test_*.py
```
