# Competitor Comparison

This note captures what the Codex methodology package borrows from the closest alternatives and where it intentionally differs.

## Comparison Set

| System | Closest strength | Limitation relative to this methodology |
| --- | --- | --- |
| Tessl | Spec-driven process plus dependency/library knowledge separation | Less explicit about mandatory domain modeling and long-lived stale reconciliation |
| Kiro Specs | Pragmatic per-change workflow, strong steering model, explicit bugfix guidance | Feature-centric rather than centered on a durable semantic stack |
| GitHub Spec Kit | Portable constitution, clarify/analyze/checklist discipline | Lighter on domain semantics, module ownership, and long-term reconciliation |

## Borrowed Ideas

### From Tessl

- Keep dependency and API usage knowledge separate from product meaning, even if it stays within the `spec` family.
- Preserve a strong distinction between generated code and the contracts used to generate or evaluate it.

### From Kiro

- Make scoped guidance explicit.
- Treat bugfix work as a first-class workflow rather than pretending every change is a new feature.
- Keep the methodology practical for incremental day-to-day development rather than only initial generation.

### From GitHub Spec Kit

- Use a constitution-style foundational layer to avoid repeating obvious defaults in every downstream artifact.
- Keep clarify and analyze discipline as part of the human review mindset even when the implementation is not yet automated.

## Intentional Differences

### Mandatory `USM + DM`

This methodology requires both:
- `USM` for user-visible workflows and easy semantic review
- `DM` for durable ubiquitous language, invariants, and bounded contexts

The combination is the main differentiator. Other systems often stop after requirements and design or do not insist on a separate workflow layer plus domain layer.

### Asymmetric Reconciliation

Approved upstream truth is not silently replaced by downstream edits or code drift. The agent must propose the direction of change and the human approves it.

### Derived Operational Artifacts

`AGENTS.md` and `plan.md` are explicitly non-canonical. They are execution aids, not peers to the semantic contract stack.

### Projection Restraint

The methodology allows only three durable projections so the package does not create its own context-window problem:
- trace index
- dependency/stale graph
- interface/schema manifests

## Honest Assessment

This methodology is heavier than direct agent prompting or lightweight feature-spec systems. That weight is justified only when the target is sustained, multi-agent, semantically governed development.

For small, local, well-tested changes, modern generators are often good enough without the full stack. For long-lived large codebases with parallel work and evolving semantics, the stricter contract model is the more credible approach.
