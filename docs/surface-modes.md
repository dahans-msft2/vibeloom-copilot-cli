# Surface Modes Guide

VibeLoom has one canonical methodology and two user-facing surfaces:

- `product-first`
- `code-first`

Surface modes change what the user sees first. They do not change:

- the canonical artifact stack
- approval scopes
- lifecycle states
- traceability rules
- reconcile asymmetry

## Product-First

Use `product-first` when the user wants to lead with:

- goals and requirements
- workflows and acceptance criteria
- domain language and invariants
- scope and approval readiness

This is the default surface.

## Code-First

Use `code-first` when the user wants to lead with:

- `spec.md`
- module boundaries
- interfaces and ownership
- technical policies
- implementation-safe change scope

`code-first` is an advanced engineering surface. It does not remove `prd`, `usm`, or `dm`; it collapses them until the task needs them.

## Session Scope

Surface mode is session-scoped only.

- switch with `/vibeloom surface <product-first|code-first>`
- do not persist it to repo state
- do not infer a permanent repo preference

## Escalation Triggers

When `code-first` is active, automatically surface the relevant `prd/usm/dm` slices if any of these are true:

- the change is `boundary-changing`
- workflows or actors are touched or ambiguous
- concepts, entities, invariants, interfaces, or NFR boundaries are touched or ambiguous
- semantic drift appears during `review`, `eval`, or `reconcile`
- the user explicitly asks to inspect product or domain artifacts

## Approval And Review

All approvals remain available in both surfaces:

- `approve intent`
- `approve product`
- `approve spec`

`code-first` may collapse the product/domain layers, but it must never hide that product approval is still required when product artifacts are draft, stale, or blocking.

## Recommended Use

Use `product-first` for:

- new product framing
- workflow review
- acceptance clarification
- semantic drift resolution

Use `code-first` for:

- module-scoped engineering work
- interface-focused design
- architecture review
- safe local and behavioral-in-module changes

## Examples

```text
/vibeloom surface code-first
/vibeloom status
/vibeloom develop add CSV export to billing module
/vibeloom review spec
/vibeloom review usm
```

In the example above, `status`, `develop`, and `review spec` should lead with technical context. `review usm` should still surface the workflow layer directly because the user asked for it.
