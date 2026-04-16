# Implementation

## Summary

Implemented machine-readable publication output for the static build by adding
deterministic projections for feed and sitemap metadata and emitting `feed.xml`
plus `sitemap.xml` alongside the HTML routes.

## Main Changes

- added `project_publication_metadata` to compute:
  - bounded feed entries from standalone pages and episodes
  - sitemap entries from generated publication routes with stable `lastmod`
- extended content view models with feed and sitemap record types
- updated `build_site.py` to render:
  - `feed.xml` with absolute canonical item URLs and RFC 2822 dates
  - `sitemap.xml` with absolute canonical route URLs and deterministic
    last-modified metadata
- added unit and integration coverage for publication metadata projection and
  XML output

## Validation

- `PYTHONPATH=. python3 -m pytest`
- `PYTHONPATH=. python3 -m src.app.interfaces.cli.run_scenario`
