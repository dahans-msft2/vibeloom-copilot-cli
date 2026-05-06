/**
 * VibeLoom pitch deck — VC-format rebuild.
 *
 * Output: v03/pitch-deck.pptx (16:9, 13.333" x 7.5")
 *
 * Design rules (per the pptx skill):
 *   - 3–8 word headlines
 *   - One visual centerpiece per slide
 *   - "Sandwich": dark slide 1 (title) + dark slide 10 (ask), light in between
 *   - No accent lines under titles, no decorative full-width colored bars
 *   - 60–72pt big-stat callouts
 *   - 0.5" margins minimum
 *
 * Brand:
 *   - Inter (sans), JetBrains Mono (mono), Fraunces (italic serif)
 *   - Signature red #e84057, ink #0a0a0a, white #ffffff
 */

const pptxgen = require("pptxgenjs");

// === brand tokens ============================================================
const C = {
  bg:        "FFFFFF",
  bgSoft:    "F7F7F6",
  bgMute:    "EFEEEC",
  ink:       "0A0A0A",
  ink2:      "1A1A1A",
  ink3:      "3A3A3A",
  ink4:      "5A5A5A",
  ink5:      "707070",
  line:      "E6E4E0",
  line2:     "D6D3CD",
  red:       "E84057",
  redDeep:   "C43A50",
  redSoft:   "FBE6EA",
  white:     "FFFFFF",
  inkOnDark: "F0EEEA",
  whiteSoft: "D6D3CD",
};

const F = {
  sans:  "Inter",
  mono:  "JetBrains Mono",
  serif: "Fraunces",
};

// === setup ===================================================================
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";        // 13.333" x 7.5"
pres.author = "Ilya Baimetov";
pres.title = "VibeLoom — Pitch Deck (Pre-seed, May 2026)";

const W = 13.333, H = 7.5;
const MX = 0.65;                    // x-margin

// =============================================================================
// SLIDE 1 — TITLE (DARK)
// "Code becomes a dark factory." — front and center, huge, italic-serif red
// =============================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.ink };

  // Top-left mark
  s.addText([
    { text: "Vibe", options: { color: C.white, bold: true, fontFace: F.sans } },
    { text: "Loom", options: { color: C.red, bold: true, fontFace: F.sans } },
  ], {
    x: MX, y: 0.45, w: 4, h: 0.5,
    fontSize: 18, charSpacing: -1, margin: 0,
  });

  // Top-right badge text (no decorative pill — just mono)
  s.addText("PRE-SEED · MAY 2026", {
    x: W - MX - 4, y: 0.5, w: 4, h: 0.4,
    fontSize: 9, fontFace: F.mono, bold: true,
    color: C.whiteSoft, align: "right", margin: 0, charSpacing: 1,
  });

  // THE HEADLINE — huge italic Fraunces in red, single line, sized to fit width
  s.addText("Coding becomes a dark factory.", {
    x: MX, y: 2.5, w: W - 2 * MX, h: 1.6,
    fontSize: 60, fontFace: F.serif, italic: true, bold: true,
    color: C.red, align: "left", valign: "top", margin: 0,
    charSpacing: -2,
  });

  // Sub-thesis below — bold sans white, clear separation
  s.addText("We build the contract layer above it.", {
    x: MX, y: 4.3, w: W - 2 * MX, h: 0.7,
    fontSize: 32, fontFace: F.sans, bold: true,
    color: C.white, align: "left", margin: 0,
    charSpacing: -0.5,
  });

  // Pairing line — Cursor / VibeLoom (extra spacing between phrases)
  s.addText([
    { text: "Cursor enabled ", options: { color: C.whiteSoft, fontFace: F.sans } },
    { text: "vibe coding.", options: { color: C.red, fontFace: F.serif, italic: true } },
    { text: "       VibeLoom enables ", options: { color: C.whiteSoft, fontFace: F.sans } },
    { text: "agentic engineering.", options: { color: C.red, fontFace: F.serif, italic: true } },
  ], {
    x: MX, y: 5.3, w: W - 2 * MX, h: 0.55,
    fontSize: 18, margin: 0, charSpacing: -0.2,
  });

  // Bottom contact row (mono, muted)
  s.addText([
    { text: "Ilya Baimetov, Founder", options: { color: C.white, bold: true } },
    { text: "      ilya.baimetov@vibeloom.ai      vibeloom.ai      v0.3", options: { color: C.whiteSoft } },
  ], {
    x: MX, y: H - 0.95, w: W - 2 * MX, h: 0.4,
    fontSize: 11, fontFace: F.mono, margin: 0, charSpacing: 0.4,
  });
}

// =============================================================================
// SLIDE 2 — PROBLEM
// "AI ships slop." + ONE huge stat
// =============================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  // slide num + section name
  s.addText("02 / 10", {
    x: MX, y: 0.45, w: 2, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  s.addText("PROBLEM", {
    x: W - MX - 4, y: 0.45, w: 4, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.ink5, align: "right", charSpacing: 1, margin: 0,
  });

  // Headline — 3 words
  s.addText("AI ships slop.", {
    x: MX, y: 1.0, w: W - 2 * MX, h: 1.1,
    fontSize: 64, fontFace: F.sans, bold: true,
    color: C.ink, charSpacing: -2, margin: 0,
  });

  // One sub-line
  s.addText("Multi-agent code-gen in production: drift compounds, defects survive, velocity gains evaporate. Existing tooling optimizes the moment of generation; nothing governs what happens between cycles.", {
    x: MX, y: 2.25, w: W - 2 * MX, h: 0.85,
    fontSize: 16, fontFace: F.sans, color: C.ink3, margin: 0,
  });

  // BIG stat — 22.7% (sized to fit; pptxgenjs needs more height than text height)
  s.addText("22.7%", {
    x: MX, y: 3.3, w: 5.0, h: 2.6,
    fontSize: 130, fontFace: F.serif, italic: true, bold: true,
    color: C.red, align: "left", valign: "top", margin: 0, charSpacing: -4,
  });

  s.addText([
    { text: "of tracked AI-introduced issues survive at the latest revision.", options: { bold: true, color: C.ink } },
    { text: "\n\n302.6K commits across 6,299 production repos.", options: { color: C.ink3 } },
  ], {
    x: 5.8, y: 3.7, w: W - MX - 5.8, h: 1.7,
    fontSize: 17, fontFace: F.sans, valign: "top", margin: 0,
  });

  s.addText("LIU ET AL., \"AI-DEBT IN THE WILD\" · arXiv:2603.28592 · MAR 2026", {
    x: 5.8, y: 5.45, w: W - MX - 5.8, h: 0.3,
    fontSize: 9, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });

  // Three small supporting stats — single row, bottom (kept inside slide bounds)
  const supY = 6.1;
  const supW = (W - 2 * MX - 0.6) / 3;
  const sup = [
    ["3–5×", "velocity gain dissipates after 2 months", "CMU · MSR 2026"],
    ["+30% / +41%", "warnings / complexity post-Cursor", "CMU · MSR 2026"],
    ["17%", "drop in comprehension on AI work", "Anthropic · O'Reilly"],
  ];
  sup.forEach(([num, label, src], i) => {
    const sx = MX + i * (supW + 0.3);
    s.addText(num, {
      x: sx, y: supY, w: supW, h: 0.45,
      fontSize: 22, fontFace: F.serif, italic: true, bold: true,
      color: C.ink, margin: 0,
    });
    s.addText([
      { text: label, options: { color: C.ink3 } },
      { text: "\n" + src, options: { color: C.ink5, fontFace: F.mono, fontSize: 8 } },
    ], {
      x: sx, y: supY + 0.5, w: supW, h: 0.7,
      fontSize: 11, fontFace: F.sans, margin: 0,
    });
  });
}

// =============================================================================
// SLIDE 3 — INSIGHT (the dark factory bet)
// "Lights out for code." — the bet, with before/after visual
// =============================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  s.addText("03 / 10", {
    x: MX, y: 0.45, w: 2, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  s.addText("SOLUTION · THE BET", {
    x: W - MX - 4, y: 0.45, w: 4, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.ink5, align: "right", charSpacing: 1, margin: 0,
  });

  // Headline — 4 words
  s.addText("Lights out for coding.", {
    x: MX, y: 1.0, w: W - 2 * MX, h: 1.1,
    fontSize: 64, fontFace: F.sans, bold: true,
    color: C.ink, charSpacing: -2, margin: 0,
  });

  // One subline
  s.addText("Code is generated, regenerated, never maintained by hand. Humans operate one level up — at the contract.", {
    x: MX, y: 2.25, w: W - 2 * MX, h: 0.7,
    fontSize: 16, fontFace: F.sans, color: C.ink3, margin: 0,
  });

  // Before / Arrow / After cards
  const cy = 3.3, ch = 3.0;
  const cw = (W - 2 * MX - 0.8) / 2;

  // BEFORE — gray card
  s.addShape(pres.shapes.RECTANGLE, {
    x: MX, y: cy, w: cw, h: ch,
    fill: { color: C.bgSoft }, line: { color: C.line, width: 0.75 },
  });
  s.addText("TODAY · THE CURSOR ERA", {
    x: MX + 0.35, y: cy + 0.3, w: cw - 0.7, h: 0.3,
    fontSize: 10, fontFace: F.mono, bold: true,
    color: C.ink4, charSpacing: 1, margin: 0,
  });
  s.addText("Humans maintain code.", {
    x: MX + 0.35, y: cy + 0.7, w: cw - 0.7, h: 0.5,
    fontSize: 24, fontFace: F.sans, bold: true,
    color: C.ink, margin: 0,
  });
  s.addText("~100,000 LOC", {
    x: MX + 0.35, y: cy + 1.4, w: cw - 0.7, h: 0.7,
    fontSize: 36, fontFace: F.serif, italic: true, bold: true,
    color: C.ink3, margin: 0, charSpacing: -1,
  });
  s.addText("Reviewed, every cycle, every contributor. Drift compounds invisibly.", {
    x: MX + 0.35, y: cy + 2.3, w: cw - 0.7, h: 0.55,
    fontSize: 13, fontFace: F.sans, color: C.ink3, margin: 0,
  });

  // ARROW
  const ax = MX + cw + 0.05;
  s.addText("→", {
    x: ax, y: cy + 1.1, w: 0.7, h: 0.7,
    fontSize: 44, fontFace: F.serif, italic: true, bold: true,
    color: C.red, align: "center", margin: 0,
  });

  // AFTER — red-tinted card with red left bar
  const bx = MX + cw + 0.8;
  s.addShape(pres.shapes.RECTANGLE, {
    x: bx, y: cy, w: cw, h: ch,
    fill: { color: C.redSoft }, line: { color: C.red, width: 0.75 },
  });
  // left accent bar (RECTANGLE not ROUNDED_RECTANGLE — skill warning)
  s.addShape(pres.shapes.RECTANGLE, {
    x: bx, y: cy, w: 0.04, h: ch,
    fill: { color: C.red }, line: { type: "none" },
  });
  s.addText("DARK FACTORY", {
    x: bx + 0.35, y: cy + 0.3, w: cw - 0.7, h: 0.3,
    fontSize: 10, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  s.addText("Factory ships code.", {
    x: bx + 0.35, y: cy + 0.7, w: cw - 0.7, h: 0.5,
    fontSize: 24, fontFace: F.sans, bold: true,
    color: C.ink, margin: 0,
  });
  s.addText("~30 contract items", {
    x: bx + 0.35, y: cy + 1.4, w: cw - 0.7, h: 0.7,
    fontSize: 36, fontFace: F.serif, italic: true, bold: true,
    color: C.red, margin: 0, charSpacing: -1,
  });
  s.addText("Approved once. Code regenerates deterministically. Drift detected before ship.", {
    x: bx + 0.35, y: cy + 2.3, w: cw - 0.7, h: 0.55,
    fontSize: 13, fontFace: F.sans, color: C.ink2, margin: 0,
  });

  // Bottom tagline (small, italic)
  s.addText([
    { text: "Cursor ", options: { color: C.ink3 } },
    { text: "vibe coding", options: { color: C.red, italic: true, fontFace: F.serif } },
    { text: ".  VibeLoom ", options: { color: C.ink3 } },
    { text: "agentic engineering", options: { color: C.red, italic: true, fontFace: F.serif } },
    { text: " — and the ", options: { color: C.ink3 } },
    { text: "dark factory", options: { color: C.red, italic: true, fontFace: F.serif } },
    { text: " it requires.", options: { color: C.ink3 } },
  ], {
    x: MX, y: cy + ch + 0.2, w: W - 2 * MX, h: 0.4,
    fontSize: 16, fontFace: F.sans, align: "center", margin: 0,
  });
}

// =============================================================================
// SLIDE 4 — WHY NOW
// "Four forces. Same six months."
// =============================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  s.addText("04 / 10", {
    x: MX, y: 0.45, w: 2, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  s.addText("WHY NOW", {
    x: W - MX - 4, y: 0.45, w: 4, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.ink5, align: "right", charSpacing: 1, margin: 0,
  });

  s.addText([
    { text: "Four forces.", options: { color: C.ink, bold: true, fontFace: F.sans, breakLine: true } },
    { text: "Same six months.", options: { color: C.red, italic: true, bold: true, fontFace: F.serif } },
  ], {
    x: MX, y: 0.95, w: W - 2 * MX, h: 1.95,
    fontSize: 56, charSpacing: -2, margin: 0, valign: "top",
  });

  s.addText("None of these conditions held two years ago. All four crossed their threshold in Q1 2026.", {
    x: MX, y: 3.05, w: W - 2 * MX, h: 0.6,
    fontSize: 16, fontFace: F.sans, color: C.ink3, margin: 0,
  });

  // 2x2 grid of forces — each with a big number + 2-line takeaway
  const gy = 3.85, gh = 1.55, gap = 0.25;
  const gw = (W - 2 * MX - gap) / 2;
  const forces = [
    ["$9B", "Cursor proves AI-dev-infra is a real market.\nThe layer above is the next category."],
    ["Mar '26", "SlopCodeBench + AI-debt papers shipped.\nDrift quantified for the first time."],
    ["GPT-5", "Frontier models finally reliable for deterministic regen.\nSame prompt, same output, every cycle."],
    ["60% / 0–20%", "Devs use AI in 60% of work; can fully delegate 0–20%.\nGovernance is the new bottleneck."],
  ];
  forces.forEach(([num, txt], i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const cx = MX + col * (gw + gap);
    const cy = gy + row * (gh + gap);
    s.addShape(pres.shapes.RECTANGLE, {
      x: cx, y: cy, w: gw, h: gh,
      fill: { color: C.bg }, line: { color: C.line, width: 0.75 },
    });
    s.addText(num, {
      x: cx + 0.3, y: cy + 0.2, w: 4, h: 0.65,
      fontSize: 26, fontFace: F.serif, italic: true, bold: true,
      color: C.red, margin: 0, charSpacing: -1,
    });
    s.addText(txt, {
      x: cx + 0.3, y: cy + 0.8, w: gw - 0.6, h: 0.7,
      fontSize: 12, fontFace: F.sans, color: C.ink2, margin: 0,
    });
  });
}

// =============================================================================
// SLIDE 5 — MARKET
// "$2.2B SAM." with funnel calc
// =============================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  s.addText("05 / 10", {
    x: MX, y: 0.45, w: 2, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  s.addText("MARKET", {
    x: W - MX - 4, y: 0.45, w: 4, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.ink5, align: "right", charSpacing: 1, margin: 0,
  });

  s.addText([
    { text: "$2.2B SAM.", options: { color: C.ink, bold: true, fontFace: F.sans, breakLine: true } },
    { text: "Cursor proves it.", options: { color: C.red, italic: true, bold: true, fontFace: F.serif } },
  ], {
    x: MX, y: 0.95, w: W - 2 * MX, h: 1.95,
    fontSize: 56, charSpacing: -2, margin: 0, valign: "top",
  });

  s.addText("Cursor at $9B revenue/valuation proves AI-dev-infra is a real market. We sell the layer above it — to a different buyer, at a different ACV (per-team, not per-seat).", {
    x: MX, y: 3.05, w: W - 2 * MX, h: 0.85,
    fontSize: 15, fontFace: F.sans, color: C.ink3, margin: 0,
  });

  // Funnel-style left, big number right
  const fy = 4.05;
  const funnel = [
    ["Developers worldwide",                  "30M",   "Stack Overflow Dev Survey 2025"],
    ["Using AI coding tools (~33%)",          "10M",   "JetBrains 2025; GitHub Octoverse"],
    ["Multi-cycle agentic generation (~30%)", "3M",    "the cohort that hits drift"],
    ["× $720 / yr (mid-tier B2B SaaS)",       "$720",  ""],
  ];
  funnel.forEach(([label, num, src], i) => {
    const ry = fy + i * 0.55;
    s.addText(label, {
      x: MX, y: ry, w: 6.5, h: 0.4,
      fontSize: 14, fontFace: F.sans, color: C.ink2, margin: 0,
    });
    if (src) {
      s.addText(src, {
        x: MX, y: ry + 0.32, w: 6.5, h: 0.2,
        fontSize: 9, fontFace: F.mono, color: C.ink5, margin: 0,
      });
    }
    s.addText(num, {
      x: 6.8, y: ry, w: 1.5, h: 0.4,
      fontSize: 20, fontFace: F.mono, bold: true,
      color: C.ink, align: "right", margin: 0,
    });
  });

  // SAM total at bottom of funnel — red bar accent
  s.addShape(pres.shapes.LINE, {
    x: MX, y: fy + 2.35, w: 7.65, h: 0,
    line: { color: C.red, width: 2 },
  });
  s.addText("SAM at saturation", {
    x: MX, y: fy + 2.45, w: 6.5, h: 0.5,
    fontSize: 16, fontFace: F.sans, bold: true, color: C.ink, margin: 0,
  });
  s.addText("$2.2B", {
    x: 6.8, y: fy + 2.4, w: 1.5, h: 0.6,
    fontSize: 28, fontFace: F.serif, italic: true, bold: true,
    color: C.red, align: "right", margin: 0, charSpacing: -1,
  });

  // Right side: BIG callout
  s.addText("$2.2B", {
    x: 9.0, y: fy, w: W - MX - 9.0, h: 1.3,
    fontSize: 88, fontFace: F.serif, italic: true, bold: true,
    color: C.red, align: "left", margin: 0, charSpacing: -3,
  });
  s.addText("at saturation, B2B SaaS only", {
    x: 9.0, y: fy + 1.35, w: W - MX - 9.0, h: 0.35,
    fontSize: 12, fontFace: F.mono, color: C.ink5, margin: 0,
  });
  s.addText([
    { text: "+ $5B adjacent: ", options: { bold: true, color: C.ink } },
    { text: "methodology consulting, contract pattern marketplaces, audit + compliance bundles, training.", options: { color: C.ink3 } },
  ], {
    x: 9.0, y: fy + 1.85, w: W - MX - 9.0, h: 1.3,
    fontSize: 12, fontFace: F.sans, margin: 0,
  });
}

// =============================================================================
// SLIDE 6 — INSIGHT (why we win)
// "Not Cursor's fight." — the value-chain wedge
// =============================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  s.addText("06 / 10", {
    x: MX, y: 0.45, w: 2, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  s.addText("COMPETITION", {
    x: W - MX - 4, y: 0.45, w: 4, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.ink5, align: "right", charSpacing: 1, margin: 0,
  });

  s.addText("Not Cursor's fight.", {
    x: MX, y: 1.0, w: W - 2 * MX, h: 1.1,
    fontSize: 64, fontFace: F.sans, bold: true,
    color: C.ink, charSpacing: -2, margin: 0,
  });

  s.addText("Cursor sells productivity to individual developers. We sell governance to engineering leaders. Different layer, different buyer, different metric.", {
    x: MX, y: 2.25, w: W - 2 * MX, h: 0.7,
    fontSize: 16, fontFace: F.sans, color: C.ink3, margin: 0,
  });

  // 3 horizontal layer rows — value chain (compressed to leave room for kicker)
  const ry = 3.25, rh = 0.9, rgap = 0.15;
  const rows = [
    ["Cursor / Copilot / Codeium", "Vibe coding — chat-driven, in the IDE. Per-edit velocity.", false],
    ["Kiro / Spec Kit / BMAD", "Spec-driven — per-feature specs. Decay between features.", false],
    ["VibeLoom", "Contract-driven — system-level contracts govern many cycles. Drift detected at the contract layer.", true],
  ];
  rows.forEach(([who, what, us], i) => {
    const cy = ry + i * (rh + rgap);
    s.addShape(pres.shapes.RECTANGLE, {
      x: MX, y: cy, w: W - 2 * MX, h: rh,
      fill: { color: us ? C.redSoft : C.bg },
      line: { color: us ? C.red : C.line, width: us ? 1 : 0.5 },
    });
    if (us) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: MX, y: cy, w: 0.06, h: rh,
        fill: { color: C.red }, line: { type: "none" },
      });
    }
    s.addText(who, {
      x: MX + 0.3, y: cy + 0.15, w: 3.8, h: 0.55,
      fontSize: 15, fontFace: F.mono, bold: true,
      color: us ? C.redDeep : C.ink, margin: 0, charSpacing: -0.5,
    });
    s.addText(what, {
      x: 4.5, y: cy + 0.2, w: W - MX - 4.5 - 0.3, h: 0.55,
      fontSize: 13, fontFace: F.sans, color: us ? C.ink2 : C.ink3, margin: 0,
    });
  });

  s.addText("We are not in the same fight as Cursor. We win by being one abstraction level up.", {
    x: MX, y: ry + 3 * (rh + rgap) + 0.05, w: W - 2 * MX, h: 0.5,
    fontSize: 15, fontFace: F.serif, italic: true, color: C.ink2,
    align: "center", margin: 0,
  });
}

// =============================================================================
// SLIDE 7 — SOLUTION (product)
// "The contract layer." — the actual product
// =============================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  s.addText("07 / 10", {
    x: MX, y: 0.45, w: 2, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  s.addText("PRODUCT", {
    x: W - MX - 4, y: 0.45, w: 4, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.ink5, align: "right", charSpacing: 1, margin: 0,
  });

  s.addText("The contract layer.", {
    x: MX, y: 1.0, w: W - 2 * MX, h: 1.1,
    fontSize: 64, fontFace: F.sans, bold: true,
    color: C.ink, charSpacing: -2, margin: 0,
  });

  s.addText("Methodology + Skill + deterministic engine. Ships as a Claude Code / Codex Skill. Open source under MIT.", {
    x: MX, y: 2.25, w: W - 2 * MX, h: 0.7,
    fontSize: 16, fontFace: F.sans, color: C.ink3, margin: 0,
  });

  // 4-step flow as horizontal cards
  const fy = 3.4;
  const fh = 1.6;
  const fw = (W - 2 * MX - 3 * 0.25) / 4;
  const steps = [
    ["1", "intent.md", "User edits intent + approves"],
    ["2", "regenerate", "Engine produces architecture, code, tests"],
    ["3", "eval", "Decidable + mechanical + heuristic checks"],
    ["4", "ship", "Code-sync trace closes the loop"],
  ];
  steps.forEach(([num, name, desc], i) => {
    const sx = MX + i * (fw + 0.25);
    s.addShape(pres.shapes.RECTANGLE, {
      x: sx, y: fy, w: fw, h: fh,
      fill: { color: i === 3 ? C.bgMute : C.bg },
      line: { color: C.line, width: 0.75 },
    });
    // left accent bar — red on first step, gray on others
    s.addShape(pres.shapes.RECTANGLE, {
      x: sx, y: fy, w: 0.04, h: fh,
      fill: { color: i === 0 ? C.red : (i === 3 ? C.line2 : C.ink4) },
      line: { type: "none" },
    });
    s.addText(num, {
      x: sx + 0.25, y: fy + 0.2, w: 0.5, h: 0.5,
      fontSize: 28, fontFace: F.serif, italic: true, bold: true,
      color: i === 0 ? C.red : C.ink4, margin: 0,
    });
    s.addText(name, {
      x: sx + 0.85, y: fy + 0.27, w: fw - 1, h: 0.4,
      fontSize: 14, fontFace: F.mono, bold: true,
      color: C.ink, margin: 0, charSpacing: -0.3,
    });
    s.addText(desc, {
      x: sx + 0.25, y: fy + 0.85, w: fw - 0.5, h: 0.6,
      fontSize: 12, fontFace: F.sans, color: C.ink3, margin: 0,
    });
  });

  // Modes row — single line
  s.addText([
    { text: "FIVE MODES   ", options: { color: C.redDeep, fontFace: F.mono, bold: true, charSpacing: 1, fontSize: 10 } },
    { text: "vibe", options: { color: C.ink, fontFace: F.mono, bold: true } },
    { text: " (solo) · ", options: { color: C.ink4, fontFace: F.sans } },
    { text: "pm", options: { color: C.ink, fontFace: F.mono, bold: true } },
    { text: " (product) · ", options: { color: C.ink4, fontFace: F.sans } },
    { text: "dev", options: { color: C.ink, fontFace: F.mono, bold: true } },
    { text: " (tech) · ", options: { color: C.ink4, fontFace: F.sans } },
    { text: "ux", options: { color: C.ink, fontFace: F.mono, bold: true } },
    { text: " (design) · ", options: { color: C.ink4, fontFace: F.sans } },
    { text: "expert", options: { color: C.ink, fontFace: F.mono, bold: true } },
    { text: " (regulated)", options: { color: C.ink4, fontFace: F.sans } },
  ], {
    x: MX, y: fy + fh + 0.4, w: W - 2 * MX, h: 0.5,
    fontSize: 14, margin: 0,
  });

  // Tagline
  s.addText("Open source: methodology, Skill, templates.  Paid: hosted engine, audit, compliance.", {
    x: MX, y: fy + fh + 0.95, w: W - 2 * MX, h: 0.4,
    fontSize: 12, fontFace: F.mono, color: C.ink5, margin: 0,
  });
}

// =============================================================================
// SLIDE 8 — BUSINESS MODEL
// "Open core. Tiered SaaS."
// =============================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  s.addText("08 / 10", {
    x: MX, y: 0.45, w: 2, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  s.addText("BUSINESS MODEL", {
    x: W - MX - 4, y: 0.45, w: 4, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.ink5, align: "right", charSpacing: 1, margin: 0,
  });

  s.addText("Open core. Tiered SaaS.", {
    x: MX, y: 1.0, w: W - 2 * MX, h: 1.1,
    fontSize: 56, fontFace: F.sans, bold: true,
    color: C.ink, charSpacing: -2, margin: 0,
  });

  s.addText("MIT-licensed methodology + Skill pulls developers in (PLG, Cursor's pattern). Paid tiers capture engineering teams that need audit, telemetry, compliance.", {
    x: MX, y: 2.25, w: W - 2 * MX, h: 0.7,
    fontSize: 15, fontFace: F.sans, color: C.ink3, margin: 0,
  });

  // 3 pricing cards
  const py = 3.4, ph = 3.2;
  const pw = (W - 2 * MX - 0.5) / 3;
  const tiers = [
    {
      tier: "FREE", price: "$0", unit: "MIT-licensed",
      who: "Solo devs, OSS, hobbyists",
      items: ["vibe + pm modes", "Methodology + Skill", "Self-hosted engine", "100 generations / mo"],
      featured: false,
    },
    {
      tier: "TEAM", price: "$30", unit: "/ seat / month",
      who: "Engineering teams of 5–50",
      items: ["Full pm / dev / ux modes", "Hosted engine", "Audit logs + drift telemetry", "Unlimited generations"],
      featured: true,
    },
    {
      tier: "ENTERPRISE", price: "$50K+", unit: "/ year",
      who: "Mid-market & enterprise (50+ eng)",
      items: ["expert mode + compliance", "On-prem engine", "SOC2 / HIPAA bundles", "Founder advisor seat"],
      featured: false,
    },
  ];
  tiers.forEach((t, i) => {
    const cx = MX + i * (pw + 0.25);
    if (t.featured) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: cx, y: py, w: pw, h: ph,
        fill: { color: C.redSoft }, line: { color: C.red, width: 1 },
      });
      s.addShape(pres.shapes.RECTANGLE, {
        x: cx, y: py, w: 0.06, h: ph,
        fill: { color: C.red }, line: { type: "none" },
      });
    } else {
      s.addShape(pres.shapes.RECTANGLE, {
        x: cx, y: py, w: pw, h: ph,
        fill: { color: C.bg }, line: { color: C.line, width: 0.75 },
      });
    }
    s.addText(t.tier + (t.featured ? " · RECOMMENDED" : ""), {
      x: cx + 0.35, y: py + 0.3, w: pw - 0.7, h: 0.3,
      fontSize: 9, fontFace: F.mono, bold: true,
      color: t.featured ? C.redDeep : C.ink4, charSpacing: 1, margin: 0,
    });
    s.addText([
      { text: t.price, options: { fontSize: 36, fontFace: F.serif, italic: true, bold: true, color: t.featured ? C.redDeep : C.ink } },
      { text: "  " + t.unit, options: { fontSize: 11, fontFace: F.sans, color: C.ink4 } },
    ], {
      x: cx + 0.35, y: py + 0.7, w: pw - 0.7, h: 0.7, margin: 0,
    });
    s.addText(t.who, {
      x: cx + 0.35, y: py + 1.55, w: pw - 0.7, h: 0.4,
      fontSize: 13, fontFace: F.sans, bold: true, color: C.ink2, margin: 0,
    });
    s.addText(t.items.map((it, j) => ({
      text: it, options: { breakLine: j < t.items.length - 1, bullet: { code: "2192" } }
    })), {
      x: cx + 0.35, y: py + 2.05, w: pw - 0.7, h: 1.0,
      fontSize: 11, fontFace: F.sans, color: C.ink3,
      paraSpaceAfter: 4, margin: 0,
    });
  });

  s.addText("GTM: land via individual devs (free Skill, Discord, GitHub). Expand to teams when drift becomes a P1.", {
    x: MX, y: py + ph + 0.2, w: W - 2 * MX, h: 0.4,
    fontSize: 12, fontFace: F.serif, italic: true, color: C.ink3,
    margin: 0,
  });
}

// =============================================================================
// SLIDE 9 — TEAM
// "Solo today. Two by month six."
// =============================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bg };

  s.addText("09 / 10", {
    x: MX, y: 0.45, w: 2, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  s.addText("TEAM", {
    x: W - MX - 4, y: 0.45, w: 4, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.ink5, align: "right", charSpacing: 1, margin: 0,
  });

  s.addText([
    { text: "Solo today.", options: { color: C.ink, bold: true, fontFace: F.sans, breakLine: true } },
    { text: "Two by month six.", options: { color: C.red, italic: true, bold: true, fontFace: F.serif } },
  ], {
    x: MX, y: 0.95, w: W - 2 * MX, h: 1.95,
    fontSize: 56, charSpacing: -2, margin: 0, valign: "top",
  });

  s.addText("VCs commonly flag solo founders. The concern is fair. Q1 milestone: technical co-founder onboarded — distributed-systems / dev-infra background — by month 6.", {
    x: MX, y: 3.05, w: W - 2 * MX, h: 0.85,
    fontSize: 14, fontFace: F.sans, color: C.ink3, margin: 0,
  });

  // Bio left, milestone right
  const cy = 4.0;
  const ch = 3.1;
  const cw = (W - 2 * MX - 0.4) / 2;

  // Bio card (white with line)
  s.addShape(pres.shapes.RECTANGLE, {
    x: MX, y: cy, w: cw, h: ch,
    fill: { color: C.bg }, line: { color: C.line, width: 0.75 },
  });
  s.addText("Ilya Baimetov", {
    x: MX + 0.3, y: cy + 0.25, w: cw - 0.6, h: 0.45,
    fontSize: 20, fontFace: F.sans, bold: true, color: C.ink,
    charSpacing: -0.5, margin: 0,
  });
  s.addText("FOUNDER · AUTHOR OF CODÆ + VIBELOOM", {
    x: MX + 0.3, y: cy + 0.7, w: cw - 0.6, h: 0.28,
    fontSize: 9, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  // Bio body — no visible TODO markers; placeholder reads as neutral italic
  s.addText([
    { text: "Background. ", options: { bold: true, color: C.ink } },
    { text: "Add prior roles + technical depth here.\n\n", options: { color: C.ink4, italic: true } },
    { text: "Why me. ", options: { bold: true, color: C.ink } },
    { text: "Authored the codæ paradigm + v0.3 spec end-to-end (methodology, implementation, comparison whitepaper, 35 templates, marketing site). Built daily with frontier agents through 2025–2026; saw the slop pattern emerge in production.\n\n", options: { color: C.ink3 } },
    { text: "Insight. ", options: { bold: true, color: C.ink } },
    { text: "The next layer is making the contract — not the chat — the durable surface humans operate on.", options: { color: C.ink3 } },
  ], {
    x: MX + 0.3, y: cy + 1.1, w: cw - 0.6, h: ch - 1.3,
    fontSize: 11, fontFace: F.sans, valign: "top", margin: 0,
  });

  // Q1 milestone card (red-tinted)
  const bx = MX + cw + 0.4;
  s.addShape(pres.shapes.RECTANGLE, {
    x: bx, y: cy, w: cw, h: ch,
    fill: { color: C.redSoft }, line: { color: C.red, width: 0.75 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: bx, y: cy, w: 0.06, h: ch,
    fill: { color: C.red }, line: { type: "none" },
  });
  s.addText("CO-FOUNDER ACQUISITION — TRACKED MILESTONE", {
    x: bx + 0.3, y: cy + 0.25, w: cw - 0.6, h: 0.3,
    fontSize: 9, fontFace: F.mono, bold: true,
    color: C.redDeep, charSpacing: 1, margin: 0,
  });
  s.addText("By month 6.", {
    x: bx + 0.3, y: cy + 0.6, w: cw - 0.6, h: 0.7,
    fontSize: 32, fontFace: F.serif, italic: true, bold: true,
    color: C.red, charSpacing: -1, margin: 0,
  });
  s.addText("Profile: distributed-systems / dev-infra / ex-platform-engineering. The pre-seed round itself is the team-formation forcing function — not a workaround.", {
    x: bx + 0.3, y: cy + 1.45, w: cw - 0.6, h: 0.85,
    fontSize: 12, fontFace: F.sans, color: C.ink2, margin: 0,
  });
  s.addText([
    { text: "Advisors. ", options: { color: C.ink, bold: true } },
    { text: "Add named advisor list or design-partner pipeline here.", options: { color: C.ink4, italic: true } },
  ], {
    x: bx + 0.3, y: cy + 2.45, w: cw - 0.6, h: 0.55,
    fontSize: 11, fontFace: F.sans, margin: 0,
  });
}

// =============================================================================
// SLIDE 10 — ASK (DARK)
// "$XXX. Ship the dark factory."
// =============================================================================
{
  const s = pres.addSlide();
  s.background = { color: C.ink };

  s.addText("10 / 10", {
    x: MX, y: 0.45, w: 2, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.red, charSpacing: 1, margin: 0,
  });
  s.addText("THE ASK", {
    x: W - MX - 4, y: 0.45, w: 4, h: 0.3, fontSize: 10, fontFace: F.mono, bold: true,
    color: C.whiteSoft, align: "right", charSpacing: 1, margin: 0,
  });

  // Two stacked headline lines — explicit breakLine, plenty of vertical room
  s.addText([
    { text: "$XXX", options: { color: C.red, italic: true, fontFace: F.serif, bold: true } },
    { text: ".  18 months.", options: { color: C.white, bold: true, fontFace: F.sans, breakLine: true } },
    { text: "Ship the ", options: { color: C.white, bold: true, fontFace: F.sans } },
    { text: "dark factory", options: { color: C.red, italic: true, fontFace: F.serif, bold: true } },
    { text: ".", options: { color: C.white, bold: true, fontFace: F.sans } },
  ], {
    x: MX, y: 1.15, w: W - 2 * MX, h: 2.7,
    fontSize: 68, charSpacing: -2, margin: 0, valign: "top",
  });

  s.addText("Engine v0.4  →  10 design partners  →  drift telemetry  →  Series A traction.", {
    x: MX, y: 4.05, w: W - 2 * MX, h: 0.45,
    fontSize: 16, fontFace: F.sans, color: C.whiteSoft, margin: 0,
  });

  // 2 cards: use of funds + milestones
  const cy = 4.75, ch = 2.0;
  const cw = (W - 2 * MX - 0.4) / 2;

  // Use of funds — red-tinted on dark
  s.addShape(pres.shapes.RECTANGLE, {
    x: MX, y: cy, w: cw, h: ch,
    fill: { color: "1A1A1A" }, line: { color: C.red, width: 0.75 },
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: MX, y: cy, w: 0.06, h: ch,
    fill: { color: C.red }, line: { type: "none" },
  });
  s.addText("USE OF FUNDS — 18 MONTHS", {
    x: MX + 0.3, y: cy + 0.18, w: cw - 0.5, h: 0.3,
    fontSize: 9, fontFace: F.mono, bold: true,
    color: C.red, charSpacing: 1, margin: 0,
  });
  s.addText([
    { text: "55% Engineering — ", options: { bold: true, color: C.white, breakLine: false } },
    { text: "co-founder + 2 senior eng\n", options: { color: C.whiteSoft } },
    { text: "25% Design partners — ", options: { bold: true, color: C.white } },
    { text: "success + onboarding + telemetry\n", options: { color: C.whiteSoft } },
    { text: "10% Legal / IP / compliance — ", options: { bold: true, color: C.white } },
    { text: "entity, IP, SOC2 prep\n", options: { color: C.whiteSoft } },
    { text: "10% Buffer + ops", options: { bold: true, color: C.white } },
  ], {
    x: MX + 0.3, y: cy + 0.58, w: cw - 0.5, h: 1.3,
    fontSize: 12, fontFace: F.sans, valign: "top", margin: 0,
  });

  // Milestones — white-on-dark
  const bx = MX + cw + 0.4;
  s.addShape(pres.shapes.RECTANGLE, {
    x: bx, y: cy, w: cw, h: ch,
    fill: { color: "1A1A1A" }, line: { color: C.ink4, width: 0.75 },
  });
  s.addText("MILESTONES TO SERIES A", {
    x: bx + 0.3, y: cy + 0.18, w: cw - 0.5, h: 0.3,
    fontSize: 9, fontFace: F.mono, bold: true,
    color: C.red, charSpacing: 1, margin: 0,
  });
  s.addText([
    { text: "Mo 3  ", options: { bold: true, color: C.red, fontFace: F.mono } },
    { text: "Engine v0.4 dogfood-ready\n", options: { color: C.whiteSoft } },
    { text: "Mo 6  ", options: { bold: true, color: C.red, fontFace: F.mono } },
    { text: "Co-founder + 5 design partners shipping\n", options: { color: C.whiteSoft } },
    { text: "Mo 12 ", options: { bold: true, color: C.red, fontFace: F.mono } },
    { text: "First paying teams + drift telemetry, 10+ codebases\n", options: { color: C.whiteSoft } },
    { text: "Mo 18 ", options: { bold: true, color: C.red, fontFace: F.mono } },
    { text: "Series A on trace-derived learning evidence", options: { color: C.whiteSoft } },
  ], {
    x: bx + 0.3, y: cy + 0.58, w: cw - 0.5, h: 1.3,
    fontSize: 12, fontFace: F.sans, valign: "top", margin: 0,
  });

  // Bottom contact
  s.addText([
    { text: "Ilya Baimetov", options: { bold: true, color: C.white } },
    { text: "      ilya.baimetov@vibeloom.ai      vibeloom.ai      github.com/ilya-baimetov/vibeloom", options: { color: C.whiteSoft } },
  ], {
    x: MX, y: H - 0.55, w: W - 2 * MX, h: 0.3,
    fontSize: 10, fontFace: F.mono, margin: 0, charSpacing: 0.4,
  });
}

// =============================================================================
// SAVE
// =============================================================================
pres.writeFile({ fileName: "pitch-deck.pptx" }).then((file) => {
  console.log(`✓ wrote ${file}`);
});
