# VibeLoom — Pitch Deck (Source)

**Status:** Pre-seed thesis · May 2026. **VC-independent** — works for any pre-seed audience (EWOR, YC, a16z, Project Europe, AI grants, angel rounds).

This is the **content source** for the pitch deck. The shippable artifact is `v03/pitch-deck.pptx` (16:9, 10 slides, brand-coherent, opens in PowerPoint / Google Slides / Keynote). A blank companion Google Slides file is in Ilya's Drive at *VibeLoom — Pitch Deck — Pre-seed (May 2026)* — populate by uploading the .pptx (Drive auto-converts).

Reproducible: `node v03/build-pitch-deck.js` → regenerates the .pptx from the source content here.

> **Two TODO·Ilya placeholders** before submitting:
> - Slide 9 — *Background:* prior roles, technical depth, shipped products
> - Slide 9 — *Advisors:* named advisor list or design-partner pipeline
> - Slide 10 — *target raise dollar amount* (the deck shows `$XXX`; pick per VC conversation; common pre-seed bands for solo deeptech AI infra in 2026: $500K lean → $1M priced)

---

## Design system

- Inter (sans), JetBrains Mono (mono), Fraunces (italic serif)
- Signature red `#e84057`; ink `#0a0a0a`; white background; dark `#0a0a0a` backgrounds for title + ask slides ("dark sandwich")
- One visual centerpiece per slide, headlines 3–8 words, body 14–16pt
- The "dark factory" framing is loud: appears on slide 1 (title), slide 3 (the bet), and slide 10 (ask) — bookending the deck

---

## Slide 1 — Title  *(dark background)*

**Mark:** Vibe**Loom** (top-left, small)
**Badge:** PRE-SEED · MAY 2026 (top-right, mono)

**HEADLINE (huge italic-serif red, single line):**
> *Code becomes a dark factory.*

**Sub-thesis (bold sans white):**
> We build the contract layer above it.

**Pairing line (small):**
> Cursor enabled *vibe coding.*       VibeLoom enables *agentic engineering.*

**Footer:** Ilya Baimetov, Founder · ilya.baimetov@vibeloom.ai · vibeloom.ai · v0.3

---

## Slide 2 — Problem

**Headline:** AI ships slop.

**Sub:** Multi-agent code-gen in production: drift compounds, defects survive, velocity gains evaporate. Existing tooling optimizes the moment of generation; nothing governs what happens between cycles.

**Hero stat:**
> **22.7%** — of tracked AI-introduced issues survive at the latest revision. *302.6K commits across 6,299 production repos.*
> — Liu et al., "AI-debt in the wild" · arXiv:2603.28592 · Mar 2026

**Supporting row (3 stats):**
- **3–5×** — velocity gain dissipates after 2 months · *CMU · MSR 2026*
- **+30% / +41%** — warnings / complexity post-Cursor · *CMU · MSR 2026*
- **17%** — drop in comprehension on AI work · *Anthropic · O'Reilly · Apr 2026*

---

## Slide 3 — The Bet

**Headline:** Lights out for code.

**Sub:** Code is generated, regenerated, never maintained by hand. Humans operate one level up — at the contract.

**Before/After visual:**

| TODAY · The Cursor era | → | DARK FACTORY |
|---|---|---|
| **Humans maintain code.** | | **Factory ships code.** |
| ~100,000 LOC | | ~30 contract items |
| Reviewed every cycle. Drift compounds invisibly. | | Approved once. Code regenerates. Drift detected before ship. |

**Tagline:** Cursor *vibe coding*. VibeLoom *agentic engineering* — and the *dark factory* it requires.

---

## Slide 4 — Product

**Headline:** The contract layer.

**Sub:** Methodology + Skill + deterministic engine. Ships as a Claude Code / Codex Skill. Open source under MIT.

**4-step horizontal flow:**

1. `intent.md` — User edits intent + approves
2. `regenerate` — Engine produces architecture, code, tests
3. `eval` — Decidable + mechanical + heuristic checks
4. `ship` — Code-sync trace closes the loop

**Five modes (single line):** `vibe` (solo) · `pm` (product) · `dev` (tech) · `ux` (design) · `expert` (regulated)

**Footer:** Open source: methodology, Skill, templates. Paid: hosted engine, audit, compliance.

---

## Slide 5 — Why now

**Headline (stacked, 2 lines):**
> Four forces.
> *Same six months.*

**Sub:** None of these conditions held two years ago. All four crossed their threshold in Q1 2026.

**2x2 grid:**

| **$9B** | **Mar '26** |
|---|---|
| Cursor proves AI-dev-infra is a real market. The layer above is the next category. | SlopCodeBench + AI-debt papers shipped. Drift quantified for the first time. |

| **GPT-5** | **60% / 0–20%** |
|---|---|
| Frontier models finally reliable for deterministic regen. Same prompt, same output, every cycle. | Devs use AI in 60% of work; can fully delegate 0–20%. Governance is the new bottleneck. |

---

## Slide 6 — Insight

**Headline:** Not Cursor's fight.

**Sub:** Cursor sells productivity to individual developers. We sell governance to engineering leaders. Different layer, different buyer, different metric.

**3-row value chain:**

| Cursor / Copilot / Codeium | Vibe coding — chat-driven, in the IDE. Per-edit velocity. |
| Kiro / Spec Kit / BMAD | Spec-driven — per-feature specs. Decay between features. |
| **VibeLoom** *(highlighted, red)* | Contract-driven — system-level contracts govern many cycles. Drift detected at the contract layer. |

**Italic kicker:** *We are not in the same fight as Cursor. We win by being one abstraction level up.*

---

## Slide 7 — Business model

**Headline:** Open core. Tiered SaaS.

**Sub:** MIT-licensed methodology + Skill pulls developers in (PLG, Cursor's pattern). Paid tiers capture engineering teams that need audit, telemetry, compliance.

**3 pricing tiers:**

| Free | **Team · Recommended** | Enterprise |
|---|---|---|
| **$0** · MIT-licensed | **$30** / seat / month | **$50K+** / year |
| Solo devs, OSS, hobbyists | Engineering teams of 5–50 | Mid-market & enterprise (50+ eng) |
| → vibe + pm modes | → Full pm / dev / ux modes | → expert mode + compliance |
| → Methodology + Skill | → Hosted engine | → On-prem engine |
| → Self-hosted engine | → Audit logs + drift telemetry | → SOC2 / HIPAA bundles |
| → 100 generations / mo | → Unlimited generations | → Founder advisor seat |

**GTM (italic):** *Land via individual devs (free Skill, Discord, GitHub). Expand to teams when drift becomes a P1.*

---

## Slide 8 — Market

**Headline (stacked, 2 lines):**
> $2.2B SAM.
> *Cursor proves it.*

**Sub:** Cursor at $9B revenue/valuation proves AI-dev-infra is a real market. We sell the layer above it — to a different buyer, at a different ACV (per-team, not per-seat).

**Funnel calc (left column):**

| | |
|---|---:|
| Developers worldwide *(Stack Overflow Dev Survey 2025)* | 30M |
| Using AI coding tools (~33%) *(JetBrains 2025; GitHub Octoverse)* | 10M |
| Multi-cycle agentic generation (~30% of those) — the cohort that hits drift | 3M |
| × $720 / yr (mid-tier B2B SaaS) | $720 |
| **SAM at saturation** | **$2.2B** |

**Right callout (huge italic-serif red):** *$2.2B* at saturation, B2B SaaS only

**Adjacent:** + $5B adjacent — methodology consulting, contract pattern marketplaces, audit + compliance bundles, training.

---

## Slide 9 — Team

**Headline (stacked, 2 lines):**
> Solo today.
> *Two by month six.*

**Sub:** VCs commonly flag solo founders. The concern is fair. Q1 milestone: technical co-founder onboarded — distributed-systems / dev-infra background — by month 6.

**Bio card (left):**
- **Ilya Baimetov** — FOUNDER · AUTHOR OF CODÆ + VIBELOOM
- **Background.** *[Add prior roles + technical depth here.]*
- **Why me.** Authored the codæ paradigm + v0.3 spec end-to-end (methodology, implementation, comparison whitepaper, 35 templates, marketing site). Built daily with frontier agents through 2025–2026; saw the slop pattern emerge in production.
- **Insight.** The next layer is making the contract — not the chat — the durable surface humans operate on.

**Tracked-milestone card (right, red-tinted):**
- CO-FOUNDER ACQUISITION — TRACKED MILESTONE
- **By month 6.** *(huge italic-serif red)*
- Profile: distributed-systems / dev-infra / ex-platform-engineering. The pre-seed round itself is the team-formation forcing function — not a workaround.
- **Advisors.** *[Add named advisor list or design-partner pipeline here.]*

---

## Slide 10 — Ask  *(dark background)*

**Headline (stacked, 2 lines, huge):**
> *$XXX.*  18 months.
> Ship the *dark factory.*

**Sub:** Engine v0.4 → 10 design partners → drift telemetry → Series A traction.

**Use of funds (left card, red-bordered):**
- **55% Engineering** — co-founder + 2 senior eng
- **25% Design partners** — success + onboarding + telemetry
- **10% Legal / IP / compliance** — entity, IP, SOC2 prep
- **10% Buffer + ops**

**Milestones to Series A (right card):**
- **Mo 3** — Engine v0.4 dogfood-ready
- **Mo 6** — Co-founder + 5 design partners shipping
- **Mo 12** — First paying teams + drift telemetry, 10+ codebases
- **Mo 18** — Series A on trace-derived learning evidence

**Footer:** Ilya Baimetov · ilya.baimetov@vibeloom.ai · vibeloom.ai · github.com/ilya-baimetov/vibeloom

---

## Notes for the presenter

- **Dark factory bookends.** Slide 1 opens with "Code becomes a dark factory." Slide 10 closes with "Ship the dark factory." Slide 3 carries it through the middle. Three loud mentions.
- **Print-to-PDF:** open the .pptx in PowerPoint / Slides / Keynote and File → Export → PDF.
- **Stat sources:** all numbers trace to the canonical manifesto's references (refs 3, 5, 7, 10, 13 in `v03/codæ-manifesto.html`). No invented stats.
- **Not in this deck (intentionally):** financial projections, detailed cap table, exit scenarios. These come at the term-sheet stage if the conversation gets that far.
