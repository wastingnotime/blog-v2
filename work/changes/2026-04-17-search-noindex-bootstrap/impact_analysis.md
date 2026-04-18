# Impact Analysis

## Summary

The next coherent slice after `2026-04-17-search-url-state-bootstrap` is to
correct crawl semantics for the now-shareable `/search/` utility route.

Current observed gap:

- `/search/` now reads and writes a bounded `?q=` contract
- the route still behaves as a client-side utility surface backed by
  `search.json`, not as a durable authored content page
- the shared document renderer still gives `/search/` the same
  `index,follow` robots metadata used for homepage, archives, and authored
  entries

That leaves one bounded mismatch in the current publication model: the site now
allows shareable search-state URLs while still advertising the search utility
route itself as indexable publication content.

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- route-specific robots metadata projection for generated pages
- search-page generation and deterministic test coverage for route-specific
  crawl semantics

## Boundary Change

The build does not gain new routes, search behavior, or configuration surfaces.
Instead, one existing shared metadata contract becomes route-aware:

- `/search/` should render `noindex,follow`
- durable publication routes should keep `index,follow`
- canonical `/search/` and homepage `SearchAction` should remain unchanged

## Risks

- scope could drift into a broader SEO settings system instead of staying
  bounded to the search-route distinction
- tests could overfit head ordering instead of asserting the intended robots
  policy and unchanged search contract
- a later renderer change could collapse route-specific robots handling back
  into one shared default if the distinction is not made explicit

## Follow-On Pressure

- later slices may decide whether other utility routes deserve similar
  treatment once the publication surface stabilizes further
- release review should verify that `robots.txt`, canonical URLs, homepage
  `SearchAction`, and route-specific robots metadata still describe one
  coherent static search contract
