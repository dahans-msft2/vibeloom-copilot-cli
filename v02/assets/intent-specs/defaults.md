---
artifact_id: defaults
artifact_type: defaults
tier: intent-specs
scope_kind: root
scope_id: root
status: draft
version: 0
draft_revision: 1
derives_from: []
---

# Defaults

`defaults` is the minimal repo-wide constitution. It contains only always-on, globally binding defaults that downstream tiers and code must follow.

Do not put these here:
- product rationale
- local scope guidance
- optional tactics or pattern catalogs
- detailed runtime or generation mechanics

Put those in `intent`, execution guidance, or implementation instead.

## Repo Constitution

| id | rule | rationale |
| --- | --- | --- |
| `CST-0001` | Approved contract is the semantic source of truth; if context or code conflicts with approved contract, contract wins semantically. | Preserves contract-first governance and prevents downstream artifacts from becoming accidental truth. |
| `CST-0002` | Bounded contexts do not span containers. | Keeps semantic boundaries and runtime boundaries aligned. |
| `CST-0003` | Each component has exactly one semantic home and one runtime home. | Prevents smeared ownership and ambiguous technical boundaries. |
| `CST-0004` | Filesystem layout reflects declared ownership but does not define semantic truth. | Prevents folder shape from silently becoming architecture. |

## Technology Baseline

| id | choice | scope | notes |
| --- | --- | --- | --- |
| `CST-0005` | Standardize one primary implementation stack per repo or governed runtime slice. | `repo` or one governed runtime slice | Introduce another stack only through a narrower downstream contract that explicitly owns it. |
| `CST-0006` | Standardize one web UI stack per web-facing surface when the repo includes a UI. | web-facing scope | Record framework, styling system, and component library once and reuse them consistently. |
| `CST-0007` | Make persistence, messaging, and external platform baselines explicit when they are globally assumed. | `repo` | Prevent hidden infrastructure assumptions from leaking into downstream generation. |

## Quality Guardrails

| id | guardrail | expectation | notes |
| --- | --- | --- | --- |
| `CST-0008` | Behavior changes include executable verification at the narrowest useful scope. | Tests or checks are added or updated before the change is considered complete. | Broaden scope only when boundaries require it. |
| `CST-0009` | Invariants and boundary contracts are enforced explicitly in code. | Preconditions, postconditions, or invariant checks exist where the contract requires them. | Especially at component, container, and external boundaries. |
| `CST-0010` | Approved contract changes are reconciled downward before downstream work is treated as current. | Regenerate or realign affected context and code after approved upstream change. | Prevents stale downstream truth from lingering. |
| `CST-0011` | Semantic drift is corrected upstream first. | Change contract before patching context or code when the meaning is wrong. | Keeps contract-first governance intact. |
