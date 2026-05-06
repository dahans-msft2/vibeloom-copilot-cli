# VibeLoom — Pitch Deck (Source)

**Status:** Pre-seed thesis · May 2026. **VC-independent** — works for any pre-seed audience (EWOR, YC, a16z, Project Europe, AI grants, angel rounds).

This is the **content source** for the pitch deck. The rendered version lives at `v03/pitch-deck.html` (10 slides, 16:9 fixed, brand-coherent with the codæ manifesto). A blank Google Slides file is in Ilya's Drive at *VibeLoom — Pitch Deck — Pre-seed (May 2026)*; populate by uploading `v03/pitch-deck.pptx` (Drive auto-converts).

Hand this Markdown to a designer or paste slide-by-slide into Google Slides / PowerPoint / Pitch.com. Structure follows the YC seed-round 10-slide pattern.

> **Three TODO·Ilya placeholders** before submitting:
> - Slide 9 — founder bio
> - Slide 9 — advisors / pipeline
> - Slide 10 — target raise amount (defaults to `$XXX`; pick per VC conversation)

---

## Slide 1 — Title

**Headline (mark):** VibeLoom

**Tagline:** *The contract layer for agentic engineering.*

**One-liner:** **Code becomes a dark factory. Humans operate one level up.** We build the contract substrate that keeps AI-generated code coherent across cycles — engineering teams approve intent and architecture; agents regenerate code from approved contract; drift is detected before it ships.

**Footer meta:**
- Ilya Baimetov, Founder
- ilya.baimetov@vibeloom.ai
- vibeloom.ai
- May 2026 · v0.3
- Badge: Pre-seed Thesis · May 2026

---

## Slide 2 — Problem

**Headline:** AI is shipping code *faster* than anyone can govern it.

**Subhead:** Engineering teams running multi-agent code-gen in production are paying a measurable tax. Existing tooling — Cursor, Copilot, Spec Kit — optimizes the moment of generation. **The drift between cycles is unsolved.**

**Hero stat (centerpiece):**
- **22.7%** of tracked AI-introduced issues survive at the latest revision — across **302.6K commits** in **6,299 production repos**.
- Source: Liu et al., "AI-debt in the wild" · Mar 2026

**Supporting stats (3 cards):**
1. **3–5×** short-term velocity gain from Cursor — **dissipates in 2 months**, leaving +30% warnings, +41% complexity. *(CMU · MSR 2026)*
2. **17%** lower comprehension scores for AI-assisted developers — **largest decline in debugging**. *(Anthropic · O'Reilly · Apr 2026)*
3. **60% / 0–20%** share of work that uses AI / share of tasks teams can **fully delegate** without supervision. *(Anthropic · Q1 2026)*

---

## Slide 3 — The Bet · Solution

**Headline:** Code becomes a *dark factory.* We build the *contract layer* above it.

**Subhead:** Lights-out coding. Humans approve intent, product, and architecture. Our deterministic engine regenerates code from the approved contract every cycle. Code is machinery, not literature — generated, regenerated, never maintained by hand.

**Before/After visual:**

| Today · The Cursor era | → | Agentic engineering · Dark factory |
|---|---|---|
| **Humans maintain code.** | | **Humans approve contract; factory ships code.** |
| ~100,000 LOC | | ~30 contract items |
| Every cycle, every contributor, every agent. Drift compounds invisibly. 22.7% of issues ship. | | One artifact governs many cycles. Code regenerates deterministically. Drift is detected before ship. |

**Tagline (centered, italic):** Cursor enabled *vibe coding.* VibeLoom enables *agentic engineering* — and the *dark factory* it requires.

---

## Slide 4 — Why now

**Headline:** Four forces converged in the *same six-month window.*

**Subhead:** 2026 is the year the contract layer is both buildable and necessary. None of these conditions held two years ago.

**4 cards (2×2):**

1. **Cursor at $9B proves AI-dev-infra is a real market.** Investors and buyers alike know AI coding tools are infrastructure now, not experiments. The **layer above** Cursor is the next category.
2. **Drift is now measurable, not anecdotal.** SlopCodeBench and "AI-debt in the wild" shipped in March 2026. For the first time, drift, erosion, and surviving defects are quantified across thousands of real repos.
3. **Frontier models cross the deterministic-regen threshold.** Claude Opus 4.7, GPT-5, Gemini 3 are reliable enough that regenerating from approved contracts converges to equivalent output. **Two years ago this didn't work.**
4. **The oversight bottleneck is the new constraint.** Anthropic 2026 Trends Report: developers use AI in **60% of work**, but can fully delegate only **0–20%**. Buyers know they need a governance layer; they don't know what it looks like.

---

## Slide 5 — Product

**Headline:** A methodology, a Skill, and a deterministic engine.

**Subhead:** Ships as a Claude Code / Codex Skill on day one — no install. Methodology is open source (MIT). Engine is pure Python with zero runtime dependencies. Five operating modes from solo hacker to enterprise.

**Left column — 4-step flow:**

```
1 · User edits intent.md + approves
    capabilities, constraints in plain English; approval trace recorded
        ↓
2 · Engine regenerates downstream
    product specs · UX · architecture · code · BDD scenarios
        ↓
3 · Eval ladder runs each cycle
    decidable structural · mechanical runners · heuristic semantic
        ↓
4 · Code ships; code-sync trace closes the loop
    every code path traces back to its contract item
```

**Right column — Five modes:**

| Mode | Description |
|---|---|
| `vibe` | **Solo.** Compact stack. No graph. One-way upgrade to full mode when you outgrow it. |
| `pm` | **Product-led.** PM owns intent + product specs. |
| `dev` | **Tech-led.** Dev owns intent + system specs. |
| `ux` | **Design-led.** Designer owns intent + UX. Mockups drive product specs. |
| `expert` | **Regulated.** Every approval gate explicit. Compliance-ready. |

**Footer:** Open source: methodology, Skill, templates. Paid: hosted engine, audit, compliance, advisor seat.

---

## Slide 6 — Insight (Why we win)

**Headline:** Cursor solves *generation.* We solve *coherence between generations.*

**Subhead:** Every existing tool optimizes the moment of code production. The drift problem is structural: it happens between cycles. Solving it requires a different abstraction layer — and a different buyer.

**Left — The non-obvious bet (italic callout):**
> We are **not in the same fight as Cursor**. Cursor sells productivity to individual developers. We sell **governance** to engineering leaders — at a different layer of the stack, to a different buyer, with a different metric (drift caught vs. lines shipped).

**Right — Where the value chain sits:**

| Layer | What it does |
|---|---|
| **Cursor / Copilot / Codeium** | Vibe coding — chat-driven, in the IDE. Optimizes per-edit velocity. |
| **Kiro / Spec Kit / BMAD** | Spec-driven — per-feature specs feed agent generation. Specs decay between features. |
| **VibeLoom** *(us)* | Contract-driven — system-level contracts govern many cycles. Drift detected at the contract layer, not in code. |

---

## Slide 7 — Business model

**Headline:** Open-source pull. *Tiered SaaS* capture.

**Subhead:** Methodology + Skill open under MIT pulls developers in (PLG flywheel; Cursor's pattern). Paid tiers capture engineering teams that need audit, telemetry, compliance, and on-prem.

**3 tiers:**

| Free | **Team · Recommended** | Enterprise |
|---|---|---|
| **$0** · MIT | **$30** / seat / month | **$50K+** / year |
| Solo developers, OSS, hobbyists | Engineering teams of 5–50 | Mid-market & enterprise (50+ eng) |
| → vibe + pm modes | → Full pm / dev / ux modes | → expert mode + compliance |
| → Methodology + Skill | → Hosted engine | → On-prem engine |
| → Self-hosted engine | → Audit logs + drift telemetry | → SOC2 / HIPAA bundles |
| → 100 generations / month | → Unlimited generations | → Advisor seat (founder access) |
| | → Standard SLA | → SSO + audit-trail export |

**GTM:** land via individual devs (free Skill, Discord, GitHub). Expand to teams when drift becomes a P1 (after first reconciliation crisis). Enterprise via design-partner referrals after 6 months of dogfood telemetry.

---

## Slide 8 — Market

**Headline:** $2.2B SAM at saturation. *Cursor's $9B* is the proof.

**Subhead:** If Cursor's run-rate proves the demand for AI dev infrastructure, the contract layer above it is the natural follow-on category — sold to a different buyer (CTO/VPE) at a different ACV (per-team, not per-seat).

**Bottom-up SAM (transparent calc):**

| | |
|---|---:|
| Developers worldwide *(Stack Overflow Dev Survey 2025)* | ~30M |
| Using AI coding tools (33%) *(JetBrains 2025; GitHub Octoverse 2025)* | ~10M |
| Running multi-cycle agentic generation (30% of those) *— the cohort that hits the drift problem* | ~3M |
| Avg seat ACV (mid-tier B2B SaaS) | $720 / yr |
| **SAM at saturation** | **$2.2B** |

**Narrative (right column):**
- **A new category in AI dev infrastructure.** Cursor's $9B revenue/valuation is the headline; Copilot, Codeium, Tabnine, Replit fill out the field. None of them sells to the buyer we sell to — the engineering leader responsible for codebase coherence over time.
- **Adjacent expansion: $5B+.** Methodology consulting, contract pattern marketplaces, audit + compliance bundles, training. Each unlocked once trace-derived learning is shipping (year 2).

---

## Slide 9 — Team

**Headline:** Solo founder today. *Team-of-2* by month six.

**Subhead:** VCs commonly flag solo founders. The concern is fair. We treat co-founder acquisition as a tracked Q1 milestone — not glossed over. The methodology, spec, and engine shipped solo are themselves the artifact that recruits the right co-founder.

**Bio block — Ilya Baimetov, Founder · Author of codæ & VibeLoom:**

- **Background.** *[TODO · Ilya]* Prior roles, technical depth, shipped products. EWOR weights this heavily — fill before submission.
- **Why me.** Authored the codæ paradigm and the v0.3 VibeLoom spec end-to-end: methodology, implementation, comparison whitepaper, 35 generation-ready templates, marketing site, examples. Built daily with frontier agents through 2025–2026; saw the slop pattern emerge in real codebases.
- **Insight.** Cursor proved chat-driven coding works at scale. The next layer is making the contract — not the chat — the durable surface humans operate on. **Build the layer above.**

**Solo-acknowledge callout:**
> **Q1 milestone, tracked:** technical co-founder onboarded by month 6. Profile: distributed-systems / dev-infra / ex-platform-engineering. The pre-seed round itself is the team-formation forcing function — not a workaround.

**Advisors & pipeline block:**
- *[TODO · Ilya]* Named advisor list (or "advisory list in formation, X conversations active"). Plus: design-partner pipeline of N teams currently scoping pilots.

---

## Slide 10 — Ask

**Headline:** Pre-seed: *$XXX* for 18 months of runway. *[TODO · Ilya: target $]*

**Subhead:** Build the contract layer for the agentic era. Engine v0.4 → first 10 design partners → drift telemetry → Series A traction. Solo today; team-of-2 by month six.

**Left card — Use of funds, 18 months (primary, red-tinted):**
- → **Engineering — 55%** · technical co-founder + 2 senior engineers (engine, infra)
- → **Design partners — 25%** · dedicated success + onboarding + drift-telemetry tooling
- → **Legal / IP / compliance — 10%** · entity, IP assignments, SOC2 prep
- → **Buffer + ops — 10%** · cloud, tooling, contingency

**Right card — Milestones to Series A:**
- → **Month 3** · Engine v0.4 dogfood-ready (spec → runnable Python)
- → **Month 6** · Technical co-founder onboarded + 5 design partners shipping
- → **Month 12** · First paying teams + drift telemetry across 10+ codebases
- → **Month 18** · Series A on the back of trace-derived learning evidence

**Closer (dark band):**
> Cursor enabled *vibe coding.*
> VibeLoom enables *agentic engineering* — and the *dark factory* it requires.

**Contact:**
- **Ilya Baimetov**
- ilya.baimetov@vibeloom.ai
- vibeloom.ai · github.com/ilya-baimetov/vibeloom

> **Note for the presenter:** target raise dollar amount (`$XXX`) is intentionally a placeholder — pick per VC conversation. Common pre-seed bands for solo deeptech AI infra in 2026: **$500K (lean US/EU pre-seed)** to **$1M (priced round w/ runway buffer)**.

---

## Notes for the designer / presenter

- **Brand:** Inter (sans, body), JetBrains Mono (code/labels/numbers in mono), Fraunces (italic serif for accents and big numbers). Signature red `#e84057`. Background `#ffffff` with `#f7f7f6` soft cards.
- **Type rules:** headlines bold sans, italic-serif accent words for emphasis (e.g., *faster*, *up*, *Ideation Fellowship*). Big numbers always italic Fraunces.
- **Slides:** 16:9 fixed aspect (1280×720 reference), one idea per slide, headlines tell the story alone.
- **Print-to-PDF:** the HTML at `v03/pitch-deck.html` already prints to a clean 10-page 13.333"×7.5" PDF.
- **Stat sources:** all stats trace to the canonical manifesto's references (refs 3, 5, 7, 10, 13 in `v03/codæ-manifesto.html`). No invented numbers.
