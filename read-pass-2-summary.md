# Read-pass 2 — `v03/vibeloom-methodology.md`

Paradigm context. The implementation doc is the truth on shapes; this doc is the truth on meaning.

## §1 — Relationship to codæ
codæ is the paradigm; VibeLoom is the reference implementation. Pieces VibeLoom defines: contract stack, Contract Graph, modes, review/reconciliation, context/traces, subagent loading, conformance evidence, code-sync.

## §2 — Principles
1. Live contract, not stale specs.
2. Contract as eval (same items drive generation AND check).
3. Human-mendable review surface.
4. Traceability by ID.
5. Scoped generation from bounded load sets.
6. Traces are evidence, not truth.
7. False positives beat false negatives.
8. Contract aspires toward decidability — promote heuristic→mechanical→structural.

## §3 — When to use VibeLoom
Use when: system survives >1 generation step, multiple contributors, product/domain/UX/architecture decisions matter, drift would be expensive, traceability needed.

## §4 — Layers and traces
- §4.1 Contract: governed semantic truth, lifecycle `draft|approved`. Only approved drives generation.
- §4.2 Context: active generation guidance derived from approved contract. Reviewable but normal fix is amend upstream + regenerate.
- §4.3 Code: synchronized & validated, not approved.
- §4.4 Traces: parallel durable provenance.

Stack flow: intent → product ↔ ux (peer) → system → context → code, with traces alongside.

## §5 — Modes (load-bearing)

| Mode | Lead | User-owned | Delegated | Internal |
|---|---|---|---|---|
| `vibe` | solo | intent-specs | system+code | minimal — no graph, no code-sync |
| `pm` | product | intent, product, optionally ux | system | full graph |
| `dev` | tech | intent, system | product, optionally ux | full graph |
| `ux` | design | intent, ux, optionally product | system | full graph |
| `expert` | architect | all | none | full graph |

intent-specs always user-owned. Delegated auto-advance allowed only when structural eval passes and no semantic judgment requires escalation.

- §5.1 Vibe is intentionally minimal: compact stack `intent.md`, inferred flat `system.md`, `AGENTS.md`. No IDed graph, no code-sync. Modern model keeps small system coherent. **Vibe still emits approval traces.**
- §5.2 Upgrade is a feature: `init --upgrade --mode <pm|dev|ux|expert>` is one-way, produces migration trace.
- §5.3 ux mode: design-led, mockups first-class. Uses `generate-product-specs-from-ux`. PM peer-reviews product-specs.

## §6 — Contract artifacts

### §6.1 Intent-specs
- `intent`: `CAP-####`, `CST-####` — only root source of user intent.
- `defaults`: `DEF-####` (or CST), normalized rules + Tech Stack (organized by DDD layer).

### §6.2 Product-specs
- `prd`: `OBJ`, `KR`, `MET`, `FR`, `NFR`. EARS allowed as structured field.
- `usm`: `EPIC`, `FLOW`, `STORY`, `ACC`, `MS`.
- `dm`: `TERM`, `BC`, `AGG`, `ENT`, `VO`, `INV`.

### §6.3 UX-specs (peer with product)
- `ux`: `VIEW`, `INT`, `UXC`, `MOCK`. Mockups don't become normative truth until extracted into IDed contract items.
- `ux-specs/mockups/`: image evidence.

### §6.4 System-specs
- `system`: `EXT`, `TB`, `SNFR`.
- `containers`: `CONT` (carries `layer`).
- `container.md` per container: `CMP`.
- `component.md` per component: `IF`, `DEP`, `BEH`, `NOTE` as structured content.

### §6.5 Layered architecture (load-bearing)
| Layer | Hosts BCs? | Components are... |
|---|---|---|
| `presentation` | No | UI components |
| `application` | No | API surfaces, BFF |
| `domain` | **Yes** | Service-shaped components hosting BCs |
| `infrastructure` | No | No internal components |

**Key invariants** (engine enforces):
- Component is smallest owned technical boundary.
- Bounded contexts are domain partitions inside components, NOT runtime deployment.
- Containment chain: container ⊇ component ⊇ bounded context.
- BCs only inside `domain`-layer components.

## §7 — Context artifacts
`config` (AGENTS.md/CLAUDE.md) and `bdd`/`scenarios`. Decisions live in append-only traces (ADR/PDR-style), with markdown rendering under `/decisions/<record_type>/`.

## §8 — Contract Graph
Parsed queryable model. Nodes are IDed semantic items; edges are `derives_from`; graph is a DAG. v0.3 ships as knowledge graph (instantiated ontology only).

### §8.1 Boundary principle
Component is terminal contract node for technical ownership. Code does not require deep graph carriers in v03; code-sync traces bridge graph items to code paths/hashes.

### §8.2 Derivation rules (load-bearing)
**Roots are CAP and CST. Every other item derives, directly or transitively, from at least one root.** Downstream items derive from approved upstream items or accepted input evidence (mockups). Approved Contract Graph is acyclic.

## §9 — Status categories (six)
| Cat | Meaning |
|---|---|
| `current` | synchronized to approved basis; no findings |
| `stale` | downstream depended on changed approved truth |
| `uncovered` | approved upstream lacks required downstream realization |
| `dangling` | downstream references a removed upstream |
| `drifted` | semantic mismatch, direct edit, or unvalidated divergence |
| `obsolete` | upstream basis superseded conceptually; not just hash-different |

`uncovered` distinct from `stale`. `obsolete` requires user mark or heuristic.

## §10 — Cognitive surface
Item-count compression as roadmap target.

## §11 — Traces (canonical families)
| Trace | Purpose |
|---|---|
| `approval` | who/what approved which contract basis |
| `generation` | what task generated what artifact from which basis |
| `eval` | what checks ran, what findings |
| `code-sync` | source-map connection from code → contract IDs + validation |
| `decision` | human decision history (ADR/PDR/UDR/IDR/general) |
| `import` | brownfield import evidence + confidence |
| `id-registry` | allocation state + retired IDs |

### §11.1 Decision trace classification (load-bearing)
| record_type | What | Primary tier |
|---|---|---|
| IDR | Intent Decision | intent-specs |
| PDR | Product Decision | product-specs |
| UDR | UX Decision | ux-specs |
| ADR | Architecture Decision | system-specs |
| general | process/methodology | none |

Classification by **primary** tier; multi-tier impact in `affects: [item_ids]` field. `load_bearing: bool` default false; flip to false when no longer binding.

## §12 — Operations
- `init`: bootstrap ungoverned repo with draft intent in selected mode.
- `import`: brownfield bootstrap; produces draft candidates with confidence/evidence.
- `generate`: regenerate affected/stale/uncovered downstream from approved upstream.
- `eval`: read-only validation of target against approved upstream.
- `review`: interactive findings loop on a single target; doesn't propagate.
- `reconcile`: interactive stale/drift loop; user steers direction.
- `approve`: advance reviewed approval unit from draft to approved; structural eval pass required; writes approval trace.
- `status`: read-only report.

## §13 — Review and reconciliation packets
Bounded human review surfaces. Generated by engine, presented by skill, editable by user. Default surface: changed IDs, upstream basis, findings, proposed fixes/directions, downstream impact, recommendation, evidence, traces.

## §14 — Eval

### §14.1 Structural eval (engine-side, decidable)
- lifecycle consistency,
- required fields,
- ID validity & registry consistency,
- reference integrity,
- tier order & DAG validity,
- coverage & uncovered items,
- dangling references,
- component/container ownership rules,
- context sufficiency,
- trace and code-sync consistency where available.

### §14.2 Semantic eval (skill-side, heuristic)
Faithful representation, naming consistency, implicit dependency, capability gaps, UX/product mismatch, mockup extraction gaps, target-platform mismatch.

### §14.3 Verification ladder (load-bearing)
| Tier | What | v0.3 today | Trajectory |
|---|---|---|---|
| **Decidable** | Structural eval — pure compute | engine checks | grows as new structural rules codified |
| **Mechanical** | Validation runners — orchestrator-invoked commands | runners declared in `validation-registry.md` | grows as runner library accumulates |
| **Heuristic** | Semantic eval — agent-judged | dimensions above | shrinks as dimensions promoted into mechanical/structural |

The ladder is the trajectory: promote heuristic → mechanical → structural over time.

## §15 — Change classification
| Change | Default |
|---|---|
| typo, formatting | non-breaking if hash+eval confirm |
| clarifying wording | approval-relevant, usually non-breaking |
| behavioral change | breaking |
| `derives_from` change | usually breaking |
| ID/scope/container/component move | breaking |
| deletion | breaking |
| new consistent item | non-breaking; may create uncovered downstream |

## §16 — Workflow shapes
| Workflow | Chain |
|---|---|
| New project | `init --mode X` → review intent → approve intent → generate → status |
| Brownfield | `import --mode X` → review (top-down) → approve (top-down) → generate (uncovered) → reconcile (drifted) → status |
| Product+UX co-synthesis | approve intent → iterative generate product ⇄ ux → approve both → generate system |
| ux-led | `init --mode ux` → drop mockups → approve intent + ux → generate product --from ux → PM peer-review+approve → system auto-advances → generate code |
| Reconciliation | status → reconcile → bounded generate → eval → traces |

## §17 — Non-goals
Not formal verification; not TDD; not UI design tool; not deterministic compiler; not human-judgment replacement at approval gates; not a guarantee humans never inspect code in v03; not a normative DDD claim.

## Verification ladder summary
- **Decidable** = structural eval = engine = no LLM. The engine implements this rung.
- **Mechanical** = validation runners = orchestrator-invoked = declared in registry. Engine parses; orchestrator invokes.
- **Heuristic** = semantic eval = LLM = skill concern. Engine ships hooks (eval trace schema), not the judgment.

## Layered architecture rules summary
- Container carries `layer` ∈ {presentation, application, domain, infrastructure}.
- BCs **only in `domain`-layer** components.
- Component → exactly one container.
- Bounded context → exactly one component.
- Containment chain: container ⊇ component ⊇ bounded context.

## Tier distinctions
- **Contract** (lifecycle: draft/approved): intent-specs, product-specs, ux-specs, system-specs.
- **Context** (no lifecycle, derived from contract): config (AGENTS/CLAUDE), bdd/scenarios.
- **Code** (synchronized + validated, not approved).
- **Trace** (parallel durable provenance, append-only).
