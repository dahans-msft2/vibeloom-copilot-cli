---
artifact_id: system
artifact_type: system
tier: system-specs
scope_kind: root
scope_id: root
status: draft
version: 0
draft_revision: 1
approval_mode: human
derives_from: []
---

# System

`system` defines the whole system and its relationship to the outside world. Do not place deployment topology here.

Populate `derives_from` in frontmatter with the smallest relevant approved upstream item IDs (e.g., FR-0001, NFR-0001, BC-0001).

## System Purpose And Context

<Describe what the system is and where it sits in its broader environment.>
<!--
Exemplar:
The system governs shared-workspace access by coordinating invitation lifecycle, approval, membership activation, and operational visibility across the collaboration product.
-->

## External Actors And Systems

| id | kind | name | relationship | derives_from |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific context.
| `EXT-0001` | `actor` | Workspace owner | Initiates and manages invitations for collaborators. | `[FR-0001]` |
| `EXT-0002` | `external-system` | Notification delivery service | Delivers invitation and lifecycle notifications. | `[NFR-0001]` |
-->

## Trust Boundaries

| id | boundary | implication | derives_from |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific trust boundaries.
| `TB-0001` | Invitation approval boundary | Access cannot cross from pending to active without explicit approval or acceptance semantics. | `[NFR-0001]` |
-->

## System-Wide NFR Boundaries

| id | constraint | target | derives_from |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific system guardrails.
| `SNFR-0001` | Invitation lifecycle state changes are durable and auditable. | `100% of create, resend, accept, decline, revoke actions` | `[NFR-0001]` |
-->
