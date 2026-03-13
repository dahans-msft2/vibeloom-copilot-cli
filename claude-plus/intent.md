---
artifact_id: ART-INTENT-CODEX
artifact_type: intent
status: draft
owner: methodology
approved_by:
last_reviewed: YYYY-MM-DD
version: 1
derived_from:
  - ../intent-0.md
depends_on: []
---

# Intent: Codex Variant Of Contract-Driven Vibe Coding

## What is this package?

This package defines an intent-first methodology for building and evolving production-quality software with coding agents over a long period of time. The methodology turns a loose intent into a durable stack of structured contracts, then uses those contracts as eval surfaces for incremental implementation, refactoring, and bugfix work.

The target use case is not one-shot generation. The target is sustained, high-quality vibe coding in relatively large codebases where multiple agents or humans may work in parallel without losing semantic coherence.

## Primary users

- Technically savvy product managers and designers who can validate structured specs
- Tech leads and staff engineers who need durable governance over agent-generated code
- Execution agents operating within scoped module boundaries

## Core capabilities

1. Convert a human intent into a concise but structured contract stack.
2. Keep `USM` and `DM` mandatory so workflow semantics and domain semantics both remain explicit.
3. Support greenfield initialization and brownfield import.
4. Use upstream contracts as evals for downstream artifacts and code.
5. Support modular, multi-agent execution with deterministic context loading and explicit ownership boundaries.
6. Reconcile manual edits and code drift without silently rewriting approved upstream semantics.

## Constraints and preferences

- The methodology is intent-first, not design-first.
- The initial package targets Codex workflows, but the contract language should remain tool-agnostic.
- Specs must be highly structured, concise, and stable under long-term iteration.
- Artifact explosion is explicitly out of scope. Only three durable projections are allowed.

## Non-functional expectations

- Human readability must remain high enough for frequent review.
- Context windows must be protected through scoped loading and derived operational artifacts.
- The methodology must handle both initial generation and incremental change.

## Additional context

Closest comparators are Tessl, Kiro Specs, and GitHub Spec Kit. This package intentionally keeps the strongest ideas from those systems while adding mandatory `USM + DM`, asymmetric reconciliation, and swarm-oriented module governance.
