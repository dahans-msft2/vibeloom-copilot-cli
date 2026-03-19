# VibeLoom Workspace

This repository is the VibeLoom workspace. It contains the current packaged skill in `v01/`, the next-generation workspace in `v02/`, and the independently deployed public website in `site/`.

## Workspace Map

| Path | Purpose |
| --- | --- |
| `v01/` | Current VibeLoom skill and methodology package |
| `v02/` | Next-generation implementation workspace for the Rust-based local engine and updated skill |
| `site/` | Public website project for `https://vibeloom.ai/` |
| `.claude/` | Workspace-local Claude metadata |
| `.github/` | Shared repository automation and CI metadata |

## Site Deployment

The public site is deployed from `site/`.

- Cloudflare repository root directory should be set to `site`
- `site/wrangler.jsonc` is the only Wrangler config for the public website
- static assets live in `site/public/`
- no separate build output directory is required

## Versioned Tool Workspaces

- `v01/` is the current archived package layout and remains runnable as the existing skill and methodology version
- `v02/` is intentionally only a placeholder in this phase and will host the Rust-based local engine and updated skill work next
