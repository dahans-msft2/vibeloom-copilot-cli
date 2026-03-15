# Profile Selection Guide

VibeLoom has two profiles, but both preserve the same canonical stack:
- `constitution.md`
- `intent.md`
- `prd.md`
- `usm.md`
- `dm.md`
- `spec.md`

The profile choice changes decomposition depth, interface discipline, and coordination overhead. It does not change whether workflow and domain semantics are recorded.

Profiles are not surfaces. Surface modes change which layer is shown first; profiles change how much decomposition and interface discipline the project needs. See [surface-modes.md](surface-modes.md).

## Lite Profile

Use `lite` when all of the following are true:

- the domain fits one cohesive bounded context
- one module can own the whole write surface safely
- parallel agent work is low-risk or infrequent
- cross-module interface contracts would add more ceremony than value

Typical characteristics:

| Aspect | Lite behavior |
| --- | --- |
| `usm.md` | separate canonical file, still required |
| `dm.md` | one bounded context or one clearly dominant context |
| Modules | one application module or a very shallow split |
| Interface ownership | minimal but still explicit when external or shared boundaries exist |
| `AGENTS.md` | usually one root file plus optional scoped variants |

## Full Profile

Use `full` when any of the following are true:

- the domain has multiple bounded contexts
- multiple agents or humans need parallel write ownership
- cross-module APIs, events, or schemas are part of normal change flow
- one change routinely touches more than one semantic boundary

Typical characteristics:

| Aspect | Full behavior |
| --- | --- |
| `usm.md` | separate canonical file, required |
| `dm.md` | multiple bounded contexts and usually a context map |
| Modules | one or more modules derived from bounded contexts |
| Interface ownership | required for APIs, events, and schemas |
| `AGENTS.md` | root plus per-module derived guidance |

## Selection Heuristics

Choose `full` when any of these signals appear during `dm.md` or `spec.md` review:

1. more than one bounded context is clearly named
2. one module cannot own the full write surface without ambiguity
3. interfaces between semantic areas need stable contracts
4. the team expects meaningful parallel execution

Default to `lite` only when the semantic model is truly cohesive and the write surface can stay single-owner without strain.

## Upgrade Path

Move from `lite` to `full` when the existing semantics no longer fit one safe execution boundary:

1. preserve the same `intent`, `prd`, `usm`, and `dm`
2. extract module boundaries from bounded contexts and ownership seams
3. define interface ownership and dependency rules in `spec.md`
4. generate module specs and derived module guidance
5. run structural and semantic evals before approving the new shape

## Downgrade Path

Downgrade from `full` to `lite` only when the domain genuinely collapses into one cohesive boundary:

1. merge module responsibilities back into one approved `spec.md`
2. retire interface ownership that no longer represents real boundaries
3. keep `usm.md` and `dm.md` as separate canonical artifacts
4. rerun evals to confirm ownership and trace links still hold

## Human Role

The agent may propose a profile with reasoning. A human approves the choice because the profile changes coordination cost and architectural discipline for future work.
