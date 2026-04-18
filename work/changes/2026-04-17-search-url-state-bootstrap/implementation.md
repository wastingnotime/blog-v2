# Implementation

## Summary

Implemented deterministic `/search/` URL-state coherence so the search page now
projects the same `?q=` contract it reads: initial hydration still comes from
`?q=`, interactive changes now update the browser URL, and clearing the query
returns the address to `/search/` without an empty parameter.

## Main Changes

- updated `src/app/application/use_cases/build_site.py` search-page markup to
  expose a shareable `GET` contract rooted at `/search/`:
  - added `<form id="search-form" method="get" action="/search/">`
  - added `name="q"` on the search input
- extended search-page client logic in `build_site.py` with
  `projectSearchUrlState(query)` to keep route URL state aligned during
  interaction:
  - sets `q` for non-empty queries
  - removes `q` when query is empty
  - uses `window.history.replaceState` on the existing route path
- preserved bounded behavior outside this slice:
  - search filtering still uses static `search.json`
  - canonical metadata remains `https://.../search/` (no per-query canonical)
  - no same-origin `/api` dependencies introduced

## Test Updates

- `tests/unit/test_build_site.py`
  - asserts generated `/search/` includes GET form contract (`action="/search/"`,
    `name="q"`)
  - asserts script contains URL-state projection hooks for set/remove `q` and
    `replaceState`
  - asserts canonical remains `/search/`
- `tests/integration/test_run_scenario.py`
  - asserts generated `dist/search/index.html` includes the same URL-state and
    GET-contract hooks
  - asserts canonical remains `/search/` and static-only assumptions stay intact

## Validation

- `pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `pytest`
- `python3 -m src.app.interfaces.cli.run_scenario`
