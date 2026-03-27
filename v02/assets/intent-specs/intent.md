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
- Keep items coarse. If a capability naturally subdivides into multiple requirements, that decomposition belongs in `prd`, not here.
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
