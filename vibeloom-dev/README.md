# vibeloom-dev

A Claude / Codex skill that helps develop vibeloom itself.

## What it does

Dogfoods vibeloom's own intent/product/system/code split — eval/review/generate/reconcile — to develop vibeloom's canon, skill, and site. Vibe-mode for v1: no persistent state, no derivation graph, no formal staleness tracking. Eval is the LLM-driven detector; generate is a full rewrite from current upstream.

Designed for the workflow where the user runs Claude Code in one terminal and Codex in another, and wants the two agents to independently eval the same canon and critique each other.

## Commands (quick reference)

```
vibeloom-dev init [--from vNN] [--version vNN] [--from-scratch]
vibeloom-dev eval [<target>]                          # default target: canon
vibeloom-dev review [<target>]                        # walks findings from latest eval
vibeloom-dev generate <methodology|implementation|skill|site>
vibeloom-dev reconcile [<target>]                     # walks recent generate output
vibeloom-dev feedback <peer-agent> <target>           # claude/codex
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

See [references/multi-agent.md](references/multi-agent.md). Short version:

1. `vibeloom-dev eval canon` in Claude → `reports/eval-canon-claude.md`
2. `vibeloom-dev eval canon` in Codex → `reports/eval-canon-codex.md`
3. `vibeloom-dev feedback codex canon` in Claude → `reports/feedback-canon-claude-on-codex.md`
4. `vibeloom-dev feedback claude canon` in Codex → `reports/feedback-canon-codex-on-claude.md`
5. User reads everything, decides.

All output to gitignored `reports/` at repo root. Flat, ephemeral, overwritten on rerun.

## Constraints

- **Propose only.** Never autonomous edits to canon/skill/site/examples/intent. All changes require explicit user Accept (per item) in `review` / `reconcile` interactive loops.
- **Vibe-mode.** No persistent state, no engine, no derivation graph. Future "full mode" with cross-spec tracking is planned.
- **Frozen versions are read-only.** v01/v02/v03 (legacy layout) and any current-production version must not be modified.

## Status

v1. Design captured in `/Users/ilya.baimetov/.claude/plans/i-think-i-need-shiny-donut.md`. First real test will be using `init` to bring up v04 from v03.
