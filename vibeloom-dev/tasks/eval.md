# Task: eval

Adversarial consistency/coherence check across vibeloom artifacts. Produces a prioritized findings packet for downstream `review`. Does NOT modify any artifacts.

## Purpose

- Detect drift, contradiction, authority violation, vagueness, and stale claims across the targeted artifacts.
- Produce a findings packet the user can walk interactively with `review`.
- Support the multi-agent workflow: each agent writes its own findings file (named with its self-identified name per `references/multi-agent.md`); peers can later run `feedback <peer> <target>` to critique each other.

## Inputs

- `<target>` (optional, default `canon`) — one of: `intent`, `manifesto`, `methodology`, `implementation`, `skill`, `site`, `canon`, `all`.
- `--version <vNN>` (optional, default = latest mutable) — which version to eval against.
- Self-identified: the running agent's name (per `references/multi-agent.md`).

## Preconditions

- The target's source files exist under `vNN/`.
- The current agent's own name is resolvable per `references/multi-agent.md` (env var, hardcoded install, or ask user — Step 0 below).
- `reports/` directory exists at repo root (create with `mkdir -p reports/` if not — it's gitignored).

## Steps

0. **Resolve own agent name.** Per `references/multi-agent.md`:
   1. If `VIBELOOM_AGENT_NAME` env var is set, use it.
   2. Else if the skill install has a hardcoded name, use it.
   3. Else ask the user: "What lowercase, hyphenated name should I use to identify my outputs in this repo? (e.g., `claude`, `codex`, `cursor`, `gemini`)". Use the answer for the session.
   Bind this to `<self>` for the rest of the task. All filenames written below use this name.

0.5. **Ensure `reports/` exists.** Run `mkdir -p reports/` from the repo root. The directory is gitignored (per `/file-layout.md §5`); creating it is idempotent.

1. **Resolve target → file list.**
   - `intent` → `vNN/intent.md`
   - `manifesto` → `vNN/canon/codæ-manifesto.html`
   - `methodology` → `vNN/canon/vibeloom-methodology.md`
   - `implementation` → `vNN/canon/vibeloom-implementation.md`, `vNN/canon/vibeloom-templates.md`
   - `skill` → `vNN/skill/**` (SKILL.md + references + tasks + artifacts + engine/)
   - `site` → `vNN/site/**` (public/ HTML, CSS, comparison-source.html)
   - `canon` → intent + manifesto + methodology + implementation (union of above)
   - `all` → canon + skill + site

2. **Load applicable reference passes** based on target:
   - canon, intent, manifesto, methodology, implementation, or all → `references/eval-passes-canon.md`
   - skill or all → `references/eval-passes-skill.md`
   - site or all → `references/eval-passes-site.md`

3. **Build a source map.**
   - For each file in target, extract: heading outline, major definitions, schemas/IDs/trace families, repeated claims, downstream surfaces this file likely affects.
   - Keep concise; this is audit evidence, not a new artifact.

4. **Run adversarial passes** (per the loaded reference). For each pass, look for concrete findings with file/section/line evidence. The reference defines the passes; common ones include:
   - **Authority and separation** — does each fact have one canonical owner? (manifesto owns WHY, methodology owns WHAT, implementation owns HOW, templates materialize; site is marketing-register and doesn't own facts.)
   - **Internal consistency** — does X claim consistently across documents? (e.g., does methodology's modes section agree with implementation's mode-specific runtime behavior?)
   - **Cross-layer alignment** — does intent.md's capabilities have a paradigm anchor in manifesto? Do all manifesto principles surface in intent CAPs/CSTs (or are explicitly marked manifesto-only)? Does methodology cover all intent CAPs? Etc.
   - **Concision and load-bearing value** — can a paragraph/table/example be removed without breaking a downstream consumer?
   - **Operational adequacy** — are runtime rules precise enough for an agent or engine to implement?
   - **Known failure probes** — version-specific gotchas (e.g., for skill: do task templates reference task names that match SKILL.md routing?; for site: does the HTML reflect current canon, or is it stale from a prior version?).

5. **Format findings** to the quality bar in `references/eval-passes-<target>.md`. Every finding has:
   - `id` (e.g., `CANON-001`, `SKILL-001`, `SITE-001` — prefix matches target)
   - `severity` (Critical / High / Medium / Low)
   - `location` (file:section, or file:line if narrow)
   - `issue` (what is wrong)
   - `why it matters` (downstream consequence)
   - `proposed fixes` (1-3 options; default 1, more only when there's genuine ambiguity in how to fix)
   - `recommended fix` (one option + rationale)
   - `verification` (how to check the fix worked)
   - `downstream impact` (which other artifacts this finding affects)

6. **Reject vague findings.** "Tighten wording" is not a finding unless it cites the exact wording and a concrete replacement direction.

7. **Order findings by priority** (per `references/eval-passes-<target>.md`'s priority rules; typically: schema/identity contradictions → authority violations → stale/false claims → concision cuts → prose polish).

8. **Write the findings file** to `reports/eval-<target>-<this-agent>.md`. Overwrite any existing file.

9. **Print a summary** to the user:
   - Target, version, agent identity, file written.
   - Count of findings by severity.
   - Top 3 findings (id + one-line summary).
   - Suggested next: `vibeloom-dev review <target>` to walk findings, OR (if multi-agent perspective is desired) "run `vibeloom-dev eval <target>` in another agent (in its own environment), then `feedback <that-agent-name> <target>` here to critique its findings."

## Output

- `reports/eval-<target>-<this-agent>.md` — the findings packet.
- A printed summary.

## Postconditions

- No artifact under `vNN/` is modified (eval is read-only on the artifacts).
- The findings file exists and is well-formed per the quality bar.
- The user knows what to do next.

## Constraints

- **Read-only on artifacts.** Eval never modifies canon/skill/site/examples/intent. Only writes to `reports/`.
- **One agent per run.** The skill writes ONLY to its own agent's file (`-claude.md` or `-codex.md`). Never overwrites the peer's file.
- **No peer awareness.** Eval does NOT read the peer's eval file. That's `feedback`'s job. (Reading peer's eval would couple this agent's findings to the other's; we explicitly want independent first-pass evals.)
- **Concrete or no finding.** Every finding cites evidence and proposes specifically what would fix it. No "general polish" findings.

## Invariants

- For a given (target, version, agent), eval is idempotent up to LLM nondeterminism: rerunning produces a comparable findings packet (same major findings, possibly different ordering/phrasing of edge cases).
- Findings IDs are stable within a run but not across runs (no persistent ID registry — vibe-mode).

## Failure modes

- **Target files missing.** Halt with the specific missing path. Suggest `init --version vNN` if vNN doesn't exist, or check the layout per `/file-layout.md`.
- **Reference pass file missing.** Halt with "missing references/eval-passes-<X>.md — this skill is incomplete; please report." This shouldn't happen in a healthy install.
- **Agent name not resolvable from env or install.** Step 0 falls back to asking the user. If the user declines or provides an invalid name (non-lowercase, contains whitespace, or matches an existing peer name in `reports/`), halt and surface the constraint.
- **More than ~20 findings.** That's expected for first-eval of a fresh version. Proceed; the user will walk Critical/High first via `review`.

## Validation gates

- After step 8: the findings file parses as valid markdown.
- Every finding in the file has all required fields (id, severity, location, issue, why, fixes, recommended, verification, downstream).
- The filename matches the pattern `eval-<target>-<agent>.md` exactly (lowercase, hyphenated).
- `git status --short reports/` shows only the new/updated file (reports/ is gitignored, but this is a sanity check that we didn't accidentally write outside reports/).
