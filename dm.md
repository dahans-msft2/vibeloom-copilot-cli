---
artifact_id: ART-DM-CODEX-V4
artifact_type: dm
status: draft
owner: methodology
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from:
  - ART-INTENT-CODEX-V4
  - ART-PRD-CODEX-V4
  - ART-USM-CODEX-V4
depends_on:
  - ART-INTENT-CODEX-V4
  - ART-PRD-CODEX-V4
  - ART-USM-CODEX-V4
---

# Domain Model: Codex V4 Methodology Package

## Bounded Contexts

### BC-001 — Contract Governance

**Description:** Owns canonical artifacts, traceability, evaluation, and reconciliation semantics.

**Aggregate roots:** ENT-001, ENT-004, ENT-005

#### Entities

| ID | Entity | Description | Key attributes | Invariants | Driven by stories / requirements |
| --- | --- | --- | --- | --- | --- |
| ENT-001 | Artifact | A canonical or derived document in the methodology | `artifact_id`, `artifact_type`, `status`, `version` | INV-001, INV-002 | STORY-001, STORY-002, STORY-006, STORY-008, STORY-010; PRD-FR-001, PRD-FR-007 |
| ENT-002 | Contract Item | A stable item inside an artifact, such as a requirement, story, entity, invariant, or module | `item_id`, `kind`, `label`, `artifact_id` | INV-003 | STORY-003, STORY-004, STORY-012; PRD-FR-001 |
| ENT-003 | Trace Link | A typed relationship connecting upstream and downstream contract items | `source_id`, `target_id`, `link_type` | INV-004 | STORY-012, STORY-013; PRD-FR-004, PRD-FR-009 |
| ENT-004 | Eval Run | A structural or semantic evaluation pass over a slice of artifacts | `eval_id`, `scope`, `result`, `timestamp` | INV-005 | STORY-002, STORY-008, STORY-009; PRD-FR-005, PRD-FR-008 |
| ENT-005 | Reconcile Session | A bounded attempt to resolve drift between approved truth and downstream reality | `session_id`, `trigger`, `resolution_path` | INV-006 | STORY-008, STORY-009; PRD-FR-005, PRD-FR-008 |
| ENT-006 | Change Class | A classification of scope used to choose context breadth and approval path | `class`, `confidence`, `reason` | INV-007 | STORY-007, STORY-013; PRD-FR-004 |

#### Invariants

| ID | Invariant | Applies to | Driven by stories / requirements |
| --- | --- | --- | --- |
| INV-001 | Each artifact has exactly one active lifecycle state at a time. | ENT-001 | STORY-002, STORY-008; PRD-FR-001 |
| INV-002 | Only humans may approve canonical artifacts. | ENT-001 | STORY-002; PRD-FR-001 |
| INV-003 | Every stable contract item belongs to exactly one canonical artifact version. | ENT-002 | STORY-012; PRD-FR-001 |
| INV-004 | Every downstream normative item must trace to at least one upstream normative item unless it is explicitly marked foundational. | ENT-003 | STORY-012; PRD-FR-004, PRD-FR-009 |
| INV-005 | Structural eval failures block approval; semantic eval warnings do not self-resolve. | ENT-004 | STORY-002, STORY-008; PRD-FR-005 |
| INV-006 | A reconcile session must end with either an upstream amendment proposal or a downstream correction proposal. | ENT-005 | STORY-008; PRD-FR-005 |
| INV-007 | Uncertain change classification escalates to the broader scope. | ENT-006 | STORY-007, STORY-013; PRD-FR-004 |

#### Relationships

| From | Relationship | To | Cardinality | Description |
| --- | --- | --- | --- | --- |
| ENT-001 | contains | ENT-002 | 1:N | Artifacts contain stable contract items |
| ENT-002 | links via | ENT-003 | 1:N | Contract items participate in trace links |
| ENT-004 | evaluates | ENT-001 | N:N | Eval runs may cover one or more artifacts |
| ENT-005 | resolves drift for | ENT-001 | N:N | Reconcile sessions operate over affected artifacts |
| ENT-006 | scopes | ENT-005 | 1:N | Change classification influences reconcile scope |

### BC-002 — Execution Coordination

**Description:** Owns modular execution boundaries, profiles, interface ownership, and scoped agent context.

**Aggregate roots:** ENT-007, ENT-008, ENT-010

#### Entities

| ID | Entity | Description | Key attributes | Invariants | Driven by stories / requirements |
| --- | --- | --- | --- | --- | --- |
| ENT-007 | Profile | A repo-level operating mode for artifact depth and module decomposition | `profile`, `selection_reason` | INV-008 | STORY-014; PRD-FR-010 |
| ENT-008 | Module | A unit of ownership and parallel execution derived from the technical spec | `module_id`, `name`, `bounded_context`, `write_surface` | INV-009, INV-010 | STORY-005, STORY-014; PRD-FR-011 |
| ENT-009 | Interface Contract | An owned API, event, schema, or other cross-boundary contract | `interface_id`, `owner_module`, `consumer_modules` | INV-011 | STORY-005; PRD-FR-011 |
| ENT-010 | Context Slice | The minimal set of artifacts and IDs loaded for a task | `slice_id`, `change_class`, `artifact_refs`, `item_refs` | INV-012 | STORY-006, STORY-007, STORY-013, STORY-015; PRD-FR-004, PRD-FR-010 |
| ENT-011 | Import Assessment | An inference result produced during brownfield import | `assessment_id`, `confidence`, `source_evidence` | INV-013 | STORY-010, STORY-011; PRD-FR-006 |

#### Invariants

| ID | Invariant | Applies to | Driven by stories / requirements |
| --- | --- | --- | --- |
| INV-008 | Exactly one repo profile is active at a time. | ENT-007 | STORY-014; PRD-FR-010 |
| INV-009 | Every write surface is owned by at most one module. | ENT-008 | STORY-005; PRD-FR-011, NFR-004 |
| INV-010 | Module dependencies must form an acyclic graph in `full` profile. | ENT-008 | STORY-005; PRD-FR-011, NFR-004 |
| INV-011 | Every interface contract has exactly one owner module. | ENT-009 | STORY-005; PRD-FR-011, NFR-004 |
| INV-012 | A context slice must include all referenced upstream truth and exclude unrelated modules unless escalation is required. | ENT-010 | STORY-006, STORY-007, STORY-013; PRD-FR-004, NFR-002 |
| INV-013 | Imported semantics must carry confidence signals until human approval removes uncertainty. | ENT-011 | STORY-010, STORY-011; PRD-FR-006 |

#### Relationships

| From | Relationship | To | Cardinality | Description |
| --- | --- | --- | --- | --- |
| ENT-007 | governs | ENT-008 | 1:N | Profile choice shapes module depth |
| ENT-008 | owns | ENT-009 | 1:N | Modules own interface contracts |
| ENT-010 | loads | ENT-001 | N:N | Context slices reference artifacts |
| ENT-010 | includes | ENT-002 | N:N | Context slices include contract items |
| ENT-011 | annotates | ENT-001 | N:N | Import assessments attach confidence to inferred artifacts or items |

## Domain Events

| ID | Event | Triggered by | Data | Consumers |
| --- | --- | --- | --- | --- |
| EVT-001 | ArtifactApproved | Human approval of a canonical artifact | `artifact_id`, `version`, `approved_by` | Reconcile engine, stale propagation |
| EVT-002 | ArtifactMarkedStale | Upstream dependency changed or drift detected | `artifact_id`, `reason` | Status reporting, reconcile engine |
| EVT-003 | ReconcileRequested | User or agent initiates targeted drift resolution | `session_id`, `scope`, `change_class` | Reconcile engine |
| EVT-004 | ImportCompleted | Brownfield import completes draft artifact generation | `artifact_ids`, `confidence_summary` | Human reviewer |

## Glossary

| Term | Definition |
| --- | --- |
| Canonical artifact | A long-lived project artifact that carries normative meaning |
| Derived artifact | An execution-oriented artifact that may be regenerated from canonical truth |
| Stale cascade | Deterministic marking of dependent artifacts after an approved upstream change |
| Context slice | The minimum safe contract subset required for a task |
| Write surface | The files, schemas, or routes a module is allowed to mutate directly |
