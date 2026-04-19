# Impact Analysis

## Summary

The next coherent slice is to make search-index load failures recoverable by
adding bounded in-page guidance when `search.json` cannot be loaded.

Current observed gap:

- `/search/` now supports recovery for no-script and zero-results cases
- failure to load `search.json` still produces only a plain status message
- the reader gets failure feedback, but no next step inside the same static
  search surface

## Impacted Areas

- generated search-page script in `src/app/application/use_cases/build_site.py`
- deterministic reader-facing load-failure behavior on `/search/`
- unit and integration coverage for search-route recovery guidance

## Boundary Change

The build gains no new route, artifact, or backend dependency. The boundary
change is limited to load-failure recovery inside the existing static search
page:

- `/search/` stays the canonical route
- `search.json` stays the only search artifact
- client-side rendering gains one bounded recovery shell for index-load
  failures

## Risks

- scope could drift into retry logic, offline caching, or richer resilience
  behavior rather than staying on bounded recovery guidance
- recovery copy could become misleading if it implies the page can recover
  automatically when it cannot
- tests could overfit exact prose instead of meaningful load-failure behavior

## Follow-On Pressure

- later slices may decide whether stronger resilience such as retries or
  bundled fallback artifacts is warranted once the current failure mode is
  explicit
- release review should verify that the new recovery block improves search
  resilience without changing the current static-only hosting model
