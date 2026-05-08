# VibeLoom v0.3.0 — release notes (TEMPLATE)

**For Session 3 agent — fill in placeholders marked `<…>` before tagging.**
**For Session 2 agent — produce a draft of this in your final report.**

---

## VibeLoom v0.3.0

**Released:** `<UTC ISO-8601 date>`
**Source commit:** `<SHA>`
**Tarball:** `vibeloom-v0.3.0.tar.gz` (sha256: `<hash>`)
**Methodology:** [codæ](https://vibeloom.ai/codae) — contract-driven agentic engineering

---

## What's in this release

**The codæ paradigm shipped as a working tool.** v0.3 is the first end-to-end implementation: methodology, deterministic engine, skill bundle, site, all canon-aligned.

### Capabilities

- **Five operating modes:** `vibe` (compact, solo), `pm` (product-led), `dev` (tech-led), `ux` (design-led), `expert` (all gates explicit).
- **Eight orthogonal operations:** `init`, `import`, `generate`, `eval`, `review`, `reconcile`, `approve`, `status`.
- **Deterministic Python engine** — zero runtime dependencies; Python 3.10+; CLI surface invokable from any agent.
- **41 templates** — artifact templates per tier + 14 task templates + skill manifest + references + subagent prompt.
- **Trace families:** approval, generation, eval, code-sync, decision (with IDR / PDR / UDR / ADR / general classification), import, plus the structured ID registry.
- **Brownfield import** — bottom-up contract inference from existing code with confidence + evidence.
- **Verification ladder** — decidable structural eval, mechanical validation runners, heuristic semantic eval.
- **§5.1 derivation rules + §8.2 universal-trace** — every non-root item has at least one upstream basis transitively reaching `CAP` or `CST`.

### Loadable as a Skill

Clone the repo + point Claude Code or Codex at it as a Skill source. SKILL.md auto-registers. `/vibeloom <command>` routes to the right task template.

---

## §16 acceptance checklist

| # | Item | State | Citation |
|---|---|---|---|
| 1 | `.vibeloom/cache/` and `.vibeloom/traces/` are separated | `<state>` | `<engine commit / log>` |
| 2 | Approval baseline trace-backed (JSONL append-only) | `<state>` | `<…>` |
| 3 | ID registry persists retired IDs and next counters | `<state>` | `<…>` |
| 4 | Trace families have schema_version | `<state>` | `<…>` |
| 5 | Code-sync traces connect contract IDs to file hashes + validation evidence | `<state>` | `<…>` |
| 6 | Review and reconciliation packets exist with user-notes write capability | `<state>` | `<…>` |
| 7 | Task templates use markdown structure (10 sections), not YAML wrappers | `<state>` | `<skill log>` |
| 8 | Subagent writes patch-staged in `.vibeloom/runs/`, validated, atomic | `<state>` | `<…>` |
| 9 | Dispatch plan + wave-assembly + parallel semantics match §13.1–§13.3 | `<state>` | `<…>` |
| 10 | Subagent task header schema is the only orchestrator↔subagent contract | `<state>` | `<…>` |
| 11 | Validation registry parsed and runners invokable | `<state>` | `<…>` |
| 12 | Product/UX peer generation supports mockup evidence with `MOCK-####` | `<state>` | `<…>` |
| 13 | `ux` mode supported as a fifth top-level mode | `<state>` | `<…>` |
| 14 | Verification ladder reflected in eval routing | `<state>` | `<…>` |
| 15 | Component / container / BC rules match methodology §6.5 | `<state>` | `<…>` |
| 16 | Engine validates `derives_from` per §5.1 + §8.2 (universal-trace) | `<state>` | `<…>` |
| 17 | `status` distinguishes the 6 categories | `<state>` | `<…>` |
| 18 | Each operation has explicit, traceable execution semantics §15.1–§15.8 | `<state>` | `<…>` |
| 19 | Vibe layout genuinely minimal (no graph cache, no code-sync trace) | `<state>` | `<…>` |
| 20 | Templates only as fenced blocks; tree is build artifact | `<state>` | `<…>` |

**State legend:** ✓ (engine-✓ / skill-✓) · engine-deferred · pending-live-load · blocked

---

## Smoke-test results

**vibe-mode pipeline** (Session 2 Step 6):
- Transcript: `<smoke-vibe.log path>`
- `init` / `eval` / `approve` / direct-edit + `detect-edits` cycle: `<pass / partial>`

**pm-mode pipeline** (Session 2 Step 7):
- Transcript: `<smoke-pm.log path>`
- `init` → review/approve intent → generate product-specs → review/approve product → generate system-specs → affected → dispatch → status: `<pass / partial>`

---

## Static skill-manifest validation (Step 10a)

- SKILL.md frontmatter against Claude Code schema: `<pass / fail>`
- All `references/<file>.md` paths resolve: `<pass / fail>`
- No reserved characters / parser-breaking constructs in body: `<pass / fail>`
- `argument-hint` matches body promises: `<pass / fail>`

---

## ⏳ Pending live-load test (Step 10b — the human's first post-handoff task)

Install the bundle into a clean Claude Code instance and confirm:
- Skill registers (no errors at load time).
- `/vibeloom` shows the argument-hint.
- A trial `/vibeloom init --mode vibe "test"` routes through SKILL.md → `tasks/init.md` → engine `init` correctly.

If 10b fails: the SKILL.md template needs editing in `vibeloom-templates.md`; re-extract and rebuild.

---

## Reproducibility

- Bundle re-built twice on the same source commit: `<byte-identical / mismatch>` — sha256 confirmed: `<hash>`
- Tarball flags applied: `--sort=name --owner=0 --group=0 --numeric-owner` + `gzip -n` + fixed mtimes.

---

## Install

```bash
# Clone:
git clone https://github.com/ilya-baimetov/vibeloom.git
cd vibeloom

# Or download the release tarball:
curl -L https://github.com/ilya-baimetov/vibeloom/releases/download/v0.3.0/vibeloom-v0.3.0.tar.gz | tar -xz
cd vibeloom-v0.3.0

# Verify the engine works:
python3 -m vibeloom_engine parse --repo /tmp/scratch  # or other engine command

# Load as Claude Code Skill (Codex similar):
# > add vibeloom as a Skill source from /path/to/vibeloom/v03

# Then:
# > /vibeloom init --mode vibe "your project intent in one line"
```

---

## What's deferred

- **`test-skill.md`** — behavioral testing of the skill bundle on scratch repos. Catalogued scenarios in [skill-review-report.md §6](skill-review-report.md). Will materialize in v0.4.
- **A4 Cognitive-surface instrumentation** (per [roadmap A4](v03/roadmap.md)) — engine instruments and reports compression-ratio metrics. Future.
- **CGKG-B promotion** — knowledge graph → context graph (provenance materialized). Future.

---

## Spec ambiguities surfaced + chosen interpretations

(populated by Session 2 final report — items the build agent flagged with `# spec ambiguity:` comments)

`<copy from skill-build-report.md §6 if any>`

---

## Spec bugs surfaced (no auto-fixes)

(populated by Session 2 final report — §-vs-§ contradictions surfaced and adjudicated)

`<copy from skill-build-report.md §6 if any>`

---

## Source commit SHAs

- **Canon source:** `<commit SHA>`
- **Engine source:** `<commit SHA>` (Session 1 deliverable)
- **Bundle source:** `<commit SHA>` (Session 2 deliverable)
- **Build prompts:** `<commit SHA>` of `build-engine.md` + `build-skill.md`

---

## Acknowledgments

VibeLoom v0.3 codifies the codæ paradigm — contract-driven agentic engineering. The discipline is built on Bertrand Meyer's Design by Contract heritage and 17 empirical 2026 studies (cited in the [manifesto references](https://vibeloom.ai/codae#references)).

Particular thanks to the codæ thesis itself — the discipline of "contract in, production system out" came from real failures observed across SlopCodeBench (Mar 2026), AI-debt in the wild (Mar 2026), CMU Cursor study (Jan 2026), and Comprehension Debt (Apr 2026).

— Ilya Baimetov
