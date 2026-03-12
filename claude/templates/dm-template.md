---
status: draft
owner: dm
approved-by:
last-reviewed: YYYY-MM-DD
upstream-refs:
  - artifact: intent.md
    version-hash:
  - artifact: prd.md
    version-hash:
  - artifact: usm.md
    version-hash:
---

# Domain Model: [Project Name]

<!-- The domain model defines entities and relationships as seen by system users — NOT internal technical details. This is the semantic anchor of the methodology. -->

## Bounded Contexts

<!-- For Lite profile: single bounded context. For Full profile: multiple bounded contexts with a context map. -->

### BC1 — [Context Name]

**Description:** <!-- One sentence describing what this context owns -->

**Aggregate roots:** DM-BC1-E01, DM-BC1-E03

#### Entities

| ID | Entity | Description | Key attributes | Invariants |
|----|--------|-------------|---------------|------------|
| DM-BC1-E01 | | | | |
| DM-BC1-E02 | | | | |
| DM-BC1-E03 | | | | |

#### Relationships

| From | Relationship | To | Cardinality | Description |
|------|-------------|-----|-------------|-------------|
| DM-BC1-E01 | has many | DM-BC1-E02 | 1:N | |
| DM-BC1-E01 | belongs to | DM-BC1-E03 | N:1 | |

#### Domain Events

| ID | Event | Triggered by | Data | Consumers |
|----|-------|-------------|------|-----------|
| DM-BC1-EVT-01 | | | | |

<!-- For Full profile, add more bounded contexts: -->

<!-- ### BC2 — [Context Name] -->
<!-- ... same structure ... -->

## Context Map (Full Profile Only)

<!-- How bounded contexts relate to each other -->

| Upstream BC | Downstream BC | Relationship | Integration pattern |
|-------------|---------------|-------------|---------------------|
| BC1 | BC2 | Customer-Supplier | API calls |

## Glossary

<!-- Domain terms with precise definitions to prevent ambiguity -->

| Term | Definition |
|------|-----------|
| | |
