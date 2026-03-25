---
artifact_id: guidance.container.<container-slug>.claude
artifact_type: execution-guidance
tier: context
scope_kind: container
scope_id: <container-slug>
assistant: claude
# Replace with the governing approved contract item IDs for this scope.
# Example:
# - CONT-0001
# - CMP-0001
# - EDGE-0001
derives_from: []
---

# Container Execution Guidance For Claude

## Scope And Ownership

- This scope owns one runtime boundary and the local coordination inside it.
- Stay inside this container unless the change crosses declared container or bounded-context boundaries.
- Treat `container.md` as the authoritative local inventory for component ownership.

## Load-First Context

1. Load the relevant root contract plus this `container` contract.
2. Load only the resident bounded contexts, component inventory entries, and local edges touched by the change.
3. Load component guidance only after the governing component is identified.
4. Escalate to root when the change affects multiple containers or cross-container constraints.

## Do-Not-Touch Boundaries

- Do not redistribute responsibilities between components without updating contract first.
- Do not change neighboring containers from here without explicit upstream justification.
- Do not use filesystem proximity as proof of ownership.

## Common Commands / Checks

- Run the narrowest container-local validation first.
- Prefer component-level checks before container-wide checks when one component owns the change.
- Re-run boundary and dependency checks when local interfaces or edges change.

## Local Caveats

- Bounded contexts do not span containers.
- Prefer correcting upstream contract over patching context artifacts when generation is semantically wrong.
- Escalate when local work would change shared runtime or deployment assumptions.
