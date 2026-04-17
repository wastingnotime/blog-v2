# blog-v2

## Purpose

`blog-v2` is the next version of the `../blog` site.

The first architectural reset in this repository is explicit:

- publish as a static site on GitHub Pages
- remove any dependency on a same-origin `/api` path
- stop assuming AWS deploy infrastructure is part of the blog runtime

The previous `../blog` repository evolved toward an AWS-hosted container plus
an analytics ingestion pipeline routed through `https://wastingnotime.org/api`.
This repository intentionally starts from the opposite direction: static output
first, direct browser rendering, and optional third-party analytics that do not
require first-party API infrastructure.

## Commands

```bash
pip install -e .
pytest
python -m src.app.interfaces.cli.run_scenario
./scripts/mrl-refine
./scripts/mrl-build
```

The scenario runner generates a minimal static site into `dist/`.

Phase launcher defaults:

- `./scripts/mrl-refine` starts a non-interactive `codex exec` run in the repo root with `gpt-5.4` and `medium` reasoning effort.
- `./scripts/mrl-build` starts a non-interactive `codex exec` run in the repo root with `gpt-5.3-codex` and `medium` reasoning effort.
- Override them with `CODEX_REFINE_MODEL`, `CODEX_REFINE_REASONING_EFFORT`, `CODEX_BUILD_MODEL`, and `CODEX_BUILD_REASONING_EFFORT` when needed.

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
- `SITE_BASE_URL`
- `ANALYTICS_PROVIDER`
- `PLAUSIBLE_DOMAIN`
- `PLAUSIBLE_SCRIPT_URL`
- `PLAUSIBLE_API_HOST`

If analytics variables are omitted, the site is built with analytics disabled.

## Migration Context

The repository artifacts for this migration are:

- [work/changes/2026-04-16-gh-pages-reset/request.md](/home/henrique/repos/github/wastingnotime/blog-v2/work/changes/2026-04-16-gh-pages-reset/request.md)
- [work/changes/2026-04-16-gh-pages-reset/impact_analysis.md](/home/henrique/repos/github/wastingnotime/blog-v2/work/changes/2026-04-16-gh-pages-reset/impact_analysis.md)
- [docs/slices/2026-04-16-gh-pages-reset.md](/home/henrique/repos/github/wastingnotime/blog-v2/docs/slices/2026-04-16-gh-pages-reset.md)
