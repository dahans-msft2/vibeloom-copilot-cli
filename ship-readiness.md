# v0.3 ship-readiness checklist

Spot-audit run on 2026-05-08 after the canon → site → skill review trilogy. Path: **B sliced** (3 sessions: build-engine → build-skill → release).

## ✅ Pre-build: ready

| Item | Status | Notes |
|---|---|---|
| Canon: methodology.md | ✓ | 18 sections; reviewed in trilogy |
| Canon: implementation.md | ✓ | 18 sections (after CANON-FIND-006/007 cuts); §16 acceptance = 20 items including new derives_from validation |
| Canon: vibeloom-templates.md | ✓ | 41 fenced blocks; reviewed in trilogy |
| Canon: codæ-manifesto.html (canonical) | ✓ | byte-identical to site copy |
| Site (vibeloom.ai) | ✓ | reviewed in trilogy; titles unified, Contract Graph cascade closed |
| README, getting-started, roadmap, comparison | ✓ | in sync with current canon |
| Build prompts: build-engine.md | ✓ | refined per validation friction; §-refs current; derives_from test bullet added |
| Build prompts: build-skill.md | ✓ | §16/§17/§17.3 cites current; ready to run after engine ships |
| Review prompts: review-canon/site/skill.md | ✓ | trilogy-validated |
| Cross-doc § references | ✓ | spot grep — all resolve |
| §16 acceptance ↔ build-engine mapping | ✓ | 20 ↔ 20 rows |
| extract-templates.py | ✓ | parses cleanly |
| Roadmap A4 (cognitive surface) | ✓ | added in CANON-FIND-005 |
| 9 review artifacts at repo root | ✓ | canon × 3, site × 3, skill × 3 |

## ❌ Pre-build: NOT ready (blocks ship — addressed by build sessions)

| Item | Status | Resolves in |
|---|---|---|
| `v03/engine/` Python package | ✗ does not exist | Session 1 (build-engine.md) |
| Engine smoke test | ✗ never run | Session 1 |
| `templates/` extracted tree (build artifact) | ✗ not materialized | Session 2 (build-skill bundles it) |
| Skill release tarball | ✗ does not exist | Session 2 |
| GitHub release v0.3 tag | ✗ untagged | Session 3 |
| Release notes (with §16 checklist marked) | ✗ not drafted | Session 3 |

## Path B sliced — 3 sessions

### Session 1 — Build engine (~2-3 hours focused agentic, or 1 day human-paced)

**Run `build-engine.md`** with an agent. Per the prompt's priority stages I added during the validation-friction fixes:

- Stage 1 (30%): read-only primitives — parser, IDs, graph, cycle detection, layered invariants, structural-eval CLI verbs (parse/graph/eval)
- Stage 2 (15%): structural eval — all §14.1 checks
- Stage 3 (15%): trace I/O + schema versioning
- Stage 4 (15%): staleness / affected-set / direct-edit detection
- Stage 5 (15%): dispatch plan + execute_plan
- Stage 6 (10%): status classification + decision-trace render + cache

**Expected outputs:**
- `v03/engine/` Python package with all stages shipped
- Test suite: 23+ tests, ≥85% coverage on engine modules (per impl §16)
- Step 6 smoke test transcript on a scratch `/tmp/` repo
- Engine final report (per build-engine.md §Final report)
- §16 engine-side acceptance items checked off

**Pre-session sanity (run from v03/):**
```bash
test ! -d engine && echo "✓ no prior engine; clean start"
git status --short  # should be clean
git log -1 --format="canon at %h %s"  # latest canon SHA
```

**Post-session verify:**
- `pytest -q v03/engine/tests/` passes 100%
- `pytest --cov=vibeloom_engine` reports ≥85%
- All Stage verify gates passed per the build-engine.md prompt
- Engine commit SHA tagged in handoff

**Handoff to Session 2:** the engine commit SHA (build-skill.md uses it as its starting point per impl §16 acceptance).

### Session 2 — Build skill bundle (~half-day focused agentic)

**Run `build-skill.md`** with an agent. Preconditions per its prompt:
- engine/ exists, tests pass
- engine-related items in §16 are ✓
- canon hasn't moved since Session 1 (or the agent re-validates)

**Expected outputs:**
- `templates/` materialized via extract-templates.py (gitignored build artifact)
- Skill bundle release tarball (e.g. `vibeloom-v0.3.tar.gz`) with sha256
- Smoke-test transcripts for vibe-mode and pm-mode pipelines
- Live-load sanity test (Step 10b) — manual handoff at end (Claude Code or Codex actually loads SKILL.md)
- Release notes draft with §16 checklist marked (engine-✓ / skill-✓ / blocked / pending-live-load)

**Pre-session sanity:**
- engine commit SHA from Session 1 hasn't drifted
- No new canon changes since Session 1 (or re-baseline)

**Post-session verify:**
- Tarball exists, sha256 captured
- Both smoke tests transcripts captured
- §16 acceptance fully marked

### Session 3 — Release v0.3

This is mostly mechanical:

- [ ] Tag `v0.3.0` on the release commit
- [ ] Push tag
- [ ] Create GitHub release with the release notes from Session 2
- [ ] Attach skill bundle tarball + sha256
- [ ] Site spot-check (re-render get-started.html — verify install/Skill-source command in copy still works against the released tarball; update if needed)
- [ ] Optional: announce on relevant channels

**Pre-session sanity:**
- v0.3.0 not already tagged (`git tag --list | grep v0.3.0`)

**Post-session verify:**
- Tag exists upstream
- GitHub release page is live
- Tarball downloadable + sha256 matches
- A fresh clone + tarball install works against `/vibeloom init --mode vibe "test"` smoke

## Risk notes

1. **Session 1 first-production-run risk.** The validation worktree got ~40% (Stages 1-3 mostly). Stages 4-6 (~60% of surface — staleness/affected/dispatch/status/decision-rendering/cache) have never been built end-to-end in production form. Friction-free completion is not guaranteed. Plan: agent surfaces friction → user adjudicates → may take longer than 1 day if novel issues emerge.

2. **Skill load-test (Step 10b) is manual.** It requires actually loading the produced bundle into Claude Code or Codex and confirming `/vibeloom` commands route correctly. Out of agent's hands; a small post-handoff task for the user.

3. **§16 has 20 items.** Most are engine-owned, some are skill-owned, all need to be marked in release notes. Treat any "blocked" as a release blocker; document any "deferred" with explicit rationale.

## Optional pre-Session-1 cleanups

These would be nice-to-have but **not blockers**:

- Delete the lingering `worktree-agent-afbed1bf8df18d8b5` branch from local (~ pointing at the validation MVP). `git branch -D worktree-agent-afbed1bf8df18d8b5` — destructive, only if the validation engine isn't useful as a starting checkpoint.
- Delete the empty `.claude/worktrees/` dir if it bothers you.

## Decision

**Ready to kick off Session 1?** I'll spawn the build-engine agent in a fresh worktree (isolated, can fail without polluting main), then surface the result for your review before merging.

Or want any pre-flight adjustment first?
