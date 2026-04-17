# Implementation

## Summary

Implemented a deterministic static search index by projecting repository-authored
pages, sagas, arcs, and episodes into `search.json` during the site build.

## Main Changes

- added `project_search_index` to compute flat search records with:
  - stable title, URL, and type fields
  - optional summary, tags, context, and date fields
  - absolute URLs derived from the configured site base URL
- extended the content model with `SearchEntry` and `SearchIndex`
- updated `build_site.py` to emit `search.json` alongside the existing HTML,
  feed, and sitemap outputs
- added unit and integration coverage for:
  - deterministic search record projection
  - emitted `search.json` output in the static build

## Validation

- `PYTHONPATH=. python3 -m pytest`
- `PYTHONPATH=. python3 -m src.app.interfaces.cli.run_scenario`
