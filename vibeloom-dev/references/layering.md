# Reference: layering

The vibeloom-as-a-product layering model that dev-skill enforces.

## The dependency chain

```
(intent ↔ manifesto) ──> methodology ──> implementation (+ templates) ──> skill (+ engine)
                                                                                      │
                                                                                      ▼
                                                                                    site
```

- **intent and manifesto are sibling roots** with bidirectional consistency. Both are hand-authored. Eval checks both directions.
- **methodology** derives from intent + manifesto. Generated.
- **implementation + templates** derive from methodology. Generated together (one unit; templates materialize implementation).
- **skill + engine** derive from implementation + templates. Skill bundle is extracted from templates mechanically; engine is hand-authored Python that COULD be regenerated from implementation (drift recovery), but in practice is maintained directly.
- **site** is a marketing-register sibling of skill, also derived from methodology + implementation (and manifesto for framing). Must not contradict canon.

## The intent ↔ manifesto sibling relation

Both intent and manifesto express "what vibeloom is about" at the highest level. They're in different registers:

- **intent**: structured/technical. Capabilities (CAP-####), Constraints (CST-####), Vision, Context.
- **manifesto**: philosophical/HTML/design-heavy. Paradigm, principles, motivation, rhetorical claims.

The two should AGREE but in different styles. Eval checks:

- **Forward direction:** every CAP/CST in intent is expressible in manifesto's paradigm. (If intent says "support multi-agent reviews" and manifesto's paradigm wouldn't accommodate that, there's drift — fix one or the other.)
- **Reverse direction:** every principle in manifesto surfaces as an intent CAP/CST, OR is deliberately marked manifesto-only philosophy. (If manifesto trumpets "human-in-the-loop approval at every layer" but intent has no CST about approval gates, there's drift.)

Mismatches → eval surfaces a finding. User decides which to amend.

## The down-flow

Methodology owns WHAT (concepts, operations, modes, status semantics).
Implementation owns HOW (runtime, schemas, IDs, dispatch).
Templates materialize implementation as concrete files (skill bundle source).
Skill is the deliverable Claude/Codex skill bundle.
Engine is Python that implements implementation's runtime spec.

Each layer is fully determined by what's above. Generate's job is to produce that layer from upstream truth. Reconcile lets the user steer per item.

## The site sibling

Site is downstream of canon but in marketing register. It derives from methodology + implementation (and references manifesto for paradigm framing) but is NOT constrained to cover every concept. Allowed to:

- Simplify language.
- Abbreviate concepts.
- Use illustrative examples instead of formal definitions.
- Order content for narrative flow, not formal taxonomy.

Disallowed:

- Contradicting canon. (If methodology says modes are {vibe, pm, dev, ux, expert}, site can't say {casual, professional}.)
- Introducing concepts not in canon. (If site mentions a "deluxe mode" that doesn't exist in methodology, that's drift — fix one or the other.)
- Visual claims that don't hold (e.g., "5-minute setup" if implementation requires more).

## Authority discipline (per-layer rules)

| Layer | Owns | Doesn't own |
|---|---|---|
| Manifesto | WHY (paradigm, motivation, philosophical claims) | Schemas, file paths, runtime mechanics |
| Intent | CAPs, CSTs, Vision, version-specific direction | How those CAPs are implemented |
| Methodology | WHAT (concepts, operations, modes, governance) | Schemas, file paths, code |
| Implementation | HOW (runtime, schemas, IDs, dispatch, validation) | Marketing language, motivation |
| Templates | Materialization (concrete skill bundle source) | New concepts not in methodology |
| Skill | Deliverable bundle | Anything beyond what implementation specifies |
| Engine | Runtime code | Semantic judgments (those stay with the LLM) |
| Site | Marketing register | New concepts not in canon |

Eval's authority pass flags facts that appear in multiple layers without a clear canonical owner, OR facts owned by the wrong layer (e.g., file paths in methodology — those belong in implementation or file-layout.md).

## Why this matters for `generate`

`generate <layer>` reads ONLY from upstream layers, never from itself or downstream. Examples:

- `generate methodology` reads intent + manifesto. Never reads existing methodology except for structural baseline context. Never reads implementation/skill/site.
- `generate implementation` reads methodology. Never reads existing implementation except for baseline. Never reads intent/manifesto except as cross-reference.
- `generate skill` reads implementation + templates. Mechanical for templates → skill bundle; LLM-driven for engine regen.
- `generate site` reads methodology + implementation (+ manifesto for framing). Never reads existing site except for styling/layout preservation.

Generate from downstream → upstream is FORBIDDEN. If methodology generation needs information that only exists in implementation, that's a layering violation — surface it as a finding.

## Why this matters for `eval`

Eval checks consistency BOTH forward (intent → manifesto → methodology → ...) AND backward (do downstream artifacts reference upstream items that exist? does the site contradict canon?). It is the only operation that reads across layers freely.
