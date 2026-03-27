---
artifact_id: guidance.root.<assistant>
artifact_type: execution-guidance
tier: context
scope_kind: root
scope_id: root
assistant: <assistant>
derives_from: []
---

# Root Execution Guidance

Populate `derives_from` in frontmatter with the governing approved contract item IDs for this scope (e.g., CAP-0001, FR-0001, CONT-0001). Replace `<assistant>` in frontmatter with the target assistant slug (e.g., `claude`, `codex`).

## Scope And Ownership

- Root scope owns repo-wide contract, global defaults, and cross-container coordination.
- Prefer the narrowest valid container or component scope whenever the change can stay there.
- Treat execution guidance as operational help; contract remains semantic truth.

## Your Context

Your context includes this execution guidance and the governing contract artifacts for this scope (`system`, `containers`, `defaults`). Use contract as authoritative reference; use this guidance for orientation and operational rules.

1. Start from the contract artifacts provided — they are the source of truth.
2. If a change requires artifacts outside your load set, escalate to the orchestrator.
3. Do not infer product semantics from code when approved contract already exists.

## Do-Not-Touch Boundaries

- Do not edit unrelated containers or components from root scope just because they are nearby.
- Do not patch context artifacts directly when the real fix belongs upstream in contract.
- Do not infer new product semantics from code when approved contract already exists.

## Common Commands / Checks

- Run the narrowest useful validation first, then broaden only if the change crosses boundaries.
- Prefer scope-local tests, lint, type, or schema checks before repo-wide checks.
- Re-evaluate stale downstream artifacts after approved contract changes.

## Local Caveats

- Approval behavior follows the current mode; do not assume every run stops at each tier.
- Prefer upstream contract edits over direct context edits when semantics are wrong.
- Keep root-scope work small and push ownership back down whenever possible.
