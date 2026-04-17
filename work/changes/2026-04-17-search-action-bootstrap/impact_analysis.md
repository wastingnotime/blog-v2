# Impact Analysis

## Summary

The next coherent slice after the bounded JSON-LD work is to connect the
homepage `WebSite` schema to the already-published static search route through
one explicit search-entry contract.

Current observed gap:

- homepage structured data now exists, but it does not yet advertise the
  site's own search entry point
- `/search/` exists and filters `search.json`, but it does not hydrate from a
  stable `?q=` URL contract
- that leaves the machine-readable site-search story incomplete even though the
  repository already has the necessary static search surface

## Impacted Areas

- homepage structured-data projection in
  `src/app/application/use_cases/build_site.py`
- generated search-page client script and its deterministic initial state
- unit and integration coverage for JSON-LD and search-page behavior

## Boundary Change

The static build does not gain new routes, backend services, or a new search
index. Instead, it tightens the existing publication contract between homepage
metadata and `/search/`:

- homepage `WebSite` JSON-LD gains one bounded `SearchAction`
- `/search/` accepts a deterministic `?q=` entry shape on first load
- canonical route behavior stays centered on `/search/` rather than per-query
  documents

## Risks

- scope could drift into richer search product work such as ranking,
  suggestions, or multi-filter UI instead of staying on the entry contract
- the structured-data target and the search-page query handling could drift if
  the `?q=` shape is duplicated rather than treated as one shared contract
- tests could overfit exact script formatting instead of asserting the
  meaningful query-hydration behavior

## Follow-On Pressure

- later slices may decide whether additional schema work such as
  `BreadcrumbList`, saga-level structured data, or search-page-specific
  structured data is worthwhile
- release review should verify that homepage JSON-LD, search-page behavior, and
  canonical metadata still describe one coherent static search surface
