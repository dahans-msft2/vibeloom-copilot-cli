# Canon fact map

Externalized Step 1 verify for `review-canon.md`. Every load-bearing fact in the canon and its canonical home tier.

Tier legend: **W** = manifesto (WHY), **M** = methodology (WHAT), **I** = implementation (HOW), **T** = templates (MATERIALIZATION).

Format: `fact → canonical tier (citation)` then any other-tier appearances flagged.

## Core paradigm

| Fact | Canonical | Other appearances |
|---|---|---|
| Dark-factory destination | W §1 | — |
| Contract definition (human-mendable, agent-legible, machine-checkable, traceable) | W §2 | — |
| Specs / Graph / Obligations / Checks four-part structure | W §2 | — |
| codæ vs spec-driven distinction | W §3 | — |
| The bet (code is downstream infrastructure) | W §8 | — |
| codæ is the paradigm; VibeLoom is one instantiation | M §1 | — |

## Contract stack

| Fact | Canonical | Other appearances |
|---|---|---|
| Contract / Context / Code stack + Traces | M §4 | — |
| Contract artifacts and tiers (intent / product ⇄ ux / system) | M §6 | — |
| EARS-as-structured-field for FR/NFR/ACC | M §6.2 | — |
| Mockups as input evidence; not normative until IDed | M §6.3 | I §17 (re-states YAML) |
| Layered architecture rules (BCs only in domain components) | M §6.5 | I §6.3 (cites layer field) |
| Contract graph definition + DAG invariants | M §8 | — |
| Knowledge graph (v0.3) vs context graph (roadmap CGKG-B) | M §8 | — |

## Modes + operations

| Fact | Canonical | Other appearances |
|---|---|---|
| Five modes (vibe / pm / dev / ux / expert) | M §5 | T references/modes.md (specializes per mode) |
| Vibe is intentionally minimal (different operating point) | M §5.1 | I §2.2 (cites by forward ref) ✓ |
| Upgrade is one-way + migration trace | M §5.2 | — |
| ux mode is designer-led + PM peer | M §5.3 | — |
| Operations list (init / import / generate / eval / review / reconcile / approve / status) | M §12 | I §15 (implements) |

## Status + traces

| Fact | Canonical | Other appearances |
|---|---|---|
| Status categories meanings (current / stale / uncovered / dangling / drifted / obsolete) | M §9 | I §10 (cites + adds computation rules) ✓ |
| Status computation rules (the table) | I §10 | — |
| Multi-basis lookup protocol | I §10 | — |
| Trace families list (approval / generation / eval / code-sync / decision / import / id-registry) | M §11 | I §8 (schemas), I §5.1 (prefixes), M §4.4 (brief intro) |
| Decision trace classification (IDR / PDR / UDR / ADR / general) | M §11.1 | I §5.1 (cites by forward ref) ✓ |
| Trace schemas (per-family JSON shapes) | I §8 | — |

## IDs + registry

| Fact | Canonical | Other appearances |
|---|---|---|
| ID prefix registry (40 prefixes, table) | I §5.1 | T references/artifacts.md (re-presents) |
| Semantic-item registry shape `{next, retired}` | I §5.2 | — |
| Trace + runtime + packet ID dated form `<KIND>-<YYYYMMDD>-<NNN>` | I §5.3 | — |
| FIND / DRIFT counters (not registry-allocated) | I §5.3 | — |

## Eval

| Fact | Canonical | Other appearances |
|---|---|---|
| Verification ladder (Decidable / Mechanical / Heuristic) — naming + climb concept | M §14.3 | W §7 (with check lists per rung), T references/eval.md (with check list per tier), T tasks/eval.md (with check list per tier) ⚠ DUP |
| Per-tier check list (what's in Decidable, Mechanical, Heuristic) | M §14.3 | W §7, T references/eval.md, T tasks/eval.md ⚠ DUP |
| Structural eval check list | M §14.1 | — |
| Semantic eval dimensions | M §14.2 | T references/eval.md (specializes per dimension) ✓ |

## Engine + runtime

| Fact | Canonical | Other appearances |
|---|---|---|
| Three operational layers (skill / engine / runners) | I §1 | — |
| Engine ownership boundary | I §4 | — |
| Cache vs traces split | I §3 | — |
| Repo layouts (full / vibe) | I §2 | — |
| Dispatch plan + wave assembly + parallel semantics | I §13 | — |
| Subagent task header schema | I §13.4 | — |
| Patch-based writes | I §14 | — |
| Operation pseudo-code per operation | I §15 | — |

## Brownfield + UX ingestion

| Fact | Canonical | Other appearances |
|---|---|---|
| Brownfield import operation | I §15.8 | I §16 ⚠ orphan section, just a YAML shape |
| MOCK record YAML shape | I §17 ⚠ orphan section | M §6.3 (covers conceptually) |

## Cognitive surface

| Fact | Canonical | Other appearances |
|---|---|---|
| Cognitive surface visual (108K-LOC vs 24% contract) | W §5 (the "mendable surface" SVG) | — |
| Cognitive surface metric (item count, compression ratio, secondary metrics) | M §10 ⚠ unreferenced | — |

## Templates + skill

| Fact | Canonical | Other appearances |
|---|---|---|
| Templates as fenced blocks; extracted on demand | I §19 | T README.md (re-states), T versioning |
| Task-template 10-section structure | I §12.1 | T tasks/* (each materializes) |
| Skill manifest (SKILL.md) | T skill/SKILL.md | — |
| Skill loads methodology + implementation as authoritative sources | T skill/SKILL.md | ⚠ omits manifesto + misattributes methodology as "WHAT and WHY" |
| Verification ladder reference | T references/eval.md | ⚠ DUP with M §14.3 |

## Acceptance + roadmap

| Fact | Canonical | Other appearances |
|---|---|---|
| §18 acceptance checklist | I §18 | — |
| Roadmap items (CGKG-B, DDD context maps, etc.) | roadmap.md | — |

---

**Flagged for the packet (cross-references show duplication or scope leak):**

- ⚠ Verification ladder check list in 4 places (W §7, M §14.3, T references/eval.md, T tasks/eval.md)
- ⚠ I §16 (Brownfield import) is an orphan section
- ⚠ I §17 (UX and mockup ingestion) is an orphan section
- ⚠ M §10 (Cognitive surface metric) is unreferenced anywhere downstream
- ⚠ T skill/SKILL.md misattributes methodology as "WHAT and WHY"; omits manifesto from authoritative sources

(Pass-3 cross-walk surfaces these into the canon-review-packet.md.)
