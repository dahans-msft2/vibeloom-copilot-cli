# Reference: multi-agent

How vibeloom-dev coordinates two agents (Claude Code + Codex) running independently in their own environments.

## Why two agents?

A second perspective catches things one agent misses. The skill formalizes this without requiring inter-agent API calls (which would be expensive). Both agents run locally in their own environments; the **repo filesystem is the shared substrate**.

Russian proverb (paraphrased): "one head is good, two are better."

## Agent identity

Auto-detected at runtime.

### Detection signatures

- **Claude (Claude Code / Cowork)**: presence of `CLAUDE_*` env vars, or the `.claude/` directory in repo root with settings, or `claude` in argv0.
- **Codex**: presence of Codex-specific env vars (e.g., `OPENAI_*` in a Codex-specific config), or `codex` in argv0, or `.codex/` config directory.

If detection ambiguous, **ask the user**: "Running in Claude or Codex?". Use the answer for this session.

There is **no `--as` flag** — auto-detect only. If a user really needs to spoof identity, they can set the env var explicitly before running.

## Filename conventions

All multi-agent files live in `reports/` (flat, at repo root, gitignored).

| File | Pattern | Example |
|---|---|---|
| Own eval output | `eval-<target>-<self>.md` | `reports/eval-canon-claude.md` |
| Peer's eval output (read-only) | `eval-<target>-<peer>.md` | `reports/eval-canon-codex.md` |
| Own feedback on peer | `feedback-<target>-<self>-on-<peer>.md` | `reports/feedback-canon-claude-on-codex.md` |
| Peer's feedback on me (read-only) | `feedback-<target>-<peer>-on-<self>.md` | `reports/feedback-canon-codex-on-claude.md` |

## The multi-agent flow

1. **Round 1: independent evals.**
   - User runs `vibeloom-dev eval canon` in Claude. Claude writes `reports/eval-canon-claude.md`.
   - User runs `vibeloom-dev eval canon` in Codex. Codex writes `reports/eval-canon-codex.md`.
   - Eval has **no peer awareness** — each agent eval'd the canon fresh, independently.

2. **Round 2 (optional): cross-critique.**
   - User runs `vibeloom-dev feedback codex canon` in Claude. Claude reads `reports/eval-canon-codex.md`, independently re-reads canon, writes `reports/feedback-canon-claude-on-codex.md` with: agreement/disagreement per finding, plus new MISS-* findings Codex missed.
   - User runs `vibeloom-dev feedback claude canon` in Codex. Symmetric: writes `reports/feedback-canon-codex-on-claude.md`.

3. **Round 3 (user-driven): decision.**
   - User reads all four files (two evals + two feedbacks).
   - Decides what to act on.
   - Runs `vibeloom-dev review canon` in one agent (whichever they trust more for this target, or whichever they're sitting in).
   - The review uses one agent's findings file as the working list — typically the agent's own. The user mentally synthesizes with the feedbacks.

## What's NOT in v1

- **No iteration loop** — eval is one-shot, not multi-round-with-state-detection. (Earlier design had auto-detected filesystem state mode; rejected as over-engineered.)
- **No round cap** — there's no "3 rounds and done" because there's no auto-iteration. User does as many rounds as they want by running commands manually.
- **No synthesize/consensus command** — the synthesis is mental, by the user. Building a "merge both evals into one consensus list" command was deferred because the result is agent-dependent anyway (whichever agent runs synthesize has its own bias).
- **No feedback for non-eval ops** — `feedback` is eval-only in v1. Generate stays single-agent. Review/reconcile are interactive with the user (cross-agent critique of user decisions is weird). Future extension possible.

## Handoff convention

The handoff between agents is **manual** ("now run this command in the other agent"). The skill makes the handoff zero-context by writing to deterministic file paths — the other agent reads files, no copy-paste of findings between chat windows needed.

At the end of an eval/feedback command, the skill should suggest the next handoff step. e.g., after `eval canon` in Claude completes:
> Suggested next: "Run `vibeloom-dev eval canon` in Codex for a second perspective. Then `vibeloom-dev feedback codex canon` here, and `vibeloom-dev feedback claude canon` in Codex."

## Anti-patterns

- **Reading the peer's eval during your own eval** — defeats the purpose of independent first-pass evals. Use `feedback` for cross-agent assessment, not eval.
- **Editing the peer's eval file** — never. Peer's eval is read-only from your agent's perspective.
- **Inferring agent identity from history/context** — always use the runtime detection. If env signatures change between sessions, identity could flip; check at command start.
