# AGENTS.md — [Project Name / Module Name]

This file is derived operational guidance. It is not a canonical source of truth and may be regenerated whenever upstream contracts change.

## Source Inputs

- `constitution.md`
- relevant root `spec.md`
- relevant module spec, if any
- trace slice for the current task
- current `plan.md`

## Project Overview

<!-- 1-2 sentences summarizing the project or module.
     Example: "This module owns user identity and session management." -->

## Tech Stack

| Layer | Technology | Version | Notes |
| --- | --- | --- | --- |
| Runtime | | | |
| Data | | | |
| Testing | | | |
| Deployment | | | |

## Commands

```bash
# install dependencies
# run the dev server or worker
# run tests
# run linter
# build the affected target
```

## Project Structure

```text
src/              # core application code
modules/          # full-profile module directories, when present
tests/            # test files or test helpers
docs/             # governance artifacts, if kept near code
```

<!-- Replace the sketch above with the real project layout when deriving this file. -->

## Task Scope

- Change class:
- Owned write surface:
- Allowed dependencies:
- Touched IDs:

## Must Load

- [canonical contract files]
- [trace slice]
- [repro, acceptance criteria, or failing test when relevant]

## Must Not Assume

- anything not present in the loaded upstream contracts
- that hand edits to this file override canonical contracts
- that a bugfix permits an implicit upstream semantic rewrite

## Boundaries — Do NOT

- modify files outside the owned write surface for this scope
- add dependencies without updating the owning spec
- change public interfaces without updating the owning interface contract
- mark canonical artifacts as approved

## Domain Context

- Bounded context:
- Key entities:
- Key invariants:

## Code Style And Conventions

- Language mode: <!-- e.g. TypeScript strict mode -->
- Naming conventions: <!-- e.g. files kebab-case, types PascalCase, functions camelCase -->
- Formatting rules: <!-- e.g. Prettier default, ESLint strict -->
- Import rules: <!-- e.g. absolute imports via @/ alias -->

## Git Workflow

- Branch naming: <!-- e.g. feat/STORY-001-short-name -->
- Commit message style: <!-- e.g. feat(auth): add invite acceptance -->
- Review requirements: <!-- e.g. tests green, touched contracts reviewed -->

## Execution Rules

- stay within the owned write surface for this scope
- do not change public interfaces without updating the owning spec
- regenerate this file after upstream contract changes
- escalate when the loaded slice is not sufficient to make a safe change

## Testing Conventions

- add or update regression coverage when fixing bugs
- prefer contract tests for boundary changes
- trace new tests back to changed contract items

## Validation Before Finish

- run structural checks on touched artifacts
- run targeted semantic checks for touched stories, entities, invariants, and interfaces
- run the relevant project commands for lint, tests, and build health
- confirm tests trace to the changed contract items

## VibeLoom Integration

- Root spec ref:
- Module spec ref:
- Domain model ref:
- Local ID prefix:
- After significant changes, run `/vibeloom eval` over the smallest valid scope
