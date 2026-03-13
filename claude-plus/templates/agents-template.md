# AGENTS.md — [Project Name / Module Name]

<!-- AGENTS.md is derived operational guidance — it is NOT a canonical source
     of truth. It may be regenerated whenever upstream contracts change.
     The Agent reads this file to understand how to work within the project
     or module boundaries. -->
<!-- Include in both Lite and Full profiles. -->

This file is derived operational guidance. It is not a canonical source of truth and may be regenerated whenever upstream contracts change.

## Source Inputs

<!-- List the canonical artifacts this AGENTS.md was derived from. -->

- `constitution.md`
- Relevant `spec.md`
- Relevant module spec, if any
- Trace slice for the current task
- Current `plan.md`

## Project Overview

<!-- 1-2 sentences: what this project/module does.
     Example: "BookIt is an appointment-scheduling SaaS built with Next.js
     and PostgreSQL. This AGENTS.md covers the root project." -->

## Tech Stack

<!-- Mirror from spec.md Tech Stack table. Keep in sync. -->

| Layer | Technology | Version |
| --- | --- | --- |
| Language | | |
| Framework | | |
| Database | | |
| Testing | | |

## Commands

<!-- Standard commands the Agent should know how to run. -->

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Run tests
npm test

# Run linter
npm run lint

# Build for production
npm run build
```

## Project Structure

<!-- Key directories and their purpose. Helps the Agent navigate the codebase. -->

```
├── src/
│   ├── app/            # Next.js app router pages
│   ├── components/     # Shared UI components
│   ├── lib/            # Business logic and utilities
│   └── modules/        # Module directories (Full profile)
├── prisma/             # Database schema and migrations
├── tests/              # Test files
└── docs/               # VibeLoom governance artifacts
```

## Task Scope

<!-- Filled in when AGENTS.md is generated for a specific task. -->

- Change class: <!-- local | behavioral-in-module | boundary-changing -->
- Owned write surface: <!-- directories/files this task may modify -->
- Allowed dependencies: <!-- modules this task may import from -->

## Code Style & Conventions

- **Language:** <!-- e.g., TypeScript strict mode -->
- **Naming:**
  - Files: <!-- e.g., kebab-case.ts -->
  - Functions/methods: <!-- e.g., camelCase -->
  - Types/interfaces: <!-- e.g., PascalCase -->
  - Constants: <!-- e.g., UPPER_SNAKE_CASE -->
- **Formatting:** <!-- e.g., Prettier with default config -->
- **Imports:** <!-- e.g., absolute imports via @/ alias -->

## Testing Conventions

- **Test framework:** <!-- e.g., Vitest -->
- **Test file location:** <!-- e.g., co-located as *.test.ts or in tests/ -->
- **Naming convention:** <!-- e.g., describe("ModuleName") / it("should ...") -->
- **Coverage requirements:** <!-- e.g., 80% line coverage -->

## Git Workflow

- **Branch naming:** <!-- e.g., feat/STORY-001-user-registration -->
- **Commit message format:** <!-- e.g., feat(auth): add user registration (STORY-001) -->
- **PR requirements:** <!-- e.g., all tests pass, at least one approval -->

## Must Load

<!-- Artifacts the Agent must read before starting work. -->

- [contract files]
- [trace slice]

## Must Not Assume

<!-- Guard rails to prevent the Agent from drifting. -->

- Anything not present in the loaded upstream contracts
- That hand edits to this file override canonical contracts

## Boundaries — Do NOT

<!-- Critical: things the agent must never do in this project/module. -->

- Do NOT modify files outside this module's directory (Full profile)
- Do NOT add dependencies without updating spec.md
- Do NOT change public interface signatures without updating the interface contract
- Do NOT skip tests for new functionality
- Do NOT mark canonical artifacts as approved — only humans approve

## Domain Context

<!-- Key domain concepts the agent needs to understand. -->

**Bounded Context:** <!-- Which BC this module belongs to (Full profile).
     Example: "BC-001 — User Management" -->
**Key Entities:** <!-- List entity IDs from dm.md.
     Example: "ENT-001 (User), ENT-002 (UserProfile)" -->
**Key Invariants:** <!-- Domain rules that must never be violated.
     Example: "INV-001: Email must be unique across all users" -->

## Execution Rules

- Stay within the owned write surface for this scope.
- Do not change public interfaces without updating the owning spec.
- Do not mark canonical artifacts approved.
- Regenerate this file after upstream contract changes.

## Validation Before Finish

<!-- Checklist the Agent runs before declaring a task complete. -->

- Run structural checks on touched artifacts.
- Run the targeted semantic checks for touched stories, entities, and interfaces.
- Confirm tests trace to the changed contract items.
- Run linter and ensure no new warnings.

## VibeLoom Integration

<!-- How this project connects to the VibeLoom governance chain. -->

**Spec refs:**
- Root spec: `../../spec.md` (or `spec.md` for root AGENTS.md)
- Module spec: `spec.md` (for module AGENTS.md)
- Domain model: `../../dm.md`

**ID prefix for this module:** `MOD-{name}-`

**When generating code:** Always check that implementations satisfy the stories and invariants from upstream specs. Run `/vibeloom eval` after significant changes.
