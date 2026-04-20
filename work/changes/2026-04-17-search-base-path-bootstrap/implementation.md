# Implementation

## Summary

Implemented the search base-path bootstrap slice by removing the last
root-relative search submission target and making the generated search form
action derive from `SiteConfig.base_url`.

## Main Changes

- updated `src/app/application/use_cases/build_site.py`:
  - `build_search_page(...)` now computes `search_action_url` via
    `_absolute_url(config.base_url, "/search/")`
  - search form output now renders:
    `action="<base_url>/search/"` instead of `action="/search/"`
- preserved existing search behavior:
  - static index fetch still uses `search.json` projected from
    `SiteConfig.base_url`
  - URL-state query logic (`?q=` hydration and `replaceState`) remains unchanged
  - canonical URL for `/search/` remains unchanged and aligned with base URL

## Test Updates

- `tests/unit/test_build_site.py`
  - updated existing assertion to require
    `action="https://example.com/search/"`
  - added `test_build_static_site_uses_base_url_for_search_form_action` to
    verify prefixed deployment behavior with
    `base_url="https://example.com/blog/"`
  - made `_site_config(...)` accept an optional `base_url` override for bounded
    deterministic scenarios
- `tests/integration/test_run_scenario.py`
  - updated existing scenario assertion to require
    `action="https://blog.wastingnotime.org/search/"`
  - added
    `test_static_site_builder_uses_prefixed_base_url_for_search_form_action`
    using `SITE_BASE_URL=https://example.com/blog/` and validating generated
    `dist/search/index.html` action, canonical URL, and search index URL

## Validation

- `pytest` (full suite)
  - result: `64 passed`
- `OUTPUT_DIR=/tmp/blog-v2-search-base-path SITE_BASE_URL=https://example.com/blog/ python3 -m src.app.interfaces.cli.run_scenario`
  - result: generated search page contains:
    - canonical `https://example.com/blog/search/`
    - form action `https://example.com/blog/search/`
    - search index URL `https://example.com/blog/search.json`
