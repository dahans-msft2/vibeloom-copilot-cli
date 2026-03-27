---
artifact_id: intent
artifact_type: intent
tier: intent-specs
scope_kind: root
scope_id: root
status: draft
version: 0
draft_revision: 1
derives_from: []
---

# Intent

`intent` stays prose-first. Use coarse IDs only for structured capabilities or constraints that must participate in derivation.

### Guidance

- **Capabilities** (CAP) are user-facing, observable outcomes the system should deliver. Focus on what the user needs and why, not how to build it.
- **Wishes** (WISH) are softer preferences that clarify priorities but do not block delivery if omitted. They inform downstream trade-offs.
- **Constraints** (CST) are hard, non-negotiable requirements. Violating a constraint blocks delivery. Constraints may be product-level (e.g., "explicit approval before access") or technical (e.g., "must run on ARM64").
- Keep items coarse. If a capability naturally subdivides into multiple requirements, that decomposition belongs in product-specs after upgrade to pm/dev/expert.
- Items that are repo-wide and always-on belong in `defaults`, not `intent`.

## Vision

<Free-form prose description of the system: purpose, users, value proposition, and any high-level context that does not fit into structured tables below.>
<!--
Exemplar:
A lightweight workspace collaboration tool that lets owners invite trusted collaborators into a shared environment. The product emphasizes explicit approval, auditability, and a calm user experience over complex role hierarchies.
-->

## Functionality

| id | statement | notes |
| --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific intent.
| `CAP-0001` | Workspace owners can invite collaborators into a shared workspace. | Invitations require explicit acceptance before access is granted. |
| `CAP-0002` | Invited users can review and act on pending invitations inside the product. | Support accept and decline flows. |
-->

## Miscellaneous

| id | type | statement | notes |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific intent.
| `WISH-0001` | `wish` | Prefer a calm, low-ceremony approval flow for invitation management. | Keep the UX direct and easy to explain. |
| `CST-0001` | `constraint` | Preserve explicit approval before any shared access is granted. | This drives downstream security and lifecycle rules. |
-->

## Product Summary

<Narrative prose summarizing the product dimensions that will seed future product-specs on upgrade. Cover three areas:>

### Key Requirements

<What must the product do? Describe the core functional requirements and any critical non-functional requirements (performance, security, availability) in prose. Do not use IDs — keep it narrative.>
<!--
Exemplar:
The system must support workspace creation, invitation lifecycle (create, accept, decline, revoke), and basic access control. Invitations must be durable — surviving restarts and retries — and auditable. Response time for invitation operations should stay under 500ms at p95.
-->

### Core User Workflows

<How do users interact with the product? Describe the primary workflows or journeys in prose. Focus on the happy path and key decision points.>
<!--
Exemplar:
A workspace owner creates a workspace, then invites collaborators by email. Each collaborator receives a notification, reviews the invitation, and either accepts (gaining access) or declines. The owner can see pending, accepted, and declined invitations on a dashboard. Revocation is available at any time before or after acceptance.
-->

### Domain Concepts

<What are the key domain terms and how do they relate? Describe the core entities, their relationships, and any important invariants in prose.>
<!--
Exemplar:
The core domain centers on Workspace, Invitation, and Collaborator. A Workspace owns zero or more Invitations. An Invitation transitions through a lifecycle: pending → accepted | declined | revoked. A Collaborator is created when an Invitation is accepted. Key invariant: access is never granted without an accepted Invitation.
-->
