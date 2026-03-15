# AGENTS.md — [Project Name / Module Name]

This file is derived operational guidance. It is not a canonical source of truth and may be regenerated whenever upstream contracts change.

## Source Inputs

- `constitution.md`
- relevant root `spec.md`
- relevant module spec, if any
- trace slice for the current task
- current `plan.md`

## Commands

```bash
# install dependencies, e.g. pnpm install / npm install / bundle install
# run the dev server or worker, e.g. pnpm dev / npm run worker
# run tests for the touched slice, e.g. pnpm test --filter billing
# run linter, e.g. pnpm lint
# build the affected target, e.g. pnpm build
```

## Task Scope

- Surface:
- Change class:
- Owned write surface:
- Allowed dependencies:
- Touched IDs:

## Must Load

- [canonical contract files]
- [trace slice]
- [repro, acceptance criteria, or failing test when relevant]

## Boundaries — Do NOT

- modify files outside the owned write surface for this scope
- add dependencies without updating the owning spec
- change public interfaces without updating the owning interface contract
- mark canonical artifacts as approved
- assume anything not present in the loaded upstream contracts
- treat hand edits to this file as stronger than canonical contracts
- permit an implicit upstream semantic rewrite during a bugfix
- continue without escalating when the loaded slice is not sufficient

## Domain Context

- Bounded context:
- Key entities:
- Key invariants:

## Validation Before Finish

- run structural checks on touched artifacts
- run targeted semantic checks for touched stories, entities, invariants, and interfaces
- run the relevant project commands for lint, tests, and build health
- record the exact validation commands that were used when deriving this file for a concrete repo
- confirm tests trace to the changed contract items
