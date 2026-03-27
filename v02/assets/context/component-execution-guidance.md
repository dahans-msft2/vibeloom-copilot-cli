---
artifact_id: guidance.component.<container-slug>.<component-slug>.<assistant>
artifact_type: execution-guidance
tier: context
scope_kind: component
scope_id: <container-slug>.<component-slug>
assistant: <assistant>
derives_from: []
---

# Component Execution Guidance

Populate `derives_from` in frontmatter with the governing approved contract item IDs for this scope (e.g., CMP-0001, BEH-0001, DEP-0001). Replace `<assistant>` with the target assistant slug and `<container-slug>.<component-slug>` with the component path.

## Scope And Ownership

- This scope owns only the paths, interfaces, and behavior explicitly assigned to the component.
- Prefer changes that stay entirely inside owned paths and owned interfaces.
- If work requires behavior owned by another component, escalate rather than smearing responsibilities.

## Your Context

Your context includes this execution guidance and the governing contract artifacts for this scope (`component` spec, `container` spec, `defaults`). Use contract as authoritative reference; use this guidance for orientation and operational rules.

1. Start from the contract artifacts provided — they are the source of truth.
2. If a change requires artifacts outside your load set (e.g., other components or containers), escalate to the orchestrator.
3. Do not edit paths or interfaces not owned by this component without explicit contract changes.

## Do-Not-Touch Boundaries

- Do not edit paths or interfaces not owned by this component without explicit contract changes.
- Do not bury cross-component behavior in local helper code.
- Do not correct semantic drift only in code if the contract is wrong or incomplete.

## Common Commands / Checks

- Run the narrowest useful component-level tests and boundary checks first.
- Verify owned interfaces and local behavior before broadening to container-wide checks.
- Re-run dependency-sensitive checks when changing interfaces, invariants, or behavior contracts.

## Local Caveats

- One component has one semantic home and one runtime home.
- Prefer upstream contract edits over context edits when local guidance is semantically wrong.
- Keep behavior, ownership, and tests aligned with declared component boundaries.
