# Example: greenfield note-search app

A solo developer wants a personal note-taking app with full-text search, tags, and offline support. This example shows VibeLoom in `vibe` mode end-to-end (with actual artifact contents), then the upgrade trigger when the app outgrows it.

The artifact contents below are exactly what the templates in `v03/vibeloom-templates.md` (extracted to `templates/` at build time) materialize into. The intent of this example is to show that the templates produce real, usable artifacts — not just diagrams of what could be.

---

## 1. Initial intent

```text
$ vibeloom init --mode vibe
✓ Created intent.md (draft)
✓ Created defaults.md (draft)
→ Next: edit intent.md, then `vibeloom approve intent-specs`
```

The user opens `intent.md` and writes:

> A personal note-taking app. Notes are plain text with optional tags. The app must work offline and search by text or tag in under 200ms for 10,000 notes.

Vibeloom extracts and materializes:

### `intent.md` (vibe mode)

```markdown
---
artifact_id: intent
artifact_type: intent
tier: intent-specs
scope_kind: root
scope_id: root
status: draft
timestamp: 2026-05-05T09:14:22Z
derives_from: []
---

# Intent

A personal note-taking app. Notes are plain text with optional tags. The app must work offline and search by text or tag in under 200ms for 10,000 notes.

## Capabilities

| id | capability | notes |
|---|---|---|
| CAP-0001 | Create / edit / delete notes | core CRUD |
| CAP-0002 | Tag notes with arbitrary labels | optional per note |
| CAP-0003 | Search notes by text or tag | substring or exact-tag |

## Constraints

| id | constraint | notes |
|---|---|---|
| CST-0001 | Must work offline | no required network connectivity |
| CST-0002 | Search completes under 200ms for 10,000 notes | NFR; user-perceptible latency |

## Product summary

(Vibe-mode prose; on upgrade, this seeds prd + usm + dm.)

A single-user app. Notes are the primary noun. Search is the primary verb. Tags are a secondary classification. Offline-first means local storage and local query — no server round-trip in the search path.
```

### `defaults.md`

```markdown
---
artifact_id: defaults
artifact_type: defaults
tier: intent-specs
scope_kind: root
scope_id: root
status: draft
timestamp: 2026-05-05T09:14:22Z
derives_from: []
---

# Defaults

Repo-wide constitution. Binding globally and always.

## Rules

| id | rule | derives_from | notes |
|---|---|---|---|
| DEF-0001 | All persistent state is local-first | CST-0001 | offline mandate |
| DEF-0002 | Search latency budget: p99 < 200ms | CST-0002 | enforced via test |

## Tech stack

### Presentation
| field | choice | DEF id | derives_from |
|---|---|---|---|
| Framework | (agent decides) | | |

### Application
| field | choice | DEF id | derives_from |
|---|---|---|---|
| API style | (agent decides) | | |

### Domain
| field | choice | DEF id | derives_from |
|---|---|---|---|
| Language | TypeScript | DEF-0003 | DEF-0001 |
| Decomposition | monolith | DEF-0004 | (vibe scale) |
| Aggregate pattern | CRUD | DEF-0005 | |

### Infrastructure
| field | choice | DEF id | derives_from |
|---|---|---|---|
| Database | SQLite (local file) | DEF-0006 | DEF-0001 |
| Compute pattern | local CLI / browser | DEF-0007 | DEF-0001 |
```

User approves. Approval trace is appended:

```text
$ vibeloom approve intent-specs
✓ intent-specs approved (mode=user) · approval trace emitted (APPROVAL-20260505-001)
```

---

## 2. Compact system generation

Vibe auto-advances `system-specs` (compact, no graph). The materialized `system.md`:

### `system.md` (vibe mode)

```markdown
---
artifact_id: system
artifact_type: system
tier: system-specs
scope_kind: root
scope_id: root
status: approved
approval_mode: delegated
timestamp: 2026-05-05T09:14:23Z
derives_from: [CAP-0001, CAP-0002, CAP-0003, CST-0001, CST-0002]
---

# System (vibe-flat)

Single-tier compact system. EXT/TB/SNFR/interfaces/dependencies/behaviors as structured content; not separate artifacts.

## External actors

- USER: the single user of the app

## Trust boundaries

- App boundary: everything inside the local install; no remote services per CST-0001

## Components (compact)

| id | name | responsibility | interfaces (compact) |
|---|---|---|---|
| CMP-0001 | NOTES | CRUD on notes; persistence | createNote, editNote, deleteNote, getNote |
| CMP-0002 | TAGS | Tag attach/detach | tagNote, untagNote, listTags |
| CMP-0003 | SEARCH | Full-text and tag search | searchByText, searchByTag, searchCombined |
| CMP-0004 | UI | Presentation layer | renders NOTES + TAGS + SEARCH |

## Behaviors

- BEH-0001: CMP-0001.createNote — creates a note with body + optional tags; returns note_id
- BEH-0002: CMP-0001.getNote — fetches by note_id
- BEH-0006: CMP-0003.searchByText — matches substring against all notes; returns top results ranked by recency
- BEH-0007: CMP-0003.searchByTag — exact-tag match; returns matching notes
```

---

## 3. First conflict

User asks vibeloom to generate the code. The model proposes a cloud-backed Elasticsearch index for the search component. Vibeloom catches the conflict in `eval`:

```text
$ vibeloom eval system
! Finding (blocking): SEARCH component proposes cloud-backed Elasticsearch;
  conflicts with CST-0001 (must work offline) and DEF-0001 (local-first state).
```

This is the kind of conflict that proves the methodology: a passable-looking generation that quietly violates an upstream constraint. Catching it at eval rather than in production is the point.

User runs `review system`. The review packet:

```yaml
packet_type: review
target: system
basis: [CAP-0003, CST-0001, CST-0002, DEF-0001]
findings:
  blocking:
    - finding_id: FIND-0001
      severity: breaking
      dimension: faithful-representation
      message: "SEARCH proposes cloud-backed Elasticsearch; violates CST-0001 (offline) and DEF-0001 (local-first)."
      suggested_fix: "Use local SQLite FTS5 with BM25 ranking; sized for 10k rows."
recommendation: apply_proposed_fix
```

User accepts the fix. Re-eval passes. The orchestrator emits a decision trace recording the choice:

```json
{
  "trace_id": "DEC-20260505-0001",
  "kind": "decision",
  "record_type": "ADR",
  "load_bearing": true,
  "affects": ["CMP-0003", "DEF-0006"],
  "topic": "search-backend-choice",
  "author": "user@example.local",
  "timestamp": "2026-05-05T09:18:14Z",
  "payload": "Selected SQLite FTS5 over cloud-backed Elasticsearch. Rationale: CST-0001 (offline) is binding; FTS5 with BM25 meets CST-0002 (200ms for 10k notes) in benchmarks; zero infra cost. Rejected: Elasticsearch (violates offline), local Lucene (heavy JVM dependency), Tantivy (extra Rust toolchain)."
}
```

---

## 4. Code generation

```text
$ vibeloom approve system
✓ system approved · approval trace emitted (APPROVAL-20260505-002)

$ vibeloom generate code
✓ Generated files across NOTES, TAGS, SEARCH, UI components in 1 dispatch wave
✓ Validation: typecheck=pass, unit=pass, contract-conformance=pass
✓ Code-sync trace emitted (SYNC-20260505-001)
```

Code-sync trace records that `src/search/fts.ts` realizes `BEH-0006` (text search) on `CMP-0003` (search component), with file hashes and validation results.

---

## 5. Upgrade trigger

Three months later, the project has grown: 4 contributors, 12 components, an embedding-based semantic search proposed alongside the original text search. Vibeloom flags:

```text
$ vibeloom status
ℹ Vibe limits exceeded:
  - 12 components (vibe recommends ≤ 5)
  - 4 contributors (vibe recommends 1-2)
  - 3 reconciliations in last 30 days
→ Consider: vibeloom init --upgrade --mode pm
```

User upgrades. Migration trace records that compact intent + flat system became full intent-specs + product-specs + system-specs (ux-specs added in `ux` mode upgrade, not pm).

The expanded `intent.md` carries forward the original CAPs and CSTs. `defaults.md` Tech Stack section is filled in based on observed code:

```markdown
## Tech stack

### Presentation
| field | choice | DEF id | derives_from |
|---|---|---|---|
| Framework | React 18 | DEF-0010 | (observed in code) |
| Meta-framework | Vite | DEF-0011 | |
| Styling | Tailwind CSS | DEF-0012 | |
| State management | TanStack Query + Zustand | DEF-0013 | |

### Application
| field | choice | DEF id | derives_from |
|---|---|---|---|
| API style | tRPC (local; offline-first) | DEF-0014 | DEF-0001 |
| Backend framework | Node 20 | DEF-0015 | |

### Domain
| field | choice | DEF id | derives_from |
|---|---|---|---|
| Language | TypeScript | DEF-0003 | (carried from vibe) |
| Decomposition | monolith | DEF-0004 | |
| Aggregate pattern | CRUD | DEF-0005 | |

### Infrastructure
| field | choice | DEF id | derives_from |
|---|---|---|---|
| Database | SQLite (local file) + better-sqlite3 | DEF-0006 | DEF-0001 |
| Compute pattern | Electron app + local CLI | DEF-0007 | DEF-0001 |
```

The newly generated `containers.md` shows the layered split:

```markdown
## Containers

| id | slug | layer | purpose |
|---|---|---|---|
| CONT-0001 | web-app | presentation | React SPA in Electron renderer |
| CONT-0002 | local-api | application | tRPC API in Electron main process |
| CONT-0003 | notes-domain | domain | Notes + Tags aggregates |
| CONT-0004 | search-domain | domain | Search aggregate (FTS5-backed) |
| CONT-0005 | local-infra | infrastructure | SQLite file + filesystem layout |
```

A representative container.md (the search-domain container) gets its `layer` field and per-layer deployment guidance:

```markdown
---
artifact_id: container.search-domain
artifact_type: container
tier: system-specs
scope_kind: container
scope_id: search-domain
container_id: CONT-0004
layer: domain
status: draft
timestamp: 2026-05-05T11:42:00Z
derives_from: [CONT-0004, BC-0002]
---

# Container — search-domain

Owns the search bounded context. Hosts the SQLite FTS5 query path and ranking logic. Pure logic; no I/O beyond the SQLite handle injected from local-infra.

## Deployment target

| field | choice |
|---|---|
| Platform | Electron main process (in-process; no separate runtime) |
| Pattern | TypeScript module; consumed via tRPC by local-api |
| Runtime | Node 20 |
| Notes | Domain runs in-process for vibe-scale monolith. multi-service decomposition deferred until cloud-sync ships. |

## Resident bounded contexts

| bounded_context | notes |
|---|---|
| BC-0002 | Search BC: query parsing, FTS5 invocation, ranking |

## Component inventory

| id | slug | description | bounded_context | derives_from |
|---|---|---|---|---|
| CMP-0010 | query-parser | Parse text + tag query syntax | BC-0002 | CONT-0004, BC-0002 |
| CMP-0011 | fts5-driver | Wrap SQLite FTS5 invocation | BC-0002 | CONT-0004, BC-0002 |
| CMP-0012 | ranker | BM25 + recency reranking | BC-0002 | CONT-0004, BC-0002 |
```

Existing code is import-analyzed against the freshly generated full contract; most is recognized; a few drifted spots are flagged for reconciliation.

---

## What this example illustrates

- **Vibe is genuinely minimal** — no graph cache, no code-sync trace folder beyond the basics. Just intent + defaults + flat system + approvals.jsonl.
- **Templates produce real artifacts** — every code block above is what the templates in `v03/vibeloom-templates.md` (extracted to `templates/artifacts/` at build time) materialize into. Frontmatter, sections, item IDs, `derives_from` edges all match the spec.
- **Tech Stack section is structured** — per DDD layer, fields filled or empty signal binding-vs-agent-decides, choices have DEF ids and derives_from links.
- **Conflict is the test, not clean cascade** — the value of the contract shows up when the agent's generation contradicts an upstream constraint. The reconciliation produces a load-bearing decision trace.
- **Decision traces have classification** — the FTS5 choice is an `ADR` (architecture decision) with explicit `affects` (CMP-0003, DEF-0006). Future eval queries can answer "why is search using FTS5?" by walking the trace.
- **Upgrade is a feature** — when vibe outgrows itself, vibeloom recommends migration; the migration is a traceable operation, not a tool reset; tech-stack inferences are populated from observed code.
- **Layered architecture is concrete** — containers carry `layer` and have per-layer deployment targets. The presentation/application/domain/infrastructure split maps to real deployment patterns.
