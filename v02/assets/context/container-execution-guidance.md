---
artifact_id: guidance.container.<container-slug>.<assistant>
artifact_type: execution-guidance
tier: context
scope_kind: container
scope_id: <container-slug>
assistant: <assistant>
derives_from: []
---

# Container Execution Guidance

Populate `derives_from` in frontmatter with the governing approved contract item IDs for this scope (e.g., CONT-0001, CMP-0001, EDGE-0001). Replace `<assistant>` with the target assistant slug and `<container-slug>` with the container name.

## Scope And Ownership

- This scope owns one runtime boundary and the local coordination inside it.
- Stay inside this container unless the change crosses declared container or bounded-context boundaries.
- Treat `container.md` as the authoritative local inventory for component ownership.

## Your Context

Your context includes this execution guidance and the governing contract artifacts for this scope (`container` spec, `system`/`containers` spec, `defaults`). Use contract as authoritative reference; use this guidance for orientation and operational rules.

1. Start from the contract artifacts provided — they are the source of truth.
2. If a change requires artifacts outside your load set (e.g., other containers), escalate to the orchestrator.
3. Do not redistribute responsibilities between components without updating contract first.

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
