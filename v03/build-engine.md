# Build the v0.3 vibeloom engine

A prompt for Claude Code (or any equivalent agentic coding tool). The agent reads the canonical implementation spec and produces a working `engine/` directory.

This prompt names **what** must happen, not how. Module decomposition, public API shapes, internal data structures, parsing strategies, code style — those are the agent's call. The agent should consult `vibeloom-implementation.md` as the source of truth and exercise judgment.

This prompt is itself codæ-shaped — Inputs, Preconditions, Steps, Output, Postconditions, Constraints, Invariants, Validation, Failure modes — because the build of vibeloom should follow the same discipline vibeloom imposes on the systems it governs.

---

## Purpose

Build the v0.3 vibeloom engine: a deterministic Python package that parses contract artifacts, validates schemas, builds the contract graph, computes affected sets, plans dispatch waves, manages the ID registry, reads/writes durable traces, and computes status. The engine never makes semantic judgments. **Skill = orchestrator + judgment; engine = parser + math.**

## Inputs

- **`v03/vibeloom-implementation.md`** — canonical spec. Authoritative for every shape, schema, rule, and operation the engine must implement. Read it cover-to-cover before writing code.
- **`v03/vibeloom-methodology.md`** — paradigm context. Read to understand contract tiers, modes, derivation DAG, status taxonomy, traces, and the verification ladder.
- **`v02/engine/`** — prior-art reference. The v02 engine targets an older spec; many concepts carry over but several details have changed. Use it for inspiration, not for copy-paste.

### v02 → v03 delta (must-handle)

| Area | v03 changes |
|---|---|
| Contract artifact frontmatter | adds `approval_unit` field (impl §6.1, §6.3) |
| Decision traces | JSONL canonical + per-record markdown rendering at `/decisions/<record_type>/<TRACE_ID>-<slug>.md`, regenerable from JSONL (impl §8.5.1) |
| Dispatch | `execute_plan(plan)` is now a single primitive shared by `generate` and `reconcile` (impl §13.3); the engine assembles the plan and validates results, the orchestrator drives subagents |
| ID prefixes | 6-column registry (prefix / name / tier / source artifact / scope / notes) per impl §5.1 |
| Containers | `layer` field required (`presentation` \| `application` \| `domain` \| `infrastructure`); BCs only in `domain` layer (methodology §6.4) |
| Modes | adds `ux` mode (designer-led + PM peer reviewer) |
| Task templates | 10 sections (Purpose / Inputs / Preconditions / Steps / Output / Postconditions / Constraints / Invariants / Validation / Failure modes) per impl §12.1 |
| Decisions | unified `DEC-` family with `record_type` (`IDR`/`PDR`/`UDR`/`ADR`/`general`); no separate ADR/PDR folders |
| Eval ladder | explicit `decidable` / `mechanical` / `heuristic` rungs per methodology §14.3 |

The implementation doc is the truth. Treat the table above as a starting checklist, not an exhaustive list.

## Architecture sketch (data flow only)

```text
artifacts (markdown + frontmatter)
        │
        ▼
parsing & schema validation
        │
        ▼
ID registry & contract graph (DAG over derives_from)
        │
        ▼
read-only operations:  structural eval • staleness • affected-set
        │
        ▼
dispatch plan (waves) and execute_plan (validation + atomic patches + trace I/O)
        │
        ▼
status classification (current / stale / uncovered / dangling / drifted / obsolete)
        │
        ▼
JSON on stdout  ←  CLI surface
```

How to decompose this into modules and APIs is the agent's choice — match the impl spec's responsibilities and keep the dependencies acyclic.

## Preconditions

- Repository is checked out at `vibeloom/`. You are working in `vibeloom/v03/`.
- Python 3.10+ available.
- All three input files exist.
- No `engine/` directory at `v03/`. If one exists from a prior incomplete build, read it first before overwriting; then start clean.

## Steps

1. **Read `vibeloom-implementation.md` end-to-end.** Take notes on every frontmatter shape (§6), every trace schema (§8), every operation pseudocode (§15), and every acceptance-checklist item (§18). Re-read until ambiguities are clearly identified — do not start coding while still confused.

2. **Read `vibeloom-methodology.md` cover-to-cover for paradigm context.** Methodology §6.5 (layered architecture) and §11.1 (decision-trace classification) are particularly load-bearing.

3. **Diff v02 against v03.** Identify every place the v03 spec changes the contract. The delta table above is a starting list; the spec is the truth.

4. **Implement the engine** as a Python 3.10+ package under `v03/engine/`, packaged so it can be invoked with `python -m <package_name>` and (optionally) installed via `pip install -e v03/engine`. Cover the full set of capabilities the implementation doc requires:

   - **Frontmatter and body parsing** for every artifact type listed in §6. Body parsing must extract IDed items per the per-tier templates referenced in `vibeloom-templates.md`.
   - **Schema validation** for every frontmatter shape (§6) and every trace family (§8), with `schema_version` handling per §8.7.
   - **ID registry** with allocation, retired-list, and the rule that retired IDs are never reused (§5.2).
   - **Trace I/O** for every family in §8 (approval, code-sync, generation, eval, decision, import) plus the structured `id-registry.json`. JSONL is append-only; rejecting in-place rewrites is non-negotiable.
   - **Decision-trace markdown rendering** per §8.5.1 — every JSONL row in `decisions.jsonl` materializes deterministically as a per-record file at `/decisions/<record_type>/<TRACE_ID>-<slug>.md`. Idempotent, regenerable.
   - **Contract graph** as a DAG over `derives_from` edges; cycle detection; only `CAP` and `CST` may be roots; bounded contexts only in domain-layer components (methodology §6.4); the rest of §8 of methodology.
   - **Cache management** at `.vibeloom/cache/` — regenerable, never authoritative, safe to delete.
   - **Structural eval** covering every check listed in impl §14.1 and methodology §14.1 (Rung 1 of the verification ladder).
   - **Staleness, affected-set, direct-edit detection** per impl §10 + §15.
   - **Dispatch plan** with wave assembly per impl §13.1–§13.2 (disjoint ownership, derivation precedence, concurrency cap, reconciliation singletons, eval ordering).
   - **`execute_plan(plan)`** per §13.3 — coordinates validation, trace writing, atomic patch application; calls back to the orchestrator for actual subagent spawning.
   - **Status classification** producing the six categories in §10, plus the surrounding report fields (lifecycle per artifact, affected scope, coverage gaps, current mode, recommended next operation).
   - **CLI** exposing every command listed in impl §1 (`parse`, `graph`, `eval`, `affected`, `staleness`, `detect-edits`, `dispatch`, `status`). All commands emit JSON on stdout. Non-zero exit on blocking findings.

   The agent decides module names, public APIs, internal data shapes, parsing strategy, and code organization. Match the spec's behavior; don't over-think the structure.

5. **Write tests covering the engine's behavior.** At minimum, the test suite must:
   - Exercise every status category from §10 (`current` / `stale` / `uncovered` / `dangling` / `drifted` / `obsolete`).
   - Exercise wave-assembly rules from §13.2 (disjoint ownership, derivation precedence, concurrency cap, reconciliation singletons).
   - Exercise schema-version handling from §8.7 (parser meets older trace; meets newer trace; rejects incompatible major).
   - Exercise the ID registry's retired-list invariant.
   - Exercise the decision-trace markdown rendering's idempotency.
   - Exercise the cache's regeneration-from-traces property.

   Build whatever test fixtures the suite needs. Tests run with `pytest`.

6. **Smoke-test end-to-end on a scratch repo.** The agent assembles a fresh vibeloom-governed scratch repo (under `/tmp`) and drives the engine through enough operations to confirm the full pipeline works in both `vibe` and `pm` modes. At minimum, exercise:
   - Parsing a minimal artifact set; building the graph; running `eval` clean.
   - Writing an approval trace; running `status` and seeing lifecycle flip to approved with all items `current`.
   - Modifying an approved artifact; running `detect-edits` and seeing direct edits surfaced; running `status` and seeing items reclassified appropriately.
   - For `pm` mode: building the graph cache; running `affected` after a CAP-level change; running `dispatch` and getting a well-formed plan.

   Each engine command must produce well-formed JSON on stdout. Each CLI exit code must match the documented semantics.

## Output

A working `v03/engine/` directory invokable as a Python package. Optionally pip-installable.

## Postconditions

- All CLI commands listed in impl §1 exist, emit JSON on stdout, and follow the documented exit-code semantics.
- All trace schemas from impl §8 are encoded and validated on read per §8.7.
- ID registry persists `next` counter and `retired` list per prefix; retired IDs are never reused (§5.2).
- Contract graph is a DAG; only `CAP` and `CST` are roots.
- Decision-trace markdown rendering is wired up per §8.5.1 — JSONL canonical, markdown derived, regenerable.
- `dispatch_plan` and `execute_plan` exist per §13 and pass tests covering the wave-assembly rules.
- Status classification matches §10 for all six categories.
- Smoke tests in §6 above pass end-to-end for both `vibe` and `pm` modes.
- Test suite passes with `pytest`.

## Constraints

- **Zero runtime dependencies beyond Python 3.10+.** No `pip install` required for end users. Stdlib only. (`pytest` is dev-only.) Custom YAML frontmatter parser shipped in-tree.
- **No semantic judgments in the engine.** Hashes, schemas, derivation walks, IDs, JSON I/O — yes. Spec meaning, approval correctness, faithfulness — no.
- **All operations are deterministic.** Same inputs → same outputs.
- **Cache is regenerable.** If `.vibeloom/cache/` is deleted, the engine rebuilds from artifacts + traces with no information loss.
- **Traces are durable, append-only.** No silent rewrites. On schema-version mismatch, surface a status finding instead of crashing (§8.7).

## Invariants

- The contract graph is a DAG; only `CAP` and `CST` are roots.
- Container `layer` is required and enum-bounded.
- Bounded contexts are hosted only by domain-layer components.
- Component belongs to exactly one container; bounded context belongs to exactly one component.
- ID registry's `retired` list is append-only; retired IDs are never reused.
- Trace files are append-only; no in-place edits.

## Validation

Before declaring the engine complete, every engine-related item in impl **§18 acceptance checklist** must pass — paste a copy of §18 into your final summary with each box checked.

Plus:
- `pytest` passes 100%.
- The smoke test in step 6 passes end-to-end for both `vibe` and `pm` modes.

## Failure modes

- **Spec ambiguity.** Where the implementation doc is ambiguous, prefer the most conservative interpretation, leave a comment marking the choice (`# spec ambiguity: <reason>`), and surface the question in your final summary so the human can adjudicate. Do not invent behavior the spec doesn't specify.
- **v02-vs-v03 confusion.** If you find yourself reaching for the v02 module and pasting it, stop and re-read the relevant § of `vibeloom-implementation.md`. The v02 engine is reference, not template.
- **Schema drift.** If your implementation diverges from §8 trace schemas, the bug is in your code, not the spec. Re-read §8.7.
- **Test failures.** Don't suppress, don't skip. If a test exposes a real bug in the spec, surface it; if it exposes a bug in your code, fix it.
- **Reaching for a third-party package.** Stop. Check stdlib first. The zero-dependency constraint is not optional.

## Anti-patterns to avoid

- Importing `pyyaml`, `pydantic`, `marshmallow`, `jsonschema`, or any other parsing/validation library.
- Shelling out to `git` for content hashing — use `hashlib.sha256` on canonical-normalized text.
- In-place editing of trace files.
- Letting the engine make semantic decisions.
- Catching `Exception` broadly.
- Adding undocumented CLI flags.
- Treating cache as authoritative.
- Hand-editing extracted templates (the templates tree is a build artifact; edit the source).

## After this build

When the engine passes its acceptance checklist and the smoke test, run [`build-skill.md`](build-skill.md) to assemble the full skill bundle.

Tag a reference engine commit so the build-skill phase has a stable target.
