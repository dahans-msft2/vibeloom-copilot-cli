---
artifact_id: containers
artifact_type: containers
tier: system-specs
scope_kind: root
scope_id: root
status: draft
version: 0
draft_revision: 1
approval_mode: human
# Replace with the smallest relevant approved upstream item IDs.
# Example:
# - BC-0001
# - NFR-0001
# - SNFR-0001
derives_from: []
---

# Containers

`containers` owns the global runtime topology of the system.

## Container Inventory

| id | container_slug | responsibility | runtime | deployment_unit | derives_from |
| --- | --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific topology.
| `CONT-0001` | `app` | Owns product-facing invitation workflow and collaboration access behavior. | `web app` | `frontend + API deployable` | `[BC-0001]` |
| `CONT-0002` | `notifications` | Delivers invitation lifecycle notifications and asynchronous follow-up. | `worker` | `background worker` | `[NFR-0001]` |
-->

## Responsibilities

| container_id | statement |
| --- | --- |
<!--
Exemplar rows. Replace with project-specific responsibilities.
| `CONT-0001` | Keeps invitation approval and membership activation behavior inside the user-facing workflow boundary. |
| `CONT-0002` | Handles delivery concerns only; it does not become the source of invitation truth. |
-->

## Communication Paths

| id | from_container_id | to_container_or_external | protocol | purpose |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific communication paths.
| `EDGE-0001` | `CONT-0001` | `CONT-0002` | `event` | Publish invitation lifecycle events for delivery and audit fan-out. |
| `EDGE-0002` | `CONT-0001` | Identity provider | `HTTP` | Resolve invitee identity before activation. |
-->

## Deployment / Runtime Choices

| target | choice | notes |
| --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific runtime choices.
| `CONT-0001` | Keep the primary workflow container deployable as one coherent runtime slice until scaling pressure proves otherwise. | Preserve clear ownership while the domain is still stabilizing. |
| `CONT-0002` | Keep asynchronous delivery isolated from approval semantics. | Delivery failures should not redefine core invitation truth. |
-->

## Cross-Container Constraints

| id | constraint | affects | derives_from |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific cross-container constraints.
| `CST-0003` | Asynchronous delivery must not become the source of truth for invitation state. | `CONT-0001`, `CONT-0002` | `[NFR-0001, SNFR-0001]` |
-->
