# VibeLoom Site

This directory is the standalone public website project for `https://vibeloom.ai/`.

## Structure

| Path | Purpose |
| --- | --- |
| `wrangler.jsonc` | Cloudflare Workers Static Assets config for the site project |
| `public/` | Static site files served at `vibeloom.ai` |

## Cloudflare Setup

Use this directory as the project root in Cloudflare.

1. In Cloudflare Workers, create or import a Worker from the GitHub repo.
2. Use `main` as the production branch.
3. Set the repository root directory to `site`.
4. Do not set a separate build output directory.
5. Keep deployment config in `site/wrangler.jsonc`.
6. Attach `vibeloom.ai` and `www.vibeloom.ai` as custom domains after the zone is active in Cloudflare DNS.

## Local Notes

- static assets are served from `public/`
- the deployed URL structure should remain `/`, `/methodology`, `/robots.txt`, and `/sitemap.xml`
