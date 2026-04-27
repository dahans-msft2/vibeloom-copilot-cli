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

- Static assets are served from `public/`.
- Deployed URL structure: `/` (overview), `/methodology`, `/implementation`, `/contact`, `/robots.txt`, `/sitemap.xml`.
- One shared stylesheet at `public/styles.css`; one logo at `public/vibeloom-logo-loom.svg`.

## Local Preview

Any static-file server works. Example:

```bash
npx http-server site/public -p 8124 -c-1
# open http://127.0.0.1:8124/
```
