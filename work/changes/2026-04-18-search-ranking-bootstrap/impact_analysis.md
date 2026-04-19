# Impact Analysis

## Summary

The static search route now ranks matching results intentionally instead of
returning them in incidental catalog order.

Current observed contract:

- `/search/` exists and shares a stable `?q=` contract
- matching records are ordered by explicit match strength rather than source
  order
- the search experience has a deterministic search-result contract

## Impacted Areas

- generated search-page script in `src/app/application/use_cases/build_site.py`
- deterministic reader-facing result ordering on `/search/`
- unit and integration coverage for search-result behavior

## Boundary Change

The build already carries the route and artifact. The boundary stays limited
to result-ordering semantics inside the existing static search page:

- `/search/` stays the canonical route
- `search.json` stays the only search artifact
- client-side filtering gains one bounded ranking contract for how matches are
  ordered once found

## Risks

- scope could drift into fuzzy search, suggestions, or result highlighting
  rather than staying on bounded ordering behavior
- ranking rules could become opaque if the slice does not keep match-strength
  priorities explicit and deterministic
- tests could overfit exact script text instead of meaningful ranking outcomes

## Follow-On Pressure

- later slices may decide whether richer search behavior such as suggestions,
  highlighting, or typo tolerance is warranted once ordering is explicit
- release review should verify that search ranking improves discovery without
  changing the current static-only hosting model
