# Tier 1 — Structural Eval Instructions

These are instructions for the Agent to perform Tier 1 structural evaluations. Tier 1 checks are **blocking** — artifact approval cannot proceed if any check fails.

## How to Perform Structural Evals

For each artifact in scope, read it fully and perform the checks listed below. Report results in this format:

```
Tier 1 — Structural Evals
══════════════════════════

Check: ID format compliance
Result: ✅ PASS | ❌ FAIL
Details: [specific findings]

Check: Cross-reference integrity
Result: ✅ PASS | ❌ FAIL
Details: [specific findings]

...

Summary: X/Y checks passed. [BLOCKING if any failed]
```

---

## Check 1: ID Format Compliance

**What:** Verify all items in all artifacts use the correct ID format.

**Expected formats:**

| Artifact | ID Pattern | Regex | Examples |
|----------|-----------|-------|---------|
| prd.md | `PRD-{nnn}` | `PRD-\d{3}` | PRD-001, PRD-012 |
| prd.md (NFRs) | `NFR-{nn}` | `NFR-\d{2}` | NFR-01, NFR-05 |
| prd.md (users) | `USR-{nn}` | `USR-\d{2}` | USR-01, USR-03 |
| usm.md | `USM-E{nn}-S{nn}` | `USM-E\d{2}-S\d{2}` | USM-E01-S03 |
| usm.md (cross-cutting) | `USM-CC-S{nn}` | `USM-CC-S\d{2}` | USM-CC-S01 |
| dm.md | `DM-{BC}-E{nn}` | `DM-BC\d+-E\d{2}` | DM-BC1-E05 |
| dm.md (events) | `DM-{BC}-EVT-{nn}` | `DM-BC\d+-EVT-\d{2}` | DM-BC1-EVT-01 |
| spec.md (APIs) | `SPEC-API-{nn}` | `SPEC-API-\d{2}` | SPEC-API-01 |
| spec.md (modules) | `SPEC-MOD-{nn}` | `SPEC-MOD-\d{2}` | SPEC-MOD-01 |
| module spec (APIs) | `MOD-{name}-API-{nn}` | `MOD-\w+-API-\d{2}` | MOD-ORDERS-API-01 |
| module spec (events) | `MOD-{name}-EVT-{nn}` | `MOD-\w+-EVT-\d{2}` | MOD-ORDERS-EVT-01 |

**How to check:**
1. Read each artifact
2. Find all items that should have IDs (table rows with ID columns, list items with IDs)
3. Verify each ID matches the expected pattern for its artifact type
4. Report any IDs that don't match

**Fail if:** Any item has a missing or malformed ID.

---

## Check 2: Cross-Reference Integrity

**What:** Verify all IDs referenced in downstream artifacts actually exist in upstream artifacts.

**Cross-reference chains to verify:**

| Downstream artifact | Reference field | Must exist in |
|--------------------|----------------|---------------|
| usm.md stories | `Entities` column (DM-xx refs) | dm.md entity IDs |
| usm.md stories | `USR-xx` refs | prd.md user IDs |
| prd.md requirements | `USR-xx` refs in User(s) column | prd.md user IDs |
| spec.md APIs | `USM-xx` refs in Stories column | usm.md story IDs (or prd.md USM section) |
| spec.md modules | BC references | dm.md bounded context IDs |
| module spec | Entity ID refs | dm.md entity IDs |
| module spec imports | `MOD-{other}-API-xx` refs | Other module's export IDs |

**How to check:**
1. For each downstream artifact, find all cells/fields that reference upstream IDs
2. Collect all referenced IDs
3. Check that each referenced ID exists in the appropriate upstream artifact
4. Report any "dangling references" — IDs that don't resolve

**Fail if:** Any referenced ID does not exist in its upstream artifact.

---

## Check 3: Artifact Completeness

**What:** Verify all required sections are present and non-empty in each artifact.

**Required sections per artifact:**

| Artifact | Required sections |
|----------|------------------|
| intent.md | "What is this application?", "Who are the primary users?", "Core capabilities" |
| prd.md | "Overview", "Users & Personas" (with ≥1 user), "Requirements" (with ≥1 requirement), "Scope Boundaries" |
| prd.md (Lite) | All of above + "User Story Map" section with ≥1 epic and ≥1 story |
| usm.md | ≥1 epic with ≥1 story each |
| dm.md | ≥1 bounded context with ≥1 entity, "Relationships" section, "Glossary" |
| spec.md | "Tech Stack", "Runtime Architecture", "Data Architecture", "API Design", "Security", "Deployment Architecture" |
| spec.md (Full) | All of above + "Module Decomposition", "Dependency DAG", "Module Interface Contracts" |
| module spec | "Domain Entities Owned", "Interface Contract" (Exports + Imports), "Internal Architecture" |
| AGENTS.md | "Tech Stack", "Commands", "Code Style & Conventions", "Boundaries" |

**How to check:**
1. For each artifact, verify each required section exists as a heading
2. Verify each required section has content (not just the heading with empty placeholder text)
3. For table sections, verify at least the minimum number of data rows

**Fail if:** Any required section is missing or completely empty.

---

## Check 4: Module Structure Compliance (Full Profile Only)

**What:** Verify the file system matches the module decomposition in spec.md.

**How to check:**
1. Read the Module Decomposition table in spec.md
2. For each module listed:
   - Verify the directory exists at the specified path
   - Verify `spec.md` exists in the module directory
   - Verify `AGENTS.md` exists in the module directory
3. Verify no module directories exist that aren't listed in spec.md

**Fail if:** Any module directory is missing required files, or undeclared module directories exist.

---

## Check 5: Upstream-Ref Validity

**What:** Verify all `upstream-refs` in artifact frontmatter point to existing artifacts.

**How to check:**
1. For each artifact, read the `upstream-refs` array in frontmatter
2. For each ref, verify the referenced `artifact` file exists at the specified path
3. If the referenced artifact has a `version-hash`, verify it's an 8-character alphanumeric string

**Fail if:** Any upstream-ref points to a non-existent file.

---

## Check 6: Frontmatter Validity

**What:** Verify all artifacts have valid YAML frontmatter.

**Required frontmatter fields:**

| Field | Required | Valid values |
|-------|----------|-------------|
| status | Yes | `draft`, `approved`, `stale`, `approved-with-known-issues` |
| owner | Yes | Non-empty string |
| approved-by | Yes (can be empty) | `human` or empty |
| last-reviewed | Yes | `YYYY-MM-DD` format or `YYYY-MM-DD` placeholder |
| upstream-refs | Yes (can be empty array) | Array of `{artifact, version-hash}` objects |

**Fail if:** Any required field is missing or has an invalid value.
