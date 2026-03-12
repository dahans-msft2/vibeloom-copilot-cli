# AGENTS.md — [Project Name / Module Name]

<!-- This file provides instructions for AI coding agents working on this project or module. -->

## Project Overview

<!-- 1-2 sentences: what this project/module does -->

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| | | |

## Commands

```bash
# Install dependencies
# Run dev server
# Run tests
# Run linter
# Build for production
```

## Project Structure

```
# Key directories and their purpose
```

## Code Style & Conventions

- **Language:**
- **Naming:**
  - Files:
  - Functions/methods:
  - Types/interfaces:
  - Constants:
- **Formatting:**
- **Imports:**

## Testing Conventions

- **Test framework:**
- **Test file location:**
- **Naming convention:**
- **Coverage requirements:**

## Git Workflow

- **Branch naming:**
- **Commit message format:**
- **PR requirements:**

## Boundaries — Do NOT

<!-- Critical: things the agent must never do in this project/module -->

- Do NOT modify files outside this module's directory (Full profile)
- Do NOT add dependencies without updating spec.md
- Do NOT change public interface signatures without updating the interface contract
- Do NOT skip tests for new functionality

## Domain Context

<!-- Key domain concepts the agent needs to understand -->

**Bounded Context:** <!-- Which BC this module belongs to (Full profile) -->
**Key Entities:** <!-- List entity IDs from dm.md -->
**Key Invariants:** <!-- Domain rules that must never be violated -->

## VibeLoom Integration

**Spec refs:**
- Root spec: `../../spec.md` (or `spec.md` for root AGENTS.md)
- Module spec: `spec.md` (for module AGENTS.md)
- Domain model: `../../dm.md`

**ID prefix for this module:** `MOD-{name}-`

**When generating code:** Always check that implementations satisfy the stories and invariants from upstream specs. Run `/vibeloom eval` after significant changes.
