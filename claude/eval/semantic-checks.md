# Tier 2 — Semantic Eval Instructions

These are instructions for the Agent to perform Tier 2 semantic evaluations. Tier 2 results are **warnings** — presented to the human who decides whether to fix or proceed.

## How to Perform Semantic Evals

For each check, reason about meaning and coverage across artifacts. Report results:

```
Tier 2 — Semantic Evals
════════════════════════

Check: Requirements → Stories coverage
Result: ✅ PASS | ⚠️ WARNING
Details: [specific findings with coverage matrix]

...

Summary: X/Y checks passed, Z warnings.
```

---

## Check 1: Requirements → Stories Coverage

**What:** Every functional requirement in prd.md should be covered by at least one story in usm.md (or the USM section of prd.md).

**How to check:**
1. List all `PRD-xxx` requirements from prd.md
2. For each requirement, search usm.md stories for references to that requirement ID, OR reason about whether any story addresses the requirement semantically
3. Build a coverage matrix:

```
| Requirement | Covered by stories | Status |
|-------------|-------------------|--------|
| PRD-001     | USM-E01-S01, USM-E01-S02 | ✅ Covered |
| PRD-002     | USM-E02-S01 | ✅ Covered |
| PRD-003     | (none found) | ⚠️ Not covered |
```

**Warn if:** Any requirement has no covering stories.

---

## Check 2: Stories → Entities Coverage

**What:** Every story in usm.md should reference at least one entity from dm.md. Stories that don't touch any domain entity may indicate a missing entity or a story that's too abstract.

**How to check:**
1. List all stories from usm.md
2. For each story, check the Entities column for DM-xx references
3. If a story has no entity references, reason about whether it implies entities not yet captured in dm.md

**Warn if:** Any story has no entity references. Suggest which entities might be missing.

---

## Check 3: Entity Coverage (no orphans)

**What:** Every entity in dm.md should be referenced by at least one story in usm.md. Orphan entities may indicate over-modeling or missing stories.

**How to check:**
1. List all entity IDs from dm.md
2. Search usm.md for references to each entity ID
3. If an entity is not referenced, reason about whether it's legitimately needed (e.g., system entities for audit, infrastructure)

**Warn if:** Any entity is not referenced by any story. Note whether the entity might be a legitimate system-level entity.

---

## Check 4: Contradiction Detection

**What:** Check for logical contradictions between artifact tiers.

**Common contradictions to look for:**
- A story describes behavior that contradicts a requirement's acceptance criteria
- An entity relationship in dm.md contradicts the cardinality implied by stories
- A spec.md decision contradicts a requirement (e.g., "offline-first" requirement but spec has no offline support)
- Module boundaries split entities that the domain model keeps in the same aggregate
- Security requirements in prd.md not addressed in spec.md security section
- NFRs in prd.md not referenced in spec.md observability/deployment sections

**How to check:**
1. Read each artifact carefully for claims about system behavior
2. Cross-reference claims between tiers
3. Flag any statements that cannot both be true

**Warn if:** Any contradiction found. Quote the specific conflicting statements.

---

## Check 5: Module → Entity Completeness (Full Profile)

**What:** Every entity in dm.md should be owned by exactly one module in spec.md. No entity should be unassigned or assigned to multiple modules.

**How to check:**
1. List all entities from dm.md
2. For each module spec, list the entities in its "Domain Entities Owned" section
3. Build an ownership matrix:

```
| Entity | Owned by | Status |
|--------|----------|--------|
| DM-BC1-E01 | SPEC-MOD-01 | ✅ Single owner |
| DM-BC1-E02 | SPEC-MOD-01 | ✅ Single owner |
| DM-BC2-E01 | (none) | ⚠️ Unassigned |
| DM-BC1-E03 | SPEC-MOD-01, SPEC-MOD-02 | ⚠️ Multiple owners |
```

**Warn if:** Any entity is unassigned or has multiple owners.

---

## Check 6: Interface Contract Completeness (Full Profile)

**What:** Every import in a module's interface contract should match an export in the referenced module.

**How to check:**
1. For each module, list all imports
2. For each import, find the referenced module's exports
3. Verify the import signature matches the export signature (function name, parameter types, return type)

**Warn if:** Any import doesn't match a corresponding export, or signatures differ.

---

## Check 7: Dependency DAG Validation (Full Profile)

**What:** The module dependency graph must be acyclic.

**How to check:**
1. Build the dependency graph from module imports
2. Check for cycles (if A imports from B, and B imports from A — either directly or transitively)
3. Compare the actual dependency graph against the declared DAG in spec.md

**Warn if:** Any cycle detected, or actual dependencies differ from declared DAG.

---

## Check 8: Spec Completeness Against NFRs

**What:** Every non-functional requirement (NFR-xx) in prd.md should be addressed in spec.md.

**How to check:**
1. List all NFR-xx items from prd.md
2. Search spec.md for references to each NFR ID
3. For unreferenced NFRs, check if the concern is addressed semantically (e.g., NFR about performance might be covered in deployment/scaling section without explicit ID reference)

**Warn if:** Any NFR has no corresponding treatment in spec.md.

---

## Check 9: Story-to-API Traceability

**What:** Every story in usm.md should be implementable through the APIs defined in spec.md.

**How to check:**
1. For each story, reason about what API calls would be needed to implement it
2. Check if those APIs exist in spec.md's API Design section
3. Flag stories that imply APIs not yet defined

**Warn if:** Any story implies APIs not defined in spec.md.

---

## Check 10: Invariant Preservation

**What:** Domain invariants declared in dm.md should not be violatable by the API design in spec.md.

**How to check:**
1. List all invariants from dm.md entity definitions
2. For each invariant, reason about whether the API design in spec.md could allow it to be violated
3. Check if the spec mentions enforcement mechanisms (validation, constraints, transactions)

**Warn if:** Any invariant could potentially be violated by the current API design without explicit enforcement.
