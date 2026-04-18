# Implementation

## Summary

Implemented deterministic `WebPage` JSON-LD projection for the stable top-level
reader discovery hubs while preserving existing homepage and content-route
structured data behavior.

## Main Changes

- added `_project_webpage_structured_data(...)` in
  `src/app/application/use_cases/build_site.py`
- wired the new projector into these hub routes only:
  - `/archives/`
  - `/search/`
  - `/library/`
  - `/sagas/`
  - `/studio/`
- kept existing JSON-LD contracts unchanged for:
  - homepage (`WebSite` + existing `SearchAction`)
  - standalone pages and episode pages (`Article`)
- kept out-of-scope routes unchanged with no JSON-LD:
  - `404.html`
  - topic pages (`/library/<tag>/`)
  - saga detail pages (`/sagas/<slug>/`)
  - arc detail pages (`/sagas/<slug>/<arc>/`)

## Test Updates

- updated `tests/unit/test_build_site.py` to assert one deterministic `WebPage`
  payload on `/archives/`, `/search/`, `/library/`, `/sagas/`, and `/studio/`
- updated unit out-of-scope assertions to keep no JSON-LD on `404`, topic,
  saga detail, and arc detail routes
- updated `tests/integration/test_run_scenario.py` to verify generated scenario
  output includes the same bounded `WebPage` payloads for the five discovery
  hubs and still omits JSON-LD for topic/saga-detail/arc-detail routes

## Validation

- `pytest -q tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
  - result: `35 passed`
