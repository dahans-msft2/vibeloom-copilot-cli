# Structural Checks

These checks are blocking. A canonical artifact cannot be approved while a structural check fails.

## Report Format

Use this shape:

```text
Structural Checks
=================

Check: [name]
Result: PASS | FAIL
Details: [specific failures]
```

## Check List

### EVAL-STRUCT-001 — Metadata completeness

Verify that every canonical artifact includes valid YAML frontmatter with all required fields.

**Required frontmatter fields:**

| Field | Required | Valid values |
|-------|----------|-------------|
| `artifact_id` | Yes | Non-empty string matching the artifact filename stem |
| `artifact_type` | Yes | `intent`, `prd`, `usm`, `dm`, `spec`, `module-spec`, `agents`, `plan` |
| `status` | Yes | `draft`, `approved`, `stale`, `superseded`, `approved-with-known-issues` |
| `owner` | Yes | Non-empty string |
| `approved_by` | Yes (can be empty) | `human` or empty |
| `last_reviewed` | Yes | `YYYY-MM-DD` format |
| `version` | Yes | Semver string or integer ≥ 1 |
| `derived_from` | Yes (can be empty array) | Array of artifact references |
| `depends_on` | Yes (can be empty array) | Array of `{artifact, version-hash}` objects |

**How to check:**
1. Open each canonical artifact and locate the YAML frontmatter block (between `---` fences).
2. Parse the YAML. If parsing fails, report FAIL immediately.
3. For each field in the table above, verify:
   - The field exists.
   - Its value matches one of the listed valid values or value patterns.
4. Verify `last_reviewed` matches regex `^\d{4}-\d{2}-\d{2}$`.
5. Verify `depends_on` entries each contain both `artifact` and `version-hash` keys.

**Fail if:** Any required field is missing, unparseable, or has an invalid value.

---

### EVAL-STRUCT-002 — Artifact authority

Verify that:
- only `intent`, `prd`, `usm`, `dm`, and `spec` are treated as canonical project contracts
- `constitution.md` is treated as the governing baseline
- `AGENTS.md` and `plan.md` are described as derived, regenerable, and non-canonical

**How to check:**
1. Read the constitution and all artifact templates.
2. Search for any language that grants `AGENTS.md` or `plan.md` semantic authority equal to canonical artifacts.
3. Search for any artifact type outside the canonical set being treated as a contract.
4. Verify that derived artifacts are explicitly labeled as regenerable.

**Fail if:** Any template or doc elevates `AGENTS.md` or `plan.md` to peer semantic authority, or introduces an unauthorized canonical artifact type.

---

### EVAL-STRUCT-003 — ID grammar compliance

Verify that all stable IDs use approved prefixes and follow the correct format for their artifact type.

**Approved ID formats:**

| Artifact / Context | ID Pattern | Regex | Examples |
|---|---|---|---|
| prd.md (functional reqs) | `PRD-FR-{nnn}` | `^PRD-FR-\d{3}$` | PRD-FR-001, PRD-FR-012 |
| prd.md (NFRs) | `NFR-{nn}` | `^NFR-\d{2}$` | NFR-01, NFR-05 |
| prd.md (users) | `USR-{nn}` | `^USR-\d{2}$` | USR-01, USR-03 |
| prd.md (goals) | `GOAL-{nnn}` | `^GOAL-\d{3}$` | GOAL-001, GOAL-010 |
| prd.md (metrics) | `METRIC-{nnn}` | `^METRIC-\d{3}$` | METRIC-001, METRIC-005 |
| prd.md (acceptance criteria) | `AC-{nnn}` | `^AC-\d{3}$` | AC-001, AC-015 |
| usm.md (stories) | `STORY-E{nn}-S{nn}` | `^STORY-E\d{2}-S\d{2}$` | STORY-E01-S03 |
| usm.md (cross-cutting) | `STORY-CC-S{nn}` | `^STORY-CC-S\d{2}$` | STORY-CC-S01 |
| dm.md (entities) | `ENT-{BC}-{nn}` | `^ENT-[A-Z0-9]+-\d{2}$` | ENT-ORDER-01, ENT-USER-05 |
| dm.md (invariants) | `INV-{BC}-{nn}` | `^INV-[A-Z0-9]+-\d{2}$` | INV-ORDER-01 |
| dm.md (events) | `EVT-{BC}-{nn}` | `^EVT-[A-Z0-9]+-\d{2}$` | EVT-ORDER-01 |
| spec.md (interfaces) | `IFACE-{nn}` | `^IFACE-\d{2}$` | IFACE-01, IFACE-05 |
| spec.md (APIs) | `SPEC-API-{nn}` | `^SPEC-API-\d{2}$` | SPEC-API-01 |
| spec.md (modules) | `SPEC-MOD-{nn}` | `^SPEC-MOD-\d{2}$` | SPEC-MOD-01 |
| module spec (APIs) | `MOD-{name}-API-{nn}` | `^MOD-\w+-API-\d{2}$` | MOD-ORDERS-API-01 |
| module spec (events) | `MOD-{name}-EVT-{nn}` | `^MOD-\w+-EVT-\d{2}$` | MOD-ORDERS-EVT-01 |
| tasks | `TASK-{nnn}` | `^TASK-\d{3}$` | TASK-001, TASK-042 |
| tests | `TEST-{nnn}` | `^TEST-\d{3}$` | TEST-001, TEST-015 |
| evals | `EVAL-{type}-{nnn}` | `^EVAL-(STRUCT\|SEM)-\d{3}$` | EVAL-STRUCT-001, EVAL-SEM-005 |
| artifacts (general) | `ART-{nnn}` | `^ART-\d{3}$` | ART-001, ART-010 |

**How to check:**
1. Read each artifact in scope.
2. Find all items that should have IDs (table rows with ID columns, list items with IDs, heading-anchored identifiers).
3. For each ID found, match it against the regex for its artifact type from the table above.
4. Check for duplicate IDs within the same governed scope (same artifact file or same module).
5. Check for items that should have an ID but are missing one (e.g., a requirement row with an empty ID column).

**Fail if:**
- Any item uses an undefined prefix not in the table above.
- Any expected stable item lacks an ID.
- Duplicate IDs exist in the same governed scope.
- Any ID does not match the regex for its artifact type.

---

### EVAL-STRUCT-004 — Reference integrity

Verify that every cross-reference points to an existing ID or artifact in scope.

**Cross-reference chains to verify:**

| Downstream artifact | Reference field / column | Must resolve to |
|---|---|---|
| usm.md stories | Entity references (`ENT-*`) | dm.md entity IDs |
| usm.md stories | User references (`USR-*`) | prd.md user IDs |
| prd.md requirements | User references (`USR-*`) | prd.md user IDs |
| spec.md APIs | Story references (`STORY-*`) | usm.md story IDs |
| spec.md modules | Bounded-context references | dm.md bounded context names |
| module spec | Entity ID refs (`ENT-*`) | dm.md entity IDs |
| module spec imports | `MOD-{other}-API-*` refs | Other module's export IDs |
| any artifact | `depends_on` entries | Existing artifact files |

**How to check:**
1. For each downstream artifact, scan all cells, fields, and inline references for upstream ID patterns (use the regex patterns from EVAL-STRUCT-003).
2. Collect all referenced IDs into a list.
3. For each referenced ID, locate the upstream artifact that should contain it.
4. Verify the ID exists in the upstream artifact.
5. If the downstream artifact has a `depends_on` frontmatter field, verify that every upstream artifact referenced in the body also appears in `depends_on`.

**Fail if:**
- A referenced ID does not exist in its upstream artifact (dangling reference).
- A template references an artifact type that is no longer valid.
- A downstream artifact points to an upstream artifact that is missing from its `depends_on`.

---

### EVAL-STRUCT-005 — Lifecycle correctness

Verify that lifecycle states are limited to `draft`, `approved`, `stale`, or `superseded`.

**How to check:**
1. For each artifact, read the `status` field in frontmatter.
2. Verify it is one of: `draft`, `approved`, `stale`, `superseded`, `approved-with-known-issues`.
3. Verify no language in any artifact or template allows agents to self-approve canonical artifacts (approval must require human action).
4. Verify that stale propagation is consistent with the dependency model: if artifact A depends on artifact B and B changes, A should become stale.

**Fail if:**
- An artifact uses an unsupported lifecycle state.
- Approval language allows agents to self-approve canonical artifacts.
- Stale behavior contradicts the dependency model.

---

### EVAL-STRUCT-006 — Profile correctness

Verify that:
- only `lite` and `full` profiles exist
- `usm.md` and `dm.md` are mandatory in both profiles
- `full` profile requires module and interface ownership rules

**How to check:**
1. Read the constitution and methodology docs for profile definitions.
2. Verify only `lite` and `full` are defined.
3. Verify `usm.md` and `dm.md` are listed as required in both profiles.
4. Verify the `full` profile explicitly requires module decomposition, module specs, and interface ownership.
5. Search for any reference to a third profile name.

**Fail if:** Any artifact reintroduces a third profile or omits `USM` / `DM` from either profile.

---

### EVAL-STRUCT-007 — Traceability completeness

Verify that the methodology requires traceability from:
- intent capabilities to PRD requirements
- PRD requirements to USM stories
- USM stories to DM entities and invariants
- DM entities and invariants to spec modules and interfaces
- changed contract items to tests

**Required sections per artifact:**

| Artifact | Required sections |
|----------|------------------|
| intent.md | "What is this application?", "Who are the primary users?", "Core capabilities" |
| prd.md | "Overview", "Users & Personas" (≥1 user), "Requirements" (≥1 requirement), "Scope Boundaries" |
| prd.md (Lite) | All of above + "User Story Map" section with ≥1 epic and ≥1 story |
| usm.md | ≥1 epic with ≥1 story each |
| dm.md | ≥1 bounded context with ≥1 entity, "Relationships" section, "Glossary" |
| spec.md | "Tech Stack", "Runtime Architecture", "Data Architecture", "API Design", "Security", "Deployment Architecture" |
| spec.md (Full) | All of above + "Module Decomposition", "Dependency DAG", "Module Interface Contracts" |
| module spec | "Domain Entities Owned", "Interface Contract" (Exports + Imports), "Internal Architecture" |
| AGENTS.md | "Tech Stack", "Commands", "Code Style & Conventions", "Boundaries" |

**How to check:**
1. For each artifact in scope, verify all required sections from the table above exist as headings.
2. Verify each required section has substantive content (not just a heading with placeholder text).
3. For table sections, verify at least the minimum number of data rows (e.g., ≥1 user in "Users & Personas").
4. Trace a sample path through the full chain: pick one intent capability and verify you can follow it through PRD requirement, USM story, DM entity, and spec module.
5. Verify that test references exist for changed contract items.

**Fail if:** A tier breaks the required trace chain, or any required section is missing or completely empty.

---

### EVAL-STRUCT-008 — Projection budget

Verify that only these durable projections exist:
- trace index
- dependency/stale graph
- interface/schema manifests

**How to check:**
1. Read all docs and templates for references to generated or projected artifacts.
2. Verify only the three allowed durable projections are required.
3. Check that no template or workflow demands additional always-on generated outputs.

**Fail if:** Docs or templates require additional always-on durable projections beyond the three allowed.

---

### EVAL-STRUCT-009 — Module and interface ownership

Verify that the `full` profile requires:
- one owner per module write surface
- one owner per interface contract
- acyclic module dependencies

**How to check:**
1. For each module in spec.md, verify exactly one owner is declared.
2. For each interface contract, verify exactly one module owns the export side.
3. Build the module dependency graph from imports and verify it contains no cycles (direct or transitive).
4. Cross-check against the declared dependency DAG in spec.md.

**Fail if:** Ownership is ambiguous, optional, or a dependency cycle exists.

---

### EVAL-STRUCT-010 — Stale edge validity

Verify that stale propagation is driven by explicit dependency edges and asymmetric reconciliation rules.

**How to check:**
1. Read the dependency model from the constitution or methodology docs.
2. Verify that when an upstream artifact changes, all artifacts listing it in `depends_on` are marked stale.
3. Verify that downstream changes cannot automatically overwrite approved upstream truth (asymmetric reconciliation).
4. Trace at least one example stale edge: simulate a change to a dm.md entity and verify it would stale the spec.md and any module specs that depend on it.

**Fail if:**
- Upstream changes do not stale dependent artifacts.
- Downstream changes are allowed to overwrite approved upstream truth automatically.
