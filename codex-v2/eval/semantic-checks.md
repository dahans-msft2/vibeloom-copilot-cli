# Semantic Checks

These checks are warnings. They do not self-resolve and they do not grant approval authority to the agent.

## Report Format

Use this shape:

```text
Semantic Checks
===============

Check: [name]
Result: PASS | WARNING
Details: [specific observations]
```

## Check List

### EVAL-SEM-001 — Requirement to story coverage

Check that each `PRD-FR-*` requirement is represented by one or more `STORY-*` items and that the story acceptance criteria can plausibly satisfy the requirement.

**How to check:**
1. List all `PRD-FR-*` requirements from prd.md.
2. For each requirement, search usm.md stories for explicit references to that requirement ID.
3. If no explicit reference is found, reason about whether any story addresses the requirement semantically (by matching intent, not just ID).
4. Build a coverage matrix:

```
| Requirement | Covered by stories | Status |
|-------------|-------------------|--------|
| PRD-FR-001  | STORY-E01-S01, STORY-E01-S02 | ✅ Covered |
| PRD-FR-002  | STORY-E02-S01 | ✅ Covered |
| PRD-FR-003  | (none found) | ⚠️ Not covered |
```

5. For each covered requirement, verify the story's acceptance criteria can plausibly satisfy the requirement — not just that the IDs are linked.

**Warn if:** A requirement is unrepresented or only covered by a vague story whose acceptance criteria do not address the requirement's specifics.

---

### EVAL-SEM-002 — Story to entity coverage

Check that each `STORY-*` item references one or more `ENT-*` items or a clearly intentional cross-cutting concern.

**How to check:**
1. List all stories from usm.md.
2. For each story, check for `ENT-*` references in the entity column or body text.
3. If a story has no entity references, reason about whether it implies entities not yet captured in dm.md.
4. Build an output table:

```
| Story | Entity refs | Status |
|-------|------------|--------|
| STORY-E01-S01 | ENT-ORDER-01, ENT-USER-01 | ✅ Linked |
| STORY-E01-S02 | ENT-ORDER-01 | ✅ Linked |
| STORY-E02-S01 | (none) | ⚠️ No entity — cross-cutting? |
```

5. For stories flagged as having no entity, note whether they are legitimately cross-cutting (e.g., authentication, logging) or whether a missing entity should be added to dm.md.

**Warn if:** A story appears semantically important but touches no domain concept. Suggest which entities might be missing.

---

### EVAL-SEM-003 — Entity and invariant necessity

Check that each `ENT-*` and `INV-*` item is justified by one or more upstream stories or requirements.

**How to check:**
1. List all entity IDs (`ENT-*`) and invariant IDs (`INV-*`) from dm.md.
2. Search usm.md and prd.md for references to each entity and invariant ID.
3. If an entity is not referenced, reason about whether it is legitimately needed (e.g., system entities for audit trails, infrastructure concerns).
4. Build an output table:

```
| Entity/Invariant | Referenced by | Status |
|-----------------|---------------|--------|
| ENT-ORDER-01 | STORY-E01-S01, STORY-E01-S02 | ✅ Justified |
| ENT-AUDIT-01 | (none — system entity) | ✅ System-level, acceptable |
| ENT-LEGACY-01 | (none) | ⚠️ Orphan — over-modeled? |
| INV-ORDER-01 | STORY-E01-S03 | ✅ Justified |
| INV-CART-02 | (none) | ⚠️ No behavioral consequence found |
```

**Warn if:** The domain model appears over-modeled or if an invariant has no visible behavioral consequence.

---

### EVAL-SEM-004 — Workflow completeness

Check that the `USM` captures the critical end-to-end flows implied by the PRD and intent, including approval and reconcile steps when they are user-visible workflow concepts.

**How to check:**
1. Read the intent and PRD to identify all critical end-to-end user workflows (e.g., "user signs up, creates a project, invites collaborators, publishes").
2. For each workflow, trace it through the USM epics and stories to verify all steps are captured.
3. Pay special attention to:
   - Error and recovery paths (what happens when a step fails?)
   - Approval or review gates (if the product requires human approval at certain steps)
   - Reconciliation steps (e.g., syncing after offline use)
4. Flag any workflow that has a gap — a transition the PRD assumes but the USM does not model.

**Warn if:** The workflow model skips a key transition that the product requirements assume.

---

### EVAL-SEM-005 — Boundary sanity

Check that module boundaries in `spec.md` match domain semantics in `dm.md` and workflow slices in `usm.md`.

**How to check:**
1. List all entities from dm.md grouped by bounded context.
2. For each module in spec.md, list the entities it owns.
3. Build an ownership matrix:

```
| Entity | Bounded context (dm.md) | Owning module (spec.md) | Status |
|--------|------------------------|------------------------|--------|
| ENT-ORDER-01 | Orders | SPEC-MOD-01 (orders-svc) | ✅ Single owner, context-aligned |
| ENT-ORDER-02 | Orders | SPEC-MOD-01 (orders-svc) | ✅ Single owner, context-aligned |
| ENT-PAY-01 | Payments | SPEC-MOD-02 (payments-svc) | ✅ Single owner, context-aligned |
| ENT-ORDER-03 | Orders | SPEC-MOD-02 (payments-svc) | ⚠️ Cross-context ownership |
| ENT-INV-01 | Inventory | (none) | ⚠️ Unassigned |
```

4. Verify that module boundaries align with bounded context boundaries — a module should not split an aggregate or own entities from multiple unrelated contexts.
5. Check that no two modules own the same entity.

**Warn if:** A module split appears to cut across a single aggregate, multiple modules appear to own the same responsibility, or an entity is unassigned.

---

### EVAL-SEM-006 — Context slice sufficiency

Check that the context-loading protocol includes enough upstream truth to implement safely without loading unrelated contracts.

**How to check:**
1. Review the context-loading protocol or context slice definitions.
2. For each implementation task, identify which upstream artifacts must be loaded.
3. Evaluate whether the slice is:
   - **Too narrow**: Missing upstream artifacts that the task depends on. Concrete criteria:
     - The task references entity IDs not present in the loaded context.
     - The task implements a story whose acceptance criteria reference requirements not in the slice.
     - The task touches a module interface whose contract is not loaded.
     - The spec section for the relevant module is absent.
   - **Too broad**: Loading artifacts unrelated to the task. Concrete criteria:
     - The slice includes module specs for modules not touched by the task.
     - The slice loads the full PRD when only a subset of requirements is relevant.
     - The slice includes bounded contexts with no entity overlap with the task.
     - More than 60% of loaded content is irrelevant to the task at hand.
4. Verify that the slice includes the full trace chain for the items being implemented (requirement → story → entity → spec module).

**Warn if:** The slice looks too narrow to be safe (missing critical dependencies) or too broad to be practical (loading excessive unrelated context).

---

### EVAL-SEM-007 — Import confidence review

Check that the import path preserves uncertainty instead of presenting inferred semantics as authoritative fact.

**How to check:**
1. Identify all artifacts or sections that were generated via import (e.g., from an existing codebase, external documentation, or AI inference).
2. Verify that imported content is marked with a confidence level or provenance indicator.
3. Check that the import flow includes a human review step before imported content is promoted to `approved` status.
4. Look for any inferred relationships, entity names, or invariants that are presented as established fact without evidence.

**Warn if:** Imported artifacts lack visible confidence markers or if the import flow bypasses human review.

---

### EVAL-SEM-008 — Local bugfix path correctness

Check that the steady-state bugfix path starts from repro, expected behavior, and regression coverage before broad re-import or full upstream regeneration.

**How to check:**
1. Review the methodology's bugfix workflow documentation.
2. Verify the bugfix path follows this sequence:
   - Reproduce the defect.
   - Identify expected behavior from upstream contracts.
   - Write or update a regression test.
   - Fix the code.
   - Verify the fix does not break other tests.
3. Verify that the bugfix path does NOT default to full upstream regeneration or broad re-import for routine defects.
4. Check that bootstrapping behavior (full re-import) is reserved for unmanaged repos or major structural changes, not routine bugs.

**Warn if:** Routine defect handling appears to depend on bootstrapping behavior meant for unmanaged repos.

---

### EVAL-SEM-009 — Derived artifact restraint

Check that `AGENTS.md` and `plan.md` remain lean, scoped, and explicitly derived from upstream truth.

**How to check:**
1. Read `AGENTS.md` and `plan.md` (if they exist).
2. Compare their content against the canonical artifacts they are derived from.
3. Flag if either artifact:
   - Duplicates large sections (more than a few lines) of canonical contracts verbatim.
   - Introduces new requirements, entities, or invariants not present in upstream canonical artifacts.
   - Contains decision rationale or architectural guidance that should live in spec.md.
4. Verify that both artifacts explicitly state they are derived and regenerable.

**Warn if:** Derived artifacts duplicate large sections of canonical contracts or begin to carry semantic authority of their own.

---

### EVAL-SEM-010 — Projection restraint

Check that the methodology does not introduce a large set of persistent generated artifacts that would overwhelm context loading and review.

**How to check:**
1. Inventory all generated or projected artifacts required by the methodology.
2. Compare against the three allowed durable projections: trace index, dependency/stale graph, interface/schema manifests.
3. Flag any additional persistent generated artifacts beyond these three.
4. Assess whether the total volume of generated content is manageable for human review.

**Warn if:** The design drifts toward artifact sprawl beyond the three allowed durable projections.
