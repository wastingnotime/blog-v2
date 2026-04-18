# Implementation

## Summary

Implemented deterministic route-specific robots projection so `/search/` now
renders `noindex,follow` while durable publication routes continue to render
`index,follow`.

## Main Changes

- added `project_route_robots_policy(canonical_path)` in
  `src/app/application/use_cases/project_route_robots_policy.py`:
  - `/search/` => `noindex,follow`
  - all other routes => `index,follow`
- updated shared document rendering in
  `src/app/application/use_cases/build_site.py` to derive robots metadata from
  route policy when no explicit override is provided:
  - `_render_document(...)` now accepts optional `robots_content`
  - default path uses `project_route_robots_policy(canonical_path)`
- preserved bounded behavior outside this slice:
  - explicit `404.html` `noindex,follow` override is unchanged
  - `/search/` canonical remains `/search/`
  - search page still references `search.json` and retains `?q=` URL-state contract
  - homepage `SearchAction` contract is unchanged

## Test Updates

- added `tests/unit/test_project_route_robots_policy.py`:
  - asserts `/search/` projects `noindex,follow`
  - asserts representative durable routes project `index,follow`
- updated `tests/unit/test_build_site.py`:
  - asserts generated `/search/` includes `noindex,follow`
  - asserts generated `/search/` no longer includes `index,follow`
  - keeps canonical `/search/` and `search.json` assertions
- updated `tests/integration/test_run_scenario.py`:
  - asserts generated `dist/search/index.html` includes `noindex,follow`
  - asserts generated `dist/search/index.html` excludes `index,follow`
  - keeps canonical `/search/`, `search.json`, and homepage `SearchAction`
    assertions unchanged

## Validation

- `pytest tests/unit/test_project_route_robots_policy.py tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `pytest`
- `python -m src.app.interfaces.cli.run_scenario`
