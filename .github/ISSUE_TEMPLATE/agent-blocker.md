---
name: Agent blocker (Copilot handoff)
about: Filed by the Tech Lead agent when the autonomous team cannot proceed. Assigned to @copilot.
title: "[BLOCKER] <task-id>: <one-line summary>"
labels: ["agent-blocker", "copilot"]
assignees: ["copilot"]
---

> **Auto-filed by the Tech Lead agent.** Do not edit the structure below — Copilot relies on it.

## Task

- **Task ID:** `T-YYMMDD-NN`
- **State file:** [`.agent-state/T-YYMMDD-NN.json`](../.agent-state/T-YYMMDD-NN.json)
- **Branch:** `develop`
- **Source docs:** <!-- repo-relative links to Documents/Research/*.md grounding this task -->

## Blocker category

<!-- exactly one of: credentials | ambiguity | test-failure | external-service | architecture -->

## Summary

<!-- One paragraph. What is the team stuck on, in plain English? -->

## Escalation chain

<!-- Append entries from `state.history[].attempts[]`. Every attempt that was made and failed.
     This section MUST show: which agent, what hypothesis, what action, what result. -->

| # | Agent | Hypothesis | Action | Result |
|---|-------|------------|--------|--------|
| 1 | backend-engineer | … | … | … |
| 2 | backend-engineer | … | … | … |
| 3 | project-manager  | … | … | … |
| 4 | tech-lead        | … | … | … |

## What we need from the unblock PR

### Acceptance criteria

- [ ] <!-- testable item 1 -->
- [ ] <!-- testable item 2 -->
- [ ] <!-- testable item 3 -->

### Suspected files / paths

- `path/one.py`
- `path/two.tsx`
- `path/three.yaml`

### Definition of Done

- [ ] All acceptance criteria above are ticked.
- [ ] Unit tests pass locally (`<exact test command>`).
- [ ] Linters / type-checkers pass (`<exact lint command>`).
- [ ] No new top-level dependencies introduced without justification in the PR description.
- [ ] PR targets `develop` (not `main`).
- [ ] PR description includes a "How this unblocks task `T-YYMMDD-NN`" section.

## After merge

The human will re-invoke the Tech Lead, which will:

1. List paused tasks (including this one).
2. Verify the merge SHA referenced here matches `git log`.
3. Resume from `state.cursor` in [`.agent-state/T-YYMMDD-NN.json`](../.agent-state/T-YYMMDD-NN.json).

/cc @copilot
