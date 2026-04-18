# Impact Analysis

## Summary

The next coherent slice is to make the existing static search route explicit
about its client-side execution requirement and provide a bounded no-script
recovery path.

Current observed gap:

- `/search/` now supports query URLs, ranking, highlighting, and tag surfacing
- actual filtering still depends on browser-side script execution
- the page currently gives no direct explanation or recovery guidance when
  script execution is unavailable

## Impacted Areas

- generated search-page markup in `src/app/application/use_cases/build_site.py`
- deterministic reader-facing fallback behavior on `/search/`
- unit and integration coverage for search-route recovery guidance

## Boundary Change

The build gains no new route, artifact, or backend dependency. The boundary
change is limited to recovery messaging inside the existing static search page:

- `/search/` stays the canonical route
- `search.json` stays the only search artifact
- page markup gains one bounded `<noscript>` recovery contract for readers
  without script execution

## Risks

- scope could drift into server-side or prerendered search behavior rather than
  staying on bounded recovery guidance
- fallback copy could become misleading if it implies the site has a search
  backend when it does not
- tests could overfit exact prose instead of meaningful no-script behavior

## Follow-On Pressure

- later slices may decide whether broader progressive enhancement or script-free
  recovery paths are warranted once the current limitation is made explicit
- release review should verify that the new guidance clarifies the current
  static-only search contract without changing hosting assumptions
