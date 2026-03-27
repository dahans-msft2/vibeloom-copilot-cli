---
artifact_id: usm
artifact_type: usm
tier: product-specs
scope_kind: root
scope_id: root
status: draft
version: 0
draft_revision: 1
derives_from: []
---

# USM

`usm` is the delivery map. It organizes the product into epics, flows, stories, acceptance framing, and milestones.

Populate `derives_from` in frontmatter with the smallest relevant approved product-contract item IDs (e.g., FR-0001, NFR-0001, Q-0001).

## Epics

| id | epic | description | derives_from |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific mapping.
| `EPIC-0001` | Manage invitations | Owners and invitees need a complete invitation lifecycle inside the product. | `[FR-0001, FR-0002]` |
-->

## Flows

| id | flow | epic_id | description | derives_from |
| --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific journeys.
| `FLOW-0001` | Owner invites collaborator | `EPIC-0001` | Covers create, resend, and revoke actions from the owner point of view. | `[FR-0001]` |
| `FLOW-0002` | Invitee responds to invitation | `EPIC-0001` | Covers reviewing and accepting or declining a pending invite. | `[FR-0002]` |
-->

## Stories

| id | story | flow_id | actor | description | derives_from |
| --- | --- | --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific implementable stories.
| `STORY-0001` | Owner sends invitation | `FLOW-0001` | owner | As an owner, I can send an invitation so a collaborator can join through an explicit workflow. | `[FR-0001]` |
| `STORY-0002` | Invitee accepts invitation | `FLOW-0002` | invitee | As an invitee, I can accept a pending invitation so access is granted explicitly. | `[FR-0002]` |
-->

## Acceptance Framing

| id | story_id | framing | derives_from |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific acceptance framing.
| `ACC-0001` | `STORY-0001` | Invitation creation records the invitee, owner, and pending state in one durable action. | `[FR-0001, NFR-0001]` |
| `ACC-0002` | `STORY-0002` | Acceptance grants access only for a still-valid pending invitation. | `[FR-0002, NFR-0001]` |
-->

## Milestones

| id | milestone | included_story_ids | notes |
| --- | --- | --- | --- |
<!--
Exemplar rows. Replace with project-specific slices.
| `MS-0001` | Invitation lifecycle MVP | `[STORY-0001, STORY-0002]` | Delivers a complete happy-path invitation loop. |
-->
