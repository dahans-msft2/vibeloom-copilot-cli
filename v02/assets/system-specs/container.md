<!--
VibeLoom template: container (per-container spec)
Tier: system-specs (full modes only)
Purpose: local runtime boundary; resident bounded contexts; authoritative component inventory; local dependency edges and local constraints.
Entities: CMP-#### (components owned by this container).
Derivation rules (per DAG):
- CMP derives from AGG, ENT, BC, CONT (its container), FLOW, VO

Local dependency edges and local constraints are structured content within this container spec, not independent graph nodes.

Generator guidance:
- Fill `container_id` with the governing CONT-#### from containers.md.
- Bounded contexts must not span multiple containers. List only BCs resident in this container.
- Every CMP references the container and at least one BC + optional AGG/ENT/FLOW/VO in derives_from.
- Components from the same BC must be co-located in this container.
-->

---
artifact_id: container.<container-slug>
artifact_type: container
tier: system-specs
scope_kind: container
scope_id: <container-slug>
container_id: <CONT-####>
status: draft
timestamp: "<ISO-8601 timestamp>"
derives_from: []
---

# Container — <container-slug>

<!-- One-paragraph statement of this container's purpose and runtime boundary. -->

## Resident bounded contexts

<!-- List BCs whose semantic home is this container. Each BC is owned by exactly one container. -->

| bounded_context | notes |
|---|---|
| BC-0001 | |

## Component inventory

<!-- Authoritative list of components inside this container. Each CMP derives from its container (CONT-####), at least one BC, and any relevant AGG/ENT/FLOW/VO. -->

| id | slug | description | bounded_context | derives_from | notes |
|---|---|---|---|---|---|
| CMP-0001 | | | | | |

## Local dependency edges

<!-- Structured content — how components inside this container relate. Not graph entities. -->

| from | to | kind | notes |
|---|---|---|---|
| CMP-0001 | | | |

## Local constraints

<!-- Local NFR/operational constraints specific to this container. Each item is structured content, not a graph entity. -->

| constraint | affects | notes |
|---|---|---|
| | | |
