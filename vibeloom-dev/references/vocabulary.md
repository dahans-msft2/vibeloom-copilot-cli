# Reference: vocabulary

The decision vocabulary used in `review` and `reconcile`. Same verbs across both, with target-specific connotation.

## Decision verbs (per item in `reconcile`, per finding in `review`)

| Verb | Meaning in `reconcile` (per generated item) | Meaning in `review` (per eval finding) |
|---|---|---|
| `preserve_contract: variant-N` | Apply the chosen variant of the new generated content. Variant-A is the as-generated default; B/C are alternatives the agent offered just-in-time. | Apply the chosen fix variant for this finding. Variant-A is the recommended fix from the findings file; B/C are alternatives the agent offered in-loop. |
| `amend_contract` | The change indicates upstream needs amendment. Revert this section to baseline; user amends upstream (intent / manifesto / methodology / implementation) then re-runs `generate <target>`. | The finding points at an upstream defect, not a downstream symptom. Don't fix the downstream artifact; flag for upstream amendment. |
| `preserve_existing` | Reject the new generation; keep the prior content. (Reverts to git HEAD for this section.) | Mark the finding as "not actually a problem" or "the proposed fix is worse than the current state". Reject. |
| `user_defined` | User supplies a custom patch (inline or pre-edited). Apply or skip-apply if user did it themselves. | User supplies a custom fix (inline or pre-edited). Apply / skip-apply. |
| `defer` | Skip this item for now. No state persisted; the item remains as-generated in the working tree. | Skip this finding for now. Item remains in findings file as "deferred" verbally; no persistent decision file in v1. |

## Variant generation rule

- **Default: 1 variant** (just the as-generated / as-proposed content). The agent must justify producing 2+ variants.
- 2-3 variants only when there is **genuine ambiguity** in how to handle the item — e.g., a methodology section could legitimately be organized two different ways, both equally consistent with intent.
- Variants live ONLY in LLM context during the interactive loop. They are NEVER written to disk as sidecar files. (Earlier design considered sidecar files; rejected as too heavyweight.)

## Recommended-option rule

- Per item / finding, exactly ONE option is marked `recommended` with one-paragraph rationale.
- The recommendation may be any `preserve_contract: variant-*` OR `amend_contract`.
- Recommendation is NEVER `preserve_existing`, `user_defined`, or `defer` — those are user-initiated exceptions, not agent suggestions.

## Vocabulary parity with vibeloom proper

These verbs are vibeloom's own reconcile vocabulary, dogfooded into dev-skill. The future evolution (variants in vibeloom's own review/reconcile) will be rolled out to vibeloom proper post-v04. dev-skill is the landing zone.

## Anti-patterns

- **"Accept all" / "Accept variant-A for everything"** without confirmation — that's batch auto-apply. NOT in v1. User can request it explicitly but the default is per-item.
- **Recommending `preserve_existing`** — that's recommending "do nothing", which is what `defer` is for. If the change is actively harmful, the proper recommendation is `amend_contract` (the upstream is wrong) or `user_defined` (the right fix is different).
- **Force-fitting `user_defined` when a variant would do** — if the user's hand-edit is one of N reasonable approaches, surface it as `variant-B` next time the same item comes up, not as user_defined. (Implication: the agent can learn from user-defined patterns over a session but doesn't persist them.)
