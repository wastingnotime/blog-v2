# Impact Analysis

## Summary

The next coherent slice is to give rendered search results a dedicated row
shell so `/search/` feels as intentional as the rest of the publication's
editorial surfaces.

Current observed gap:

- `/search/` already has the right static behavior, semantics, ranking, and
  recovery
- the browser-side result rows still sit in plain list items without a
  dedicated row shell
- the title and metadata still read as stacked elements instead of one compact
  header line inside the shell
- the result surface therefore works functionally but still looks flatter than
  the refined navigation surfaces elsewhere on the site

## Impacted Areas

- generated search-page CSS in `src/app/application/use_cases/build_site.py`
- deterministic reader-facing result rendering on `/search/`
- unit and integration coverage for search-result row presentation

## Boundary Change

The build gains no new route, runtime, or search data. The boundary change is
limited to result presentation on `/search/`:

- rendered results gain one explicit row-shell contract
- the result header becomes one compact inline row inside that shell
- ranking, highlighting, tag surfacing, and recovery remain unchanged
- shared discovery and studio-specific surfaces remain unchanged

## Risks

- scope could drift into changing ranking or query behavior instead of staying
  on presentation
- CSS hooks could accidentally affect non-search surfaces if selectors are not
  kept bounded
- tests could overfit incidental script text instead of meaningful row-shell
  behavior

## Follow-On Pressure

- later slices may decide whether the search page needs richer recovery copy
  once the core result surface is explicit
- release review should verify that search now feels visually integrated
  without changing search behavior
