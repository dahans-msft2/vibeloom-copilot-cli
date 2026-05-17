<!--
  Default PR template for learn-composer.
  Agent-opened PRs will fill this out automatically.
  Human-opened PRs: fill out whatever applies and delete the rest.
-->

## Summary

<!-- One paragraph: what changed and why. -->

## Task linkage

- **Task ID:** `T-YYMMDD-NN` <!-- or "N/A" for human-authored PRs -->
- **State file:** [`.agent-state/T-YYMMDD-NN.json`](../.agent-state/T-YYMMDD-NN.json)
- **Unblocks issue:** #<!-- issue number, if this PR is an unblock-PR -->

## How this unblocks task `T-YYMMDD-NN`

<!-- REQUIRED for unblock-PRs filed by Copilot. Explain which step in the escalation chain this resolves. -->

## Type of change

- [ ] Feature
- [ ] Bug fix
- [ ] Infrastructure (Helm / K8s / Docker-Compose / Dockerfile / Terraform / Bicep) — **requires human approval**
- [ ] Documentation
- [ ] Refactor / chore
- [ ] Agent prompt / orchestration

## Verification

- [ ] Unit tests pass: `<exact command>`
- [ ] Lint / type-check passes: `<exact command>`
- [ ] All acceptance criteria from the linked task state file are ticked.
- [ ] No `git push --force`, no `--no-verify`, no destructive operations.
- [ ] If this changes infra, a human approved the change before commit.

## Notes for reviewer

<!-- Anything the human merger should know. -->
