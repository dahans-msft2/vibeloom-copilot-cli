# AGENTS.md — [Project Name / Module Name]

This file is derived operational guidance. It is not a canonical source of truth and may be regenerated whenever upstream contracts change.

## Source Inputs

- `constitution.md`
- Relevant `spec.md`
- Relevant module spec, if any
- Trace slice for the current task
- Current `plan.md`

## Task Scope

- Change class:
- Owned write surface:
- Allowed dependencies:

## Must Load

- [contract files]
- [trace slice]

## Must Not Assume

- Anything not present in the loaded upstream contracts
- That hand edits to this file override canonical contracts

## Execution Rules

- Stay within the owned write surface for this scope.
- Do not change public interfaces without updating the owning spec.
- Do not mark canonical artifacts approved.
- Regenerate this file after upstream contract changes.

## Validation Before Finish

- Run structural checks on touched artifacts.
- Run the targeted semantic checks for touched stories, entities, and interfaces.
- Confirm tests trace to the changed contract items.
