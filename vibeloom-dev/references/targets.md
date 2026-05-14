# Reference: targets

What each target keyword refers to, which commands accept it, and which files it covers.

## Targets

| Target | Files | `init` | `eval` | `review` | `generate` | `reconcile` | `feedback` |
|---|---|---|---|---|---|---|---|
| `intent` | `vNN/intent.md` | (init creates it) | ✓ | ✓ | ✗ (hand-authored) | ✓ | ✓ |
| `manifesto` | `vNN/canon/codæ-manifesto.html` | ✗ | ✓ | ✓ | ✗ (hand-authored) | ✓ | ✓ |
| `methodology` | `vNN/canon/vibeloom-methodology.md` | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| `implementation` | `vNN/canon/vibeloom-implementation.md` + `vNN/canon/vibeloom-templates.md` | ✗ | ✓ | ✓ | ✓ (both files together) | ✓ | ✓ |
| `skill` | `vNN/skill/**` (SKILL.md + references/ + tasks/ + artifacts/ + engine/) | ✗ | ✓ | ✓ | ✓ (extract + maybe engine regen) | ✓ | ✓ |
| `site` | `vNN/site/**` (public/ + comparison-source.html) | ✗ | ✓ | ✓ | ✓ (HTML pages) | ✓ | ✓ |
| `canon` (shortcut) | intent + manifesto + methodology + implementation | n/a | ✓ | ✓ | ✗ (no single command — use per-target) | ✓ | ✓ |
| `all` (shortcut) | canon + skill + site | n/a | ✓ | ✓ | ✗ (no single command) | ✓ | ✓ |

## Why intent and manifesto can't be `generate`d

Both are **hand-authored**. Intent captures the user's version-specific direction (CAPs, CSTs, Vision). Manifesto is design-heavy HTML for human consumption (paradigm exposition). Neither is mechanically derivable from anything upstream — they ARE the upstream.

`init` creates a seed `intent.md` via interview (interactive); manifesto is authored directly by the user (often by copying from a prior version and hand-editing).

## Why `templates` is not a separate target

Templates are part of implementation. `generate implementation` produces both `vibeloom-implementation.md` and `vibeloom-templates.md` together — they're tightly coupled (templates materialize what implementation specifies).

## Why `engine` is not a separate target

Engine ships inside the skill bundle (`vNN/skill/engine/`). `generate skill` includes (re)generating the engine when implementation has changed in ways that warrant it. There is no separate `generate engine`.

## Default target

For `eval`, `review`, `reconcile`: default is `canon` when omitted. For `feedback`: target must be supplied explicitly. For `generate`: target is required.

## Site as marketing-register

`site` is the outlier: it's downstream of canon but in a different register (marketing/promotional, not normative). `eval site` checks that site does not CONTRADICT canon — NOT that site covers every canon concept. The site may legitimately omit details, abbreviate, or use friendlier language.

## Version-scoping

Every target is relative to a specific `vNN`. Commands take `--version vNN` (default = latest mutable). Frozen versions (v01-v03 legacy layout, or any current-production version) are read-only — `generate` / `reconcile` / `init --version <frozen-vNN>` refuse.
