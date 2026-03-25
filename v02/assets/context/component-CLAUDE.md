---
artifact_id: guidance.component.<container-slug>.<component-slug>.claude
artifact_type: execution-guidance
tier: context
scope_kind: component
scope_id: <container-slug>.<component-slug>
assistant: claude
# Replace with the governing approved contract item IDs for this scope.
# Example:
# - CMP-0001
# - BEH-0001
# - DEP-0001
derives_from: []
---

# Component Execution Guidance For Claude

## Scope And Ownership

- This scope owns only the paths, interfaces, and behavior explicitly assigned to the component.
- Prefer changes that stay entirely inside owned paths and owned interfaces.
- If work requires behavior owned by another component, escalate rather than smearing responsibilities.

## Load-First Context

1. Load the governing component contract plus its owning container contract.
2. Load only the upstream stories, invariants, relationships, or system constraints that materially govern this component.
3. Load local execution guidance after contract if implementation detail is needed.
4. Escalate if the change crosses component, container, or bounded-context boundaries.

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
