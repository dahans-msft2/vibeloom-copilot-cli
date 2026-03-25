---
artifact_id: BDD-0001
artifact_type: bdd
tier: context
scope_kind: root
scope_id: root
# Replace with the approved upstream item IDs that produced this scenario set.
# Example:
# - STORY-0001
# - ACC-0001
derives_from: []
---

# Behavioral Scenarios

`bdd` contains generated, non-executable Gherkin scenarios derived from approved contract.

This template produces one behavior artifact per file. Keep generated BDD artifacts under `/context/bdd/`, for example `BDD-0001-<behavior-slug>.md`.

## Feature / Capability

- **id:** `BDD-0001`
- **title:** <Feature or capability title>
- **derives_from:** `[<short-item-id>, <short-item-id>]`
<!--
Exemplar:
- **title:** Invitation approval
- **derives_from:** `[FR-0001, STORY-0001]`
-->

## Scenarios

### `SCN-0001`

- **derives_from:** `[<short-item-id>, <short-item-id>]`
<!--
Exemplar:
- **derives_from:** `[ACC-0001, INV-0001]`
-->

```gherkin
Scenario: <Scenario title>
  Given <starting condition>
  And <additional context>
  When <action>
  Then <expected outcome>
  And <additional observable outcome>
```
<!--
Exemplar:
Scenario: Owner revokes a pending invitation
  Given a workspace owner has sent an invitation
  And the invitation is still pending
  When the owner revokes the invitation
  Then the invitation can no longer be accepted
  And no workspace access is granted
-->
