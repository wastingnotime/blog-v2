# Impact Analysis

## Summary

The next coherent slice after `2026-04-17-search-action-bootstrap` is to make
the generated search page produce the same `?q=` contract it now consumes.

Current observed gap:

- homepage `WebSite` JSON-LD now advertises `/search/?q={search_term_string}`
- `/search/` now hydrates from `?q=` on first load
- once a reader types a new query, the page filters results in place but leaves
  the browser URL behind

That creates one bounded mismatch in the current static search model: the site
can advertise and accept a deterministic search-entry URL, but the page itself
does not maintain that contract during actual searching.

## Impacted Areas

- generated search-page markup in `src/app/application/use_cases/build_site.py`
- browser-side query-string and history handling for `/search/`
- unit and integration coverage for search-route URL-state behavior

## Boundary Change

The static build does not gain new routes, backend services, or per-query
documents. Instead, it tightens the existing `/search/` contract:

- `/search/` still remains the canonical route
- `?q=` remains optional reader session state on that route
- the page gains deterministic behavior to keep interactive search and browser
  URL state aligned

## Risks

- scope could drift into richer search product work such as ranking,
  suggestions, or result highlighting instead of staying on URL-state
  coherence
- URL handling could accidentally make per-query pages look canonical if the
  slice does not preserve the current canonical-path rule
- tests could overfit exact script formatting instead of asserting the
  meaningful query-state behavior

## Follow-On Pressure

- later slices may decide whether search-page-specific structured data,
  suggestions, or richer result treatment are worthwhile once the URL contract
  is fully coherent
- release review should verify that homepage `SearchAction`, `/search/`
  behavior, and canonical metadata still describe one consistent static search
  surface
