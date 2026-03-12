# VibeLoom Methodology Overview

## What is VibeLoom?

VibeLoom is a contract-driven vibe coding methodology. It bridges the gap between a loose idea (intent) and production-quality code by generating a tiered stack of structured specifications — each verified against its upstream contracts.

## Why?

Prompt-first code generation ("vibe coding") works for prototypes and small projects. It breaks down when you need:

- **Long-lived systems** — architectural coherence across months of development
- **Multi-agent development** — parallel agents working without breaking each other's work
- **Incremental evolution** — changing one part without corrupting the whole
- **Human oversight** — verifying that what's built matches what's intended

VibeLoom solves these by making specifications the source of truth, with code as a downstream derivative.

## The Contract Stack

```
intent.md          ← Loose prose: what you want to build
    ↓
prd.md             ← Structured requirements + user story map
    ↓
dm.md              ← Domain model (DDD): entities, relationships, invariants
    ↓
spec.md            ← Technical design: architecture, APIs, modules, deployment
    ↓
module specs       ← Per-module specs with interface contracts (Full profile)
    ↓
code + tests       ← Generated from and verified against specs
```

**Every arrow is bidirectional.** When you edit a downstream spec, the methodology checks upstream for consistency. When you change an upstream spec, downstream specs are marked stale and regenerated.

## Evals — The Enforcement Mechanism

Specs aren't just documentation — they're evals. Three tiers:

1. **Structural (blocking):** Mechanical checks — all IDs valid, all cross-references resolve, all required sections present.
2. **Semantic (warnings):** Reasoning checks — does the code cover all stories? Are there contradictions between tiers?
3. **Behavioral (on-demand):** Test generation — scenarios from stories, invariant tests from domain model, contract tests from interfaces.

## Profiles

| | Lite | Full |
|---|---|---|
| **When** | ≤15 entities, single domain, single agent | Multiple domains, parallel agents, >50 files |
| **USM** | Inlined in prd.md | Separate file |
| **Modules** | None (whole app is one unit) | Per bounded context |
| **Interface contracts** | Not needed | Required |

## Key Commands

```
/vibeloom init      — Start a new project
/vibeloom import    — Bring existing code under the methodology
/vibeloom generate  — Generate the next artifact
/vibeloom approve   — Approve after review
/vibeloom develop   — Make an incremental change
/vibeloom eval      — Run consistency checks
/vibeloom reconcile — Fix inconsistencies after manual edits
/vibeloom status    — See where you are
```

## The Philosophy

1. **Specs are concise.** Not 100-page documents — structured markdown that humans can scan in minutes.
2. **Humans verify, agents generate.** The Agent produces artifacts; you review, edit, and approve.
3. **Upstream specs are evals.** Every generated artifact is checked against its contracts.
4. **Modules are agent boundaries.** Each module fits in a context window and can be worked on independently.
5. **Reconciliation is bounded.** One up-pass, one down-pass, one validation — no infinite loops.
