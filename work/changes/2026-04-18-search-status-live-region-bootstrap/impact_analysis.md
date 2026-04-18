# Impact Analysis

## Summary

The next coherent slice is to give the existing search status surface explicit
live-region semantics so dynamic result feedback is more clearly modeled.

Current observed gap:

- `/search/` now has stable form semantics, result rendering, and recovery
  behavior
- `#search-status` already updates as queries change, but it has no explicit
  live-region contract
- the page therefore keeps a weaker dynamic feedback contract than the rest of
  the search surface

## Impacted Areas

- generated search-page markup in `src/app/application/use_cases/build_site.py`
- deterministic reader-facing status semantics on `/search/`
- unit and integration coverage for search-status markup

## Boundary Change

The build gains no new route, artifact, or backend dependency. The boundary
change is limited to status semantics inside the existing static search page:

- `/search/` stays the canonical route
- `search.json` stays the only search artifact
- page markup gains one bounded live-region contract for the existing status
  element

## Risks

- scope could drift into broader accessibility redesign rather than staying on
  bounded status semantics
- tests could overfit exact attribute choices instead of the meaningful
  live-region contract

## Follow-On Pressure

- later slices may decide whether result focus management or additional
  accessibility affordances are warranted once the current status contract is
  explicit
- release review should verify that the new semantics clarify the current search
  feedback surface without changing the static-only hosting model
