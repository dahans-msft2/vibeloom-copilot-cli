---
name: vibeloom-dev
description: Develops vibeloom itself. Adversarial consistency checks and generation across intent / canon / skill / site for any vibeloom version. Use to bring up a new version, eval/review canon for drift, generate downstream artifacts from upstream specs, or run cross-agent reviews across multiple agents.
---

# vibeloom-dev

The dev skill for vibeloom. Dogfoods vibeloom's own intent/product/system/code split — eval/review/generate/reconcile — to develop vibeloom's canon, skill, and site.

**Vibe-mode for v1.** No persistent state, no derivation graph, no formal staleness tracking. `eval` is the LLM-driven detector. `generate` assumes upstream is consistent (it does NOT auto-invoke eval — that's on you).

## Usage

```
vibeloom-dev <command> [<args>] [--version vNN] [--from vNN] [--from-scratch]
```

| Command | Positional args |
|---|---|
| `init` | (none) |
| `eval` | `[<target>]` (default: `canon`) |
| `review` | `[<target>]` (default: `canon`) |
| `generate` | `<target>` (required: `methodology` \| `implementation` \| `skill` \| `site`) |
| `reconcile` | `[<target>]` (default: `canon`) |
| `feedback` | `<peer> <target>` |

`<target>` is one of: `intent`, `manifesto`, `methodology`, `implementation`, `skill`, `site`, `canon` (shortcut), `all` (shortcut). See `references/targets.md` for which commands accept which targets.

## When to use this skill

Invoke on `$vibeloom-dev`, `/vibeloom-dev`, or when the user asks to:
- bring up a new vibeloom version (`init`)
- check canon / skill / site for drift (`eval`)
- walk findings interactively (`review`)
- regenerate methodology / implementation / skill / site from upstream (`generate <target>`)
- walk generate's output interactively (`reconcile`)
- critique a peer agent's eval (`feedback <peer> <target>`)

## Authoritative sources

Always consult these:

- **[/file-layout.md](../file-layout.md)** — repo file layout. Defines `vNN/` shape (canon/, site/, skill/, examples/, dist/, intent.md), where everything lives, what's gitignored. Authoritative for any "where does X go" question.
- **The current version's canon** (`vNN/canon/codæ-manifesto.html`, `vNN/canon/vibeloom-methodology.md`, `vNN/canon/vibeloom-implementation.md`, `vNN/canon/vibeloom-templates.md`) — the version-specific source of truth. The skill OPERATES on these; it doesn't define them.
- **The current version's intent** (`vNN/intent.md`) — sibling-input to manifesto. Both seed methodology.

If this skill file conflicts with the canon of the version being operated on, the canon wins.

## Runtime references (load on demand)

- **[references/vocabulary.md](references/vocabulary.md)** — decision vocabulary: `preserve_contract` (with variants), `amend_contract`, `preserve_existing`, `user_defined`, `defer`. Plus eval-finding vocabulary: Accept / Edit / Defer / Reject.
- **[references/targets.md](references/targets.md)** — what each target is (intent, manifesto, methodology, implementation, skill, site, canon, all) and which commands accept it.
- **[references/layering.md](references/layering.md)** — the dependency chain: `(intent ↔ manifesto) → methodology → implementation+templates → skill (incl. engine)`. Plus the site as a marketing-register sibling that must not contradict canon.
- **[references/multi-agent.md](references/multi-agent.md)** — N-agent coordination via shared filesystem; each agent self-identifies with a stable lowercase name; per-agent filename conventions; the explicit `feedback` flow.
- **[references/interactive-loop.md](references/interactive-loop.md)** — the just-in-time variant pattern for `review` and `reconcile`. Variants live in LLM context only; never persisted as sidecar files.
- **[references/eval-passes-canon.md](references/eval-passes-canon.md)** — adversarial passes specific to canon (intent ↔ manifesto consistency, authority/separation between methodology and implementation, etc.).
- **[references/eval-passes-skill.md](references/eval-passes-skill.md)** — adversarial passes specific to skill (canon alignment, coverage/load map, agent efficiency, helper prompt quality).
- **[references/eval-passes-site.md](references/eval-passes-site.md)** — adversarial passes specific to site (canon alignment, messaging quality, public web integrity).
- **[references/generate-spec-methodology.md](references/generate-spec-methodology.md)** — target-specific procedure for generating methodology from intent + manifesto.
- **[references/generate-spec-implementation.md](references/generate-spec-implementation.md)** — target-specific procedure for generating implementation + templates from methodology.
- **[references/generate-spec-skill.md](references/generate-spec-skill.md)** — target-specific procedure for generating the skill bundle (extract + optional engine regen).
- **[references/generate-spec-site.md](references/generate-spec-site.md)** — target-specific procedure for generating site HTML pages.

## Commands and routing

| Command | First load | Task template |
|---|---|---|
| `init [--from vNN] [--version vNN] [--from-scratch]` | `targets.md`, `layering.md`, `/file-layout.md` | `tasks/init.md` |
| `eval [<target>]` | `targets.md`, `multi-agent.md`, `eval-passes-<target>.md` (or all three if target=canon/all) | `tasks/eval.md` |
| `review [<target>]` | `vocabulary.md`, `interactive-loop.md` | `tasks/review.md` |
| `generate <target>` | `layering.md`, `targets.md`, `generate-spec-<target>.md` | `tasks/generate.md` |
| `reconcile [<target>]` | `vocabulary.md`, `interactive-loop.md` | `tasks/reconcile.md` |
| `feedback <peer> <target>` | `multi-agent.md`, `vocabulary.md` | `tasks/feedback.md` |

**Default `target` for `eval` / `review` / `reconcile` is `canon`** when omitted.

## Targets

| Keyword | Refers to | Files involved |
|---|---|---|
| `intent` | The user's seed/refined intent for this version | `vNN/intent.md` |
| `manifesto` | The philosophical layer | `vNN/canon/codæ-manifesto.html` |
| `methodology` | The WHAT layer | `vNN/canon/vibeloom-methodology.md` |
| `implementation` | The HOW layer (includes templates) | `vNN/canon/vibeloom-implementation.md` + `vNN/canon/vibeloom-templates.md` |
| `skill` | The skill bundle (includes engine) | `vNN/skill/**` |
| `site` | The marketing site for this version | `vNN/site/**` |
| `canon` | Shorthand | intent + manifesto + methodology + implementation |
| `all` | Everything | canon + skill + site |

`generate` accepts only: `methodology`, `implementation`, `skill`, `site` (intent and manifesto are hand-authored).

## Version selection

A version `vNN` is **mutable** iff ALL of the following hold:
- It exists as a directory at the repo root.
- It is NOT in the frozen legacy set: `v01`, `v02`, `v03` (these use the legacy layout and are read-only; see `/file-layout.md §1`).
- It is NOT current production (where production = target of root `site/public/` symlink; if root `site/public/` is a real directory, no version is current production).

**Defaults:**

- For `eval`, `review`, `generate`, `reconcile`, `feedback`:
  - Default version = the **latest mutable** vNN (highest-numbered).
  - If no mutable version exists, **refuse**: `"No mutable version found. v01-v03 are frozen (legacy layout); v04+ would be mutable but doesn't exist yet. Run `vibeloom-dev init` to bootstrap v04 from v03."`
- For `init`:
  - Default `--from` = the highest-numbered version directory (frozen or not).
  - Default `--version` = `<--from> + 1` (e.g., `--from v03` → `--version v04`).
  - With no flags, `vibeloom-dev init` today resolves to `--from v03 --version v04` and starts the v03→v04 layout migration.

**Override:** `--version vNN` for any command. Refuses if you target a frozen version for a write operation (`generate`, `reconcile`, `init`).

No persistent "current working version" file. If you have multiple in-progress versions, pass `--version` explicitly.

## Agent identity

Each agent **self-identifies with a stable, lowercase, hyphenated name** (e.g., `claude`, `codex`, `cursor`, `gemini`). The name is the agent's identity in this repo across all sessions.

Resolution order:
1. **Env variable** `VIBELOOM_AGENT_NAME` — if set, use it.
2. **Hardcoded in the skill install** — if pre-configured by the user.
3. **Ask the user** at first invocation in this repo. Persist the answer for the session and suggest setting `VIBELOOM_AGENT_NAME` for permanence.

No detection signatures. No hardcoded list of supported agents. The name is what appears in `reports/` filenames (`eval-<target>-<name>.md`, etc.). See `references/multi-agent.md` for the full contract.

## Output locations

- **`eval` / `feedback` outputs:** `reports/<filename>.md` at repo root (FLAT, gitignored, ephemeral). See `file-layout.md §5` for the filename pattern.
- **`generate` outputs:** written IN PLACE in `vNN/` (canon/, site/public/, skill/, etc.). Git is the safety net — commit (or stash) before `generate` so `reconcile` has a stable baseline.
- **`reconcile` / `review` outputs:** modify files in place based on the user's per-item decisions. Same git-safety convention.
- **`init` outputs:** writes the new `vNN/` directory tree.

## Guardrails

- **Propose only, never autonomous edits.** Every change to canon / skill / site / examples / intent requires explicit user Accept (per item, in the interactive loop). No batch auto-apply.
- **Vibe-mode honesty.** `generate` assumes upstream is consistent. It does NOT invoke `eval` first. The user is the orchestrator — run `eval` before `generate` when you've made upstream changes.
- **Layering is canonical.** Never generate upstream from downstream. The chain is `(intent ↔ manifesto) → methodology → implementation+templates → skill (incl. engine)`. Site is sibling to skill — derived from methodology + implementation, must not contradict canon.
- **Cross-agent collaboration is filesystem-only.** All agents run locally and write to shared `reports/` files. There is no API call between agents. The handoff is manual: "now run this in another agent".
- **No own state.** vibeloom-dev writes only to `reports/` (gitignored) and to the target `vNN/` artifacts (with user approval). No `.vibeloom-dev/` cache, no hidden state file.
- **Frozen versions are read-only.** v01/v02/v03 (legacy layout) and any version that is current production must not be modified by vibeloom-dev. If asked, refuse and explain.
- **Site is marketing register.** `generate site` produces full HTML files (not content-only drafts) but they may be abbreviated relative to canon. `eval site` checks that site does not CONTRADICT canon, not that it covers every canon concept.
- **No invented operations.** The valid command set is the table above. Don't infer `approve`, `status`, `release`, `diff`, `import`, `synthesize` — those are explicitly out of v1.

## Response shape

Keep responses tight:

1. **Scope** — what version and target the operation touched.
2. **Decision** — what the skill did, or what it's asking the user to decide.
3. **Affected** — files, sections, item IDs changed or surfaced.
4. **Next** — the suggested next command (e.g., "Run `vibeloom-dev review canon` to walk the findings", or "Now run `vibeloom-dev eval canon` in another agent and then `feedback <that-agent> canon` here").

## Getting started

**First time, when no mutable version exists yet (current state — only frozen v01-v03 in the repo):**

```
vibeloom-dev init
```

This resolves `--from v03 --version v04` by default, migrates v03's legacy layout to v04's new layout, and interviews you to seed `v04/intent.md`. Once v04 exists, `eval` and the other commands become usable.

**Once a mutable version exists** (e.g., v04 in progress):

```
vibeloom-dev eval canon
```

Runs an adversarial consistency check on the latest mutable version's canon (intent + manifesto + methodology + implementation). Findings land in `reports/eval-canon-<your-agent>.md`. Then `vibeloom-dev review canon` walks them.

**Bumping to the next version** (e.g., v05 from v04):

```
vibeloom-dev init
```

Same command — it resolves `--from v04 --version v05` automatically once v04 is the highest existing version. Copies v04 → v05 with version refs updated, then interviews you to refactor `intent.md`.
