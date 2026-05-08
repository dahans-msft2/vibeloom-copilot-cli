# Site claim map

Externalized Step 1 verify for `review-site.md`. Per-page claim inventory and canon basis.

Pages reviewed (all under `v03/site/public/`):

| File | Title | Hero h1 | Role |
|---|---|---|---|
| `index.html` | "VibeLoom — Contract-Driven Agentic Engineering" | "Contract-driven agentic engineering" (with word-cycle Spec↔Contract) | Landing / overview |
| `codae.html` | "codæ — Contract-Driven Agentic Engineering · Whitepaper" | "codæ" | The case for the paradigm (compact whitepaper view; ~42K) |
| `codæ-manifesto.html` | "codæ — Dark-Factory AI Coding · Contract-Driven Agentic Engineering" | "codæ" | Full canonical manifesto (byte-identical to `v03/codæ-manifesto.html`; ~78K) |
| `methodology.html` | "Methodology — Contract-Driven Agentic Engineering · VibeLoom" | "The contract-driven methodology for AI-coded projects." | Methodology summary |
| `implementation.html` | "Implementation — Skill + Engine + Runtime · VibeLoom" | "The Skill and the engine." | Implementation summary |
| `get-started.html` | "Get started — VibeLoom (30-minute on-ramp) · v0.3" | "Make your first contract in 30 minutes." | Onboarding |
| `contact.html` | "Contact Us — Make Coding Agents Useful Past the Demo · VibeLoom" | "Make coding agents useful past the demo." | Contact |
| `404.html` | "404 — Not found · VibeLoom" | "Page not found." | Error |

Plus standalone (NOT served from site/, but reachable from canon):
- `v03/vibeloom-comparison.html` — comparison vs spec-driven tools. Not in `site/public/`; no nav link to it.

## Cross-walk: load-bearing site claims → canon basis

### `index.html` — load-bearing claims

| Site claim | Canon basis |
|---|---|
| "Contract-driven agentic engineering" (hero) | Manifesto §3 (the paradigm) |
| "Living contract stack to generate, evaluate, and reconcile AI-coded systems" (sub) | Methodology §4 (layers + traces) |
| "Graph-backed drift detection" (hero meta) | Methodology §9 (status taxonomy) + §8 (Contract Graph) |
| "Scoped subagents for parallel work" (hero meta) | Implementation §13 (dispatch + waves) |
| "Python 3.10+, no runtime dependencies" (hero meta + trust strip) | Implementation §1 (runtime architecture) |
| "Open-source Skill for Claude Code & Codex" (hero badge) | Implementation §1 + Templates skill manifest |
| "Spec-driven → Contract-driven" comparison teaser | Manifesto §3 + methodology §16 (workflow shapes) |

### `codae.html` — load-bearing claims

| Site claim | Canon basis |
|---|---|
| Cognitive surface visual (108K LOC vs ~24% contract) | Manifesto §5 visual (mendable surface) |
| "Contract is memory + eval" | Manifesto §6 |
| The codæ thesis | Manifesto §3, §8 |

### `methodology.html` — load-bearing claims

| Site h2 | Canon §  |
|---|---|
| Principles | M §2 |
| When to use | M §3 |
| Architecture | M §4 |
| Contract stack | M §6 |
| Contract graph | M §8 (now **Contract Graph**) |
| Modes | M §5 |
| Operations | M §12 |
| Lifecycle + traces | M §11 |
| Eval — verification ladder | M §14 |
| Drift and status | M §9 |
| VibeLoom vs spec-driven tools | M §16 (workflow shapes) + comparison content |
| Roadmap | roadmap.md |
| See also | M §18 |

### `implementation.html` — load-bearing claims

| Site h2 | Canon § |
|---|---|
| Skill and engine, one substrate | I §1 (runtime architecture) |
| Cache + traces | I §3 |
| The Skill | I §1 + Templates skill manifest |
| The engine | I §4 |
| Engine CLI | I §1 + getting-started commands |
| Approval traces and drift detection | I §10 (status), I §8.1 (approval trace schema) |
| The contract graph | I §8 (frontmatter `derives_from`) + M §8 |
| IDs and frontmatter | I §5.1 + §6 |
| Trace families | I §8 |
| Subagent dispatch | I §13 |
| Install + Quickstart | get-started.html mirror |
| Source layout | I §2 |
| Testing | n/a — site-original detail |

### `get-started.html` — load-bearing claims

Reflects `v03/getting-started.md` step-by-step (recently shipped; verified during review-canon as up-to-date).

### `contact.html` — load-bearing claims

Just the email + GitHub link. No load-bearing canon claims. (Recent simplification took.)

## Identified cascades (canon → site) from previous review-canon session

| # | Cascade source | Site location |
|---|---|---|
| 1 | CANON-FIND-010 (Contract Graph rename) | `methodology.html` line 205: "approved derivation graph" |
| 2 | CANON-FIND-010 (Contract Graph proper noun) | `methodology.html` lines 139, 245, 247, 369, 412 use "contract graph" lowercase where canon §8 now establishes "Contract Graph" |
| 3 | CANON-FIND-010 (Contract Graph proper noun) | `implementation.html` lines 8 (meta keyword), 132 (TOC), 146 (body) use lowercase |
| 4 | CANON-FIND-005 / 006 / 007 / 011 | No site cascades — site doesn't surface §10 metric, §16/§17 sections, or §5.1 derivation rules at the level of detail that would shift |

## Items NOT load-bearing for the canon (site-original)

- Hero meta lists, brand strip, marketing copy phrasing, narrative arc, CTAs, badges, footers, social/SEO metadata, JSON-LD: all site decisions, not derived from canon.

## Cross-walk delta — what canon work didn't propagate

- Manifesto §1-§8 unchanged in this canon-review pass (only methodology + implementation + templates touched). Site `codae.html` and `codæ-manifesto.html` content remains aligned with canon manifesto.
- Implementation page may need section-numbering audit if next review-canon edits implementation §-numbers (we just renumbered §18→§16, §19→§17, §20→§18 — but the site's implementation.html doesn't use those § numbers in its UI).
