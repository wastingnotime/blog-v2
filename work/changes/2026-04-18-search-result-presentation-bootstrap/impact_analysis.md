# Impact Analysis

## Summary

The next coherent slice is to give rendered search results an explicit
row-presentation contract so `/search/` feels consistent with the rest of the
refined publication surfaces.

Current observed gap:

- `/search/` already has the right static behavior, semantics, ranking, and
  recovery
- the browser-side result rows still render through plain generic DOM output
- the route therefore works functionally but still looks weaker than the other
  refined navigation surfaces

## Impacted Areas

- generated search-page script in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded search-result treatment
- deterministic search-page assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or search data. The boundary change is
limited to result presentation on `/search/`:

- rendered results get one explicit result-row markup contract
- ranking, highlighting, tag surfacing, and recovery remain unchanged
- shared discovery and studio-specific surfaces remain unchanged

## Risks

- scope could drift into changing ranking or query behavior instead of staying
  on presentation
- CSS hooks could accidentally affect non-search surfaces if selectors are not
  kept bounded
- tests could overfit incidental script text instead of meaningful result-row
  behavior

## Follow-On Pressure

- later slices may decide whether search recovery or empty states need richer
  copy once the core result surface is explicit
- release review should verify that search now feels visually integrated
  without changing search behavior
