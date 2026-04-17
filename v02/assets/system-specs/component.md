<!--
VibeLoom template: component (per-component spec)
Tier: system-specs (full modes only) — terminal node in the derivation graph.
Purpose: full contract for one owned technical boundary.
Structured content: IF-####, DEP-####, BEH-####, NOTE-####. These are addressable items but NOT independent graph nodes (per Boundary Principle).

Derivation rules (per DAG) for the component itself:
- component derives from AGG, ENT, BC, CONT, FLOW, VO

Generator guidance:
- `container_id`, `component_id`, `bounded_context` identify the component's ownership.
- `owned_paths` and `owned_interfaces` in frontmatter are SUMMARY INDEXES — the body IF table and explicit path declarations are the source of truth. Frontmatter is regenerated from the body.
- Every component belongs to exactly one container and exactly one bounded context.
- Interfaces, dependencies, behaviors, and notes are structured content, not graph entities. They are not subject to DAG edge validation.
- Each IF-#### is an interface this component provides. Each DEP-#### is a dependency on another component or external system. Each BEH-#### is a local behavior contract. Each NOTE-#### captures a local test or runtime concern.
-->

---
artifact_id: component.<container-slug>.<component-slug>
artifact_type: component
tier: system-specs
scope_kind: component
scope_id: <container-slug>.<component-slug>
container_id: <CONT-####>
component_id: <CMP-####>
bounded_context: <BC-####>
owned_paths: []
owned_interfaces: []
status: draft
timestamp: "<ISO-8601 timestamp>"
derives_from: []
---

# Component — <component-slug>

<!-- One-paragraph statement of what this component owns and why it exists. -->

## Responsibility

<!-- Clear statement of the component's technical boundary: what it does, what it does not do. -->

## Owned paths

<!-- Filesystem patterns this component owns. The body is source of truth; frontmatter owned_paths is a summary. -->

| path | notes |
|---|---|
| | |

## Owned interfaces

<!-- Interfaces this component provides to other components or external consumers. Each IF-#### is structured content. -->

| id | name | kind | description | notes |
|---|---|---|---|---|
| IF-0001 | | | | |

## Dependencies

<!-- Components or external systems this component consumes. Each DEP-#### references a provider. -->

| id | target | kind | notes |
|---|---|---|---|
| DEP-0001 | | | |

## Behaviors

<!-- Local behavior contracts. Each BEH-#### is a statement about how this component behaves under specific conditions. -->

| id | description | notes |
|---|---|---|
| BEH-0001 | | |

## Notes

<!-- Local test or runtime notes. Each NOTE-#### captures a concern the implementer should remember. -->

| id | kind | note |
|---|---|---|
| NOTE-0001 | | |
