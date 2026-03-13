# AGENTS.md — [Project Name / Module Name]

This file is derived operational guidance. It is not a canonical source of truth and may be regenerated whenever upstream contracts change.

## Source Inputs

- `constitution.md`
- relevant root `spec.md`
- relevant module spec, if any
- trace slice for the current task
- current `plan.md`

## Project Overview

<!-- One or two sentences summarizing the project or module responsibility. -->

## Tech Stack

| Layer | Technology | Notes |
| --- | --- | --- |
| Runtime | | |
| Data | | |
| Testing | | |

## Commands

```bash
# install dependencies
# run tests
# run linter
# run the relevant app or worker
```

## Task Scope

- Change class:
- Owned write surface:
- Allowed dependencies:
- Touched IDs:

## Must Load

- [contract files]
- [trace slice]
- [repro or acceptance criteria, if relevant]

## Must Not Assume

- anything not present in the loaded upstream contracts
- that hand edits to this file override canonical contracts
- that a bugfix permits an implicit upstream semantic rewrite

## Execution Rules

- stay within the owned write surface for this scope
- do not change public interfaces without updating the owning spec
- do not mark canonical artifacts approved
- regenerate this file after upstream contract changes

## Testing Conventions

- add or update regression coverage when fixing bugs
- prefer contract tests for boundary changes
- trace new tests back to changed contract items

## Validation Before Finish

- run structural checks on touched artifacts
- run targeted semantic checks for touched stories, entities, invariants, and interfaces
- confirm tests trace to the changed contract items
