# Implementation

## Summary

Implemented the bounded JSON-LD structured-data slice by projecting deterministic
machine-readable metadata in the shared document head for publication routes
that already carry strong authored semantics.

## Main Changes

- updated `src/app/application/use_cases/build_site.py` to project and render
  one `application/ld+json` script per eligible route:
  - homepage emits `WebSite` JSON-LD
  - standalone pages emit `Article` JSON-LD
  - episodes emit `Article` JSON-LD
- kept structural and recovery routes out of scope by default:
  - `404.html`, search, archives, library hubs, saga pages, arc pages, and
    section hubs continue to emit no JSON-LD
- added deterministic structured-data helpers:
  - `_project_website_structured_data(...)`
  - `_project_article_structured_data(...)`
  - `_render_structured_data_script(...)` with stable JSON serialization

## Deterministic Contract

- canonical absolute URLs derive from `SITE_BASE_URL`
- `Article` JSON-LD uses repository-authored route metadata (title, summary,
  and publication date) and aligns author/site naming with existing head
  metadata (`author` host and site title)
- script payload serialization is deterministic through sorted keys and stable
  separators

## Test Updates

- `tests/unit/test_build_site.py`
  - added assertions for homepage `WebSite` JSON-LD payload
  - added assertions for page and episode `Article` JSON-LD payloads
  - added assertions that representative structural/recovery routes emit no
    JSON-LD
- `tests/integration/test_run_scenario.py`
  - added end-to-end assertions for homepage and content-route JSON-LD payloads
  - added assertion that `dist/404.html` emits no JSON-LD script

## Validation

- `pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `pytest`
