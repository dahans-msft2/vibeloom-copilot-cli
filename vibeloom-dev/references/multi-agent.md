# Reference: multi-agent

How vibeloom-dev coordinates multiple agents (any number, any runtime) running independently in their own environments.

## Why multi-agent?

A second perspective catches things one agent misses. A third perspective catches things both missed. The skill formalizes this without requiring inter-agent API calls (which would be expensive). All agents run locally in their own environments; the **repo filesystem is the shared substrate**.

Russian proverb (paraphrased): "one head is good, two are better." Three is better still, when the cost is just running the same prompt in another window.

## The contract (minimum viable)

1. **Each agent self-identifies with a stable, lowercase, hyphenated name.** Examples: `claude`, `codex`, `cursor`, `gemini`. The name is the agent's identity in this repo across all sessions.
2. **The agent uses that name in every file it writes** to `reports/`.
3. That's it.

No central registry of agents. No detection signatures hardcoded into the skill. No "primary vs peer" distinction. Just: every agent knows its name and stamps it on its files.

## How an agent learns its name

In rough order of preference:

1. **Env variable** `VIBELOOM_AGENT_NAME` — if set, use it.
2. **Hardcoded in the skill install** — if the user pre-configured.
3. **Ask the user** at first invocation in this repo: "What name should I use to identify my outputs? (e.g., claude, codex, cursor)". Use the answer for the session and suggest the user set `VIBELOOM_AGENT_NAME` if they want it persistent.

The user is free to call the same Claude install `claude-a` and `claude-b` if they want two parallel Claude sessions producing distinct outputs — names are user-defined, not LLM-defined.

## Filename conventions

All multi-agent files live in `reports/` (flat, at repo root, gitignored).

| File | Pattern | Example |
|---|---|---|
| Own eval output | `eval-<target>-<self>.md` | `reports/eval-canon-claude.md` |
| Another agent's eval output (read-only from your view) | `eval-<target>-<other>.md` | `reports/eval-canon-codex.md` |
| Own feedback on someone else | `feedback-<target>-<self>-on-<peer>.md` | `reports/feedback-canon-claude-on-codex.md` |

`<self>` and `<peer>` are agent names — whatever names the agents self-identify with.

## The multi-agent flow (N agents)

Generalized — works for 2 agents, 3 agents, or more:

1. **Round 1: independent evals.**
   - Each agent runs `vibeloom-dev eval <target>` in its own environment. Each writes `reports/eval-<target>-<its-name>.md`.
   - Eval has **no peer awareness** — each agent evals fresh, independently.

2. **Round 2 (optional): cross-critique.**
   - Any agent can run `vibeloom-dev feedback <peer-name> <target>` to critique any other agent's eval. Writes `reports/feedback-<target>-<self>-on-<peer>.md`.
   - For 2 agents, this gives 2 feedback files (each on the other).
   - For 3 agents, up to 6 feedback files (each on each of the other two). User picks which critiques are worth running; not all pairs are required.

3. **Round 3 (user-driven): decision.**
   - User reads everything they care about (evals + feedbacks).
   - Runs `vibeloom-dev review <target>` in whichever agent they trust most for this target. Walks findings interactively.
   - The synthesis is mental, by the user. There's no automated consensus step in v1.

## Handoff convention

The handoff between agent sessions is **manual** ("now run this command in <other-window>"). The skill makes it zero-context: the agent reads files at deterministic paths — no copy-paste of findings between chat windows needed.

At the end of an eval or feedback command, the skill should suggest the next handoff step. e.g., after `eval canon` in Claude:
> Suggested next: "Run `vibeloom-dev eval canon` in <other agent> for a second perspective. Then `vibeloom-dev feedback <other-agent> canon` here, and reciprocally in the other window."

## What's NOT in v1

- **No iteration loop** — eval is one-shot. No auto-detected filesystem state mode driving multi-round behavior. (Earlier design considered this; rejected as over-engineered.)
- **No round cap** — there's no "3 rounds and done" because there's no auto-iteration. User does as many rounds as they want.
- **No synthesize/consensus command** — the synthesis is mental, by the user. (Earlier design considered automating it; rejected because the synthesis is itself agent-biased.)
- **No `feedback` for non-eval ops** — feedback is eval-only in v1. Generate stays single-agent. Review/reconcile are interactive with the user. Future extension possible.

## Anti-patterns

- **Reading the peer's eval during your own eval** — defeats independent first-pass evals. Use `feedback` for cross-agent assessment, not eval.
- **Editing the peer's file** — never. Each agent writes only files with its own name in the filename. Peer-named files are read-only from your view.
- **Hardcoding agent names in prompts** — never reference `claude` or `codex` (or any specific name) in task templates. Always parameterize on the runtime-resolved `<self>` and `<peer>`.
- **Inferring agent identity from heuristics** — always use the explicit name. If `VIBELOOM_AGENT_NAME` isn't set and there's no hardcoded value, ASK.
