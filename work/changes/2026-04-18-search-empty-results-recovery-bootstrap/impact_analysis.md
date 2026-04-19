# Impact Analysis

## Summary

The next coherent slice is to make zero-result searches recoverable by adding
bounded in-page guidance when the current query yields no matches.

Current observed gap:

- `/search/` now supports ranking, highlighting, tag visibility, and no-script
  recovery
- zero-match queries still produce only a plain status message
- the reader gets failure feedback, but no next step beyond manually changing
  the query

## Impacted Areas

- generated search-page script in `src/app/application/use_cases/build_site.py`
- deterministic reader-facing zero-results behavior on `/search/`
- unit and integration coverage for search-route recovery guidance

## Boundary Change

The build gains no new route, artifact, or backend dependency. The boundary
change is limited to zero-results recovery inside the existing static search
page:

- `/search/` stays the canonical route
- `search.json` stays the only search artifact
- client-side rendering gains one bounded recovery shell for queries with no
  matches

## Risks

- scope could drift into alternative-query suggestions or richer search-product
  behavior rather than staying on bounded recovery guidance
- recovery copy could become misleading if it implies the site can suggest
  better queries automatically when it cannot
- tests could overfit exact prose instead of meaningful zero-results behavior

## Follow-On Pressure

- later slices may decide whether stronger recovery behaviors such as related
  query hints are warranted once the current empty-results path is explicit
- release review should verify that the new recovery block improves search
  resilience without changing the current static-only hosting model
