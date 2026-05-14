# Reference: interactive-loop

The just-in-time variant pattern used in `review` and `reconcile`.

## Core principle

When walking findings (review) or generated changes (reconcile), the agent presents 1-3 options per item INLINE in the conversation, the user picks one, the agent applies. Options live ONLY in LLM context — never persisted as sidecar files on disk.

## Why just-in-time?

Earlier design considered pre-computing variants during `generate` and writing them to sidecar files (`reports/variants/methodology-section-X-variant-b.md`). Rejected because:

- **Cost.** Generating N variants per item ahead of time is N times the LLM work for items that don't actually have ambiguity.
- **Disk clutter.** Sidecar files outlive their usefulness; cleanup is friction.
- **Decision fatigue if always shown.** When most items have only one reasonable answer, padding to 2-3 wastes user attention.

Just-in-time variants generated DURING the interactive loop are cheaper and only paid for when actually needed.

## Variant generation rule

Per item in `reconcile` / per finding in `review`:

1. **Default: 1 variant** (the as-generated content / the recommended fix from the findings file).
2. **2-3 variants only when there is genuine ambiguity.** Examples:
   - A methodology section that could legitimately be organized two different ways (by axis vs by mode) — both consistent with intent.
   - A finding fix that could be (a) sharpen the existing wording, OR (b) restructure the surrounding section so the wording isn't needed — both valid.
3. Agent must be able to **articulate the difference** between variants. If the agent can't say "B differs from A in that..." with a clear distinction, B is just A with cosmetic changes — drop B and present A only.

## Option set per item

Always available:
- **`preserve_contract: variant-a`** — the as-generated (reconcile) or recommended fix (review).
- **`amend_contract`** — this issue points upstream; revert and amend upstream.
- **`preserve_existing`** — reject; keep prior content.
- **`user_defined`** — user supplies custom.
- **`defer`** — skip this item for now.

Conditionally available (only when agent generated alternatives in-loop):
- **`preserve_contract: variant-b`**
- **`preserve_contract: variant-c`**

Total options per item: 4 (default, no multi-variant) to 6 (max).

## Presentation format

In the interactive loop, present each item like:

```
─── Item 3 of 12: methodology.md § 4.2 (Modes) ───

[change diff or finding details here]

Why it matters: [from eval finding, or from agent's read of the change]

Options:
  [A] preserve_contract: variant-a (RECOMMENDED)
      [variant content / fix patch]
      Rationale: [why this is recommended]

  [B] preserve_contract: variant-b
      [variant content / fix patch]
      Differs from A in: [concrete difference]

  [C] amend_contract
      Indicates: intent.md section X needs amendment.
      Action: revert this section; user amends intent; re-run `generate methodology`.

  [D] preserve_existing  (revert this section to HEAD)
  [E] user_defined       (supply your own patch)
  [F] defer              (skip; no decision recorded)

Your choice [A/B/C/D/E/F]?
```

The user types the letter (or says the word, or describes a sixth option which becomes [E] user_defined).

## Cost-control: batch the trivial

For items where the change is mechanical (whitespace, link reformatting, obvious typo fixes), the agent can offer a batch:

> "Items 4-9 are all link-format normalizations (same pattern). Recommend `preserve_contract: variant-a` for all. Accept batch? (y/n/walk-individually)"

If user says "y", apply all 6 with one disposition recorded. If "n" or "walk-individually", fall back to per-item walk.

## Cost-control: skip the trivial in the count

If the agent reads the change set and a chunk is "23 sections unchanged" (genuinely no diff), surface as "23 unchanged sections — preserved." Don't walk them.

## Drift detection mid-loop

If, between `generate` and `reconcile`, the user manually edited the file in place (bypassing reconcile), the working tree has both generate's changes AND post-generate manual edits. Reconcile should:

1. Detect the discrepancy at start: compare current file vs git HEAD; identify regions that don't look like generate's output.
2. Surface to the user: "Working tree has edits beyond what generate produced. Walk all changes, or only generate's?". Default: walk all (treat manual edits as items the user already pre-applied — they're equivalent to `user_defined`).

## What's NOT in v1

- **Persistent decision log** — per-finding/per-item disposition is verbal in the response, not written to a `decisions.md`. Future addition possible.
- **Cross-session resumption** — if the user pauses mid-walk and starts a new session, the loop starts over from item 1 (with no recollection of prior dispositions). The user can ask the agent to "skip to item 7" manually.
- **Cross-agent variants** — only the current agent's variants are presented. The peer's findings/generations are not consulted during reconcile. (Use `feedback` for that.)
