---
artifact_id: container.<container-slug>
artifact_type: container
tier: system-specs
scope_kind: container
scope_id: <container-slug>
container_id: <CONT-####>
status: draft
version: 0
draft_revision: 1
approval_mode: human
# Replace with the smallest relevant approved upstream item IDs.
# Example:
# - CONT-0001
# - BC-0001
derives_from: []
---

# Container

`container` is the authoritative local inventory for one runtime boundary.

## Purpose And Runtime Boundary

<Describe what this container is for and where its runtime boundary sits.>
<!--
Exemplar:
This container owns the user-facing collaboration access workflow and keeps invitation lifecycle behavior inside one coherent runtime boundary.
-->

## Resident Bounded Contexts

| bounded_context_id | role |
| --- | --- |
<!--
Exemplar rows. Replace with project-specific residency.
| `BC-0001` | Collaboration access semantics live here because this container owns invitation lifecycle and membership activation behavior. |
-->

## Component Inventory

| id | folder | bounded_context_id | responsibility | derives_from |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific component ownership.
| `CMP-0001` | `invite-lifecycle` | `BC-0001` | Own invitation creation, resend, revoke, accept, and decline behavior. | `[AGG-0001, STORY-0001]` |
| `CMP-0002` | `membership-activation` | `BC-0001` | Activate access only after invitation acceptance satisfies invariants. | `[ENT-0001, STORY-0002]` |
-->

## Local Interfaces And Dependencies

| id | kind | source | target | notes |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific local edges.
| `EDGE-0002` | `interface` | `CMP-0001` | `CMP-0002` | Invitation acceptance is the only path that may trigger membership activation. |
-->

## Local NFR / Operational Constraints

| id | constraint | target | derives_from |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific local constraints.
| `CST-0004` | Invitation state transitions must remain durable across retries and restarts. | `CMP-0001` | `[NFR-0001, SNFR-0001]` |
-->
