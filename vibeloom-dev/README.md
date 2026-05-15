# vibeloom-dev

A multi-agent skill that helps develop vibeloom itself.

> This README is for repo browsers / humans. The canonical skill manifest (loaded by Claude/Codex/other skill runtimes) is [`SKILL.md`](SKILL.md); the operational prompts live in `tasks/` and `references/`.

## What it does

Dogfoods vibeloom's own intent/product/system/code split — eval/review/generate/reconcile — to develop vibeloom's canon, skill, and site. Vibe-mode for v1: no persistent state, no derivation graph, no formal staleness tracking. Eval is the LLM-driven detector; generate is a full rewrite from current upstream.

Designed for the workflow where the user runs two (or more) agents in separate environments — e.g., Claude Code in one terminal and Codex in another — and wants each agent to independently eval the same canon and critique the others' findings. The repo filesystem is the shared substrate; agents self-identify by name (see [references/multi-agent.md](references/multi-agent.md)).

**vibeloom-dev does not yet have its own intent.md or canon.** It's vibe-mode for v1 — dev-skill helps build/eval vibeloom but isn't itself dogfooded against vibeloom-dev. Self-application is future work.

## Commands (quick reference)

```
vibeloom-dev init [--from vNN] [--version vNN] [--from-scratch]
vibeloom-dev eval [<target>]                          # default target: canon
vibeloom-dev review [<target>]                        # walks findings from latest eval
vibeloom-dev generate <methodology|implementation|skill|site>
vibeloom-dev reconcile [<target>]                     # walks recent generate output
vibeloom-dev feedback <peer> <target>           # e.g. peer = "claude", "codex", "cursor"
```

Common flags: `--version vNN` (default: latest mutable), `--from vNN` (init source).

## Targets

`intent`, `manifesto`, `methodology`, `implementation`, `skill`, `site`, plus shortcuts `canon` (= intent + manifesto + methodology + implementation) and `all` (= canon + skill + site).

`generate` accepts only: `methodology`, `implementation`, `skill`, `site`. intent and manifesto are hand-authored.

## Layout

```
vibeloom-dev/
├── SKILL.md              # manifest + command routing
├── README.md             # this file
├── tasks/                # one prompt per operation
├── references/           # load-on-demand reference docs
└── scripts/              # extract-templates.py + site validators
```

See [SKILL.md](SKILL.md) for the full command/routing/guardrails reference. See [/file-layout.md](../file-layout.md) for the canonical repo file layout this skill operates against.

## Multi-agent flow

See [references/multi-agent.md](references/multi-agent.md). Short version (using `claude` and `codex` as example agent names — substitute whatever names your agents self-identify with):

1. `vibeloom-dev eval canon` in agent A → `reports/eval-canon-claude.md`
2. `vibeloom-dev eval canon` in agent B → `reports/eval-canon-codex.md`
3. `vibeloom-dev feedback codex canon` in agent A → `reports/feedback-canon-claude-on-codex.md`
4. `vibeloom-dev feedback claude canon` in agent B → `reports/feedback-canon-codex-on-claude.md`
5. (Optionally repeat with a third agent for a third perspective.)
6. User reads everything, decides.

All output to gitignored `reports/` at repo root. Flat, ephemeral, overwritten on rerun.

## Constraints

- **Propose only.** Never autonomous edits to canon/skill/site/examples/intent. All changes require explicit user Accept (per item) in `review` / `reconcile` interactive loops.
- **Vibe-mode.** No persistent state, no engine, no derivation graph. Future "full mode" with cross-spec tracking is planned.
- **Frozen versions are read-only.** v01/v02/v03 (legacy layout) and any current-production version must not be modified.

## Status

v1. Design captured in `/Users/ilya.baimetov/.claude/plans/i-think-i-need-shiny-donut.md`. First real test will be using `init` to bring up v04 from v03.
