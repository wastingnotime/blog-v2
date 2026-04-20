# Implementation

## Summary

Implemented the bounded search-entry contract by linking homepage `WebSite`
JSON-LD to the existing static `/search/` route and hydrating the search page
from the deterministic `?q=` URL parameter.

## Main Changes

- updated `src/app/application/use_cases/build_site.py` to add one homepage
  `SearchAction` under `WebSite` JSON-LD:
  - `target`: `/search/?q={search_term_string}` resolved against `SITE_BASE_URL`
  - `query-input`: `required name=search_term_string`
- updated search-page client script in `build_site.py` to:
  - read initial query from `window.location.search` via `q`
  - pre-populate the search input with that value
  - run the same existing static `search.json` filtering path on first load
- kept canonical route behavior, static `search.json` usage, and no-`/api`
  constraints unchanged

## Test Updates

- `tests/unit/test_build_site.py`
  - asserts homepage `WebSite` JSON-LD includes bounded `SearchAction`
  - asserts generated search page includes deterministic `?q=` hydration hooks
- `tests/integration/test_run_scenario.py`
  - asserts generated homepage JSON-LD includes `SearchAction` target rooted at
    `https://blog.wastingnotime.org/search/?q={search_term_string}`
  - asserts generated `/search/` route contains deterministic `?q=` hydration
    logic while still using `search.json`

## Validation

- `pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `pytest`
- `python3 -m src.app.interfaces.cli.run_scenario`
