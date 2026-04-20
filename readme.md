# blog-v2

## Purpose

`blog-v2` is the next version of the `../blog` site.

The first architectural reset in this repository is explicit:

- publish as a static site on GitHub Pages
- remove any dependency on a same-origin `/api` path
- stop assuming AWS deploy infrastructure is part of the blog runtime

The previous `../blog` repository evolved toward an AWS-hosted container plus
an analytics ingestion pipeline routed through `https://blog.wastingnotime.org/api`.
This repository intentionally starts from the opposite direction: static output
first, direct browser rendering, and optional third-party analytics that do not
require first-party API infrastructure.

## Commands

```bash
pip install -e .
pytest
python -m src.app.interfaces.cli.run_scenario
./scripts/gh-pages-bootstrap
./scripts/mrl-serve
```

The scenario runner generates a minimal static site into `dist/`.

Local dev server:

- `./scripts/mrl-serve` builds `dist/`, serves it on `http://localhost:8080/`, and auto-reloads the browser when watched files change.
- Override `MRL_SERVE_PORT`, `MRL_SERVE_HOST`, `MRL_SERVE_OUTPUT_DIR`, `MRL_SERVE_CONTENT_ROOT`, and `MRL_SERVE_ASSETS_DIR` when needed.
- Set `SITE_BASE_URL=http://localhost:8080/` if you want local canonical URLs and sitemap links to point at the dev server.

One-time GitHub Pages bootstrap:

- Run `./scripts/gh-pages-bootstrap` once from the repo root after `gh auth login`.
- The command uses `gh api` to create or update the repository Pages site with `build_type=workflow`.
- You need repository admin or Pages settings permission for that call.
- If Pages is deleted or reset later, run the same command again.

## Current Slice

The current implemented slice is a bootstrap for static deployment:

- a Python builder renders `dist/index.html`
- analytics are disabled by default
- when analytics are enabled, the generated HTML uses a direct external script
  instead of a same-origin `/api` endpoint
- a GitHub Actions workflow deploys the generated `dist/` folder to GitHub
  Pages

## Environment

Build-time configuration is optional:

- `SITE_TITLE`
- `SITE_DESCRIPTION`
- `SITE_BASE_URL` - canonical URL used by generated links, feeds, and sitemap output

The default site build does not require any analytics configuration.

## Migration Context

The repository artifacts for this migration are:

- [work/changes/2026-04-16-gh-pages-reset/request.md](/home/henrique/repos/github/wastingnotime/blog-v2/work/changes/2026-04-16-gh-pages-reset/request.md)
- [work/changes/2026-04-16-gh-pages-reset/impact_analysis.md](/home/henrique/repos/github/wastingnotime/blog-v2/work/changes/2026-04-16-gh-pages-reset/impact_analysis.md)
- [docs/slices/2026-04-16-gh-pages-reset.md](/home/henrique/repos/github/wastingnotime/blog-v2/docs/slices/2026-04-16-gh-pages-reset.md)
