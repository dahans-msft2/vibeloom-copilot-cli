---
artifact_id: dm
artifact_type: dm
tier: product-specs
scope_kind: root
scope_id: root
status: draft
version: 0
draft_revision: 1
derives_from: []
---

# Domain Model

`dm` is the semantic source for technical boundary derivation.

Populate `derives_from` in frontmatter with the smallest relevant approved `prd` and `usm` item IDs (e.g., FR-0001, STORY-0001, ACC-0001).

## Ubiquitous Language

| id | term | definition | notes |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific terms.
| `TERM-0001` | Invitation | A pending request for access initiated by an owner and acted on by an invitee. | Do not confuse with an already-active membership. |
| `TERM-0002` | Membership | An active access relationship between a user and a workspace. | Membership starts only after the invite lifecycle completes successfully. |
-->

## Bounded Contexts

| id | bounded_context | purpose | derives_from |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific boundaries.
| `BC-0001` | Collaboration access | Owns invitation lifecycle and membership activation semantics. | `[FR-0001, FR-0002]` |
-->

## Aggregates / Entities / Value Objects

| id | kind | bounded_context_id | name | responsibility | derives_from |
| --- | --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific structures.
| `AGG-0001` | `aggregate` | `BC-0001` | Invitation | Owns invitation state transitions and approval rules. | `[STORY-0001, STORY-0002]` |
| `ENT-0001` | `entity` | `BC-0001` | Membership | Represents active access granted after successful invitation completion. | `[STORY-0002]` |
| `VO-0001` | `value-object` | `BC-0001` | InvitationStatus | Encodes pending, accepted, declined, revoked, and expired lifecycle states. | `[ACC-0001, ACC-0002]` |
-->

## Invariants / Business Rules

| id | bounded_context_id | rule | derives_from |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific invariants.
| `INV-0001` | `BC-0001` | Only a pending invitation can be accepted. | `[FR-0002, STORY-0002]` |
| `INV-0002` | `BC-0001` | One invitation cannot activate more than one membership. | `[FR-0002]` |
-->

## Relationships / Integration Touchpoints

| id | from_item | to_item | relationship | notes |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific relationships.
| `REL-0001` | `AGG-0001` | `ENT-0001` | Invitation activation creates membership under the collaboration access boundary. | Maintain a clear state transition boundary between pending and active access. |
-->
