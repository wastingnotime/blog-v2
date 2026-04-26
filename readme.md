# blog-v2

## What This Repository Is

`blog-v2` is the current repository for the Wasting No Time publication.
It is the static-first successor to `../blog`, with the goal of keeping the
site simple to ship, easy to browse, and deterministic to build.

The repository's direction is intentionally different from the predecessor:

- publish as a static site on GitHub Pages
- remove any dependency on a same-origin `/api` path
- avoid assuming AWS deploy infrastructure is part of the blog runtime

The old `../blog` repository evolved toward an AWS-hosted container plus an
analytics ingestion pipeline routed through `https://blog.wastingnotime.org/api`.
`blog-v2` starts from the opposite direction: static output first, direct
browser rendering, and optional third-party analytics that do not require
first-party API infrastructure.

## Role of MRL

This repository uses Model Refinement Lab as the operating method for changing
the site.

MRL is not the product here. The product is the publication itself. MRL is the
workflow that keeps the site evolution explicit through artifacts, slices, and
evaluations so changes stay traceable and reviewable.

In practice, that means:

- semantic docs capture the site model and constraints
- slice docs define one bounded change at a time
- code and tests implement the current slice
- decisions and commits preserve the repository history of each completed change

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

## License

This repository uses split licensing:

- code, build tooling, tests, and operating workflow documents are licensed under MPL-2.0
- blog content, publication assets, semantic artifacts, slice artifacts, and generated publication output derived from that content are licensed under CC BY-NC-SA 4.0

See [LICENSE](/home/henrique/repos/github/wastingnotime/blog-v2/LICENSE), [LICENSES/MPL-2.0.txt](/home/henrique/repos/github/wastingnotime/blog-v2/LICENSES/MPL-2.0.txt), and [LICENSES/CC-BY-NC-SA-4.0.txt](/home/henrique/repos/github/wastingnotime/blog-v2/LICENSES/CC-BY-NC-SA-4.0.txt).

## Migration Context

The repository artifacts for this migration are:

- [work/changes/2026-04-16-gh-pages-reset/request.md](/home/henrique/repos/github/wastingnotime/blog-v2/work/changes/2026-04-16-gh-pages-reset/request.md)
- [work/changes/2026-04-16-gh-pages-reset/impact_analysis.md](/home/henrique/repos/github/wastingnotime/blog-v2/work/changes/2026-04-16-gh-pages-reset/impact_analysis.md)
- [docs/slices/2026-04-16-gh-pages-reset.md](/home/henrique/repos/github/wastingnotime/blog-v2/docs/slices/2026-04-16-gh-pages-reset.md)
