# Interaction Contract Reference

This file defines runtime response shape, not methodology truth. Use canonical command forms in suggested next actions even when the input arrived through an alias.

## Mandatory Output Shape

Every command response uses:

1. `Scope`
2. `Decision / Findings`
3. `Affected IDs`
4. `Next action`

Keep output terse. Prefer findings and decisions over process narration.

For `status repo`, render:
- surface
- profile or `undecided`
- artifact state summary
- blockers or stale warnings
- next 3 valid commands

For `init project`, if the input is underspecified:
- ask only for the minimum missing product facts
- keep the interview brief and concrete
- summarize the captured facts before drafting `intent.md`
- use `Affected IDs` as `none yet` until the first artifact draft exists
- keep profile selection provisional and session-local until the product slice is approved

## Adaptive Summary Rules

### Workflow-facing review

For:
- `review artifact prd`
- `review artifact usm`

Lead with workflow and user-value language, but always cite the IDs:
- `PRD-FR-*`
- `STORY-*`
- `AC-*`
- implied `ENT-*` where relevant

Example:

```text
Scope
USM review for onboarding and invite workflows.

Decision / Findings
STORY-014 and STORY-017 describe the same user outcome with conflicting acceptance criteria.
The flow implies a shared workspace concept, but the story set never names the concept consistently.

Affected IDs
STORY-014, STORY-017, AC-022, AC-026, ENT-009 (implied)

Next action
Unify the workflow language in USM, then confirm whether ENT-009 should be formalized in DM.
```

### Technical-governance review

For:
- `review artifact dm`
- `review artifact spec`
- `eval`
- `reconcile`

Lead with:
- semantic ownership
- invariants
- module boundaries
- interface ownership
- stale implications

Always cite:
- `ENT-*`
- `INV-*`
- `MOD-*`
- `IFACE-*`

## Bugfix Responses

`fix issue` starts with:
- repro
- expected behavior
- violated or missing contract
- regression impact

Example:

```text
Scope
Bugfix path for invite expiration.

Decision / Findings
The repro shows invite links expiring at 59 minutes, while the expected behavior is 2 hours.
The likely mismatch is between IFACE-INV-002 TTL handling and INV-014.

Affected IDs
IFACE-INV-002, INV-014, STORY-031

Next action
Add regression coverage for the 2-hour TTL, then reconcile spec and code in the invite module.
```

## Init Interview Responses

Keep the interview to the smallest set of facts that makes `intent.md` and the first downstream recommendations credible:

- project type and system goal
- scope size and expected lifetime
- primary users and first-release outcomes
- hard constraints or technology exclusions
- likely bounded contexts, if already obvious from the workflows

If the bounded contexts are unclear, ask for the main workflows instead and defer the profile recommendation.

When useful, end the interview summary with a provisional `lite` or `full` recommendation, the reason for it, and the reminder that profile choice is not final until the product slice is approved.

Example:

```text
Scope
Init interview for a new governed project.

Decision / Findings
The request identifies the domain but not the target users, likely scope size, hard constraints, or first success signal. Those details are needed to draft a stable intent artifact and make a credible provisional profile recommendation.

Affected IDs
none yet

Next action
Capture the system goal, primary users, initial workflow scope, hard constraints, and first success metric, then draft intent.md.
```

## Status Responses

Example:

```text
Scope
Repo status for the governed workspace.

Decision / Findings
Surface is `code-first`. Profile is `full`. The active risk is technical: `spec.md` is still draft and `MOD-billing` is stale because IFACE-004 changed upstream. The product stack is approved.

Affected IDs
ART-SPEC-001, MOD-billing, IFACE-004

Next action
Review the stale billing interface slice, then run /vibeloom reconcile module billing.
```

## Help Topic Responses

For `help topic ...`, answer from the requested topic only, summarize the most actionable rules first, and end with one or two example commands when relevant.

## Error Contract

When the command is invalid:
- one line naming the invalid token or missing segment
- one line showing the correct form
- one line showing nearest valid alternatives when helpful

Example:

```text
Invalid noun `artifacts` for verb `review`.
Use: /vibeloom review artifact <intent|prd|usm|dm|spec|constitution>
Closest forms: /vibeloom review artifact usm, /vibeloom review module billing
```

## Triage Contract

Bare `$vibeloom` returns governed state, current surface, blockers, profile when known, and the next 3 valid commands. When possible, include one short reason per suggested next command.

Do not return the full command catalog unless the repo state is empty or broken.
