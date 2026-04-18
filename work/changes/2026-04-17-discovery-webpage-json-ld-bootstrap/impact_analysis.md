# Impact Analysis

## Summary

The next slice should extend the current structured-data contract from homepage
and article-like routes to the stable top-level discovery hubs that already act
as reader-facing pages in the static publication.

Current observed gap:

- the build already emits deterministic JSON-LD for homepage, standalone pages,
  and episodes
- `/archives/`, `/search/`, `/library/`, `/sagas/`, and `/studio/` now expose
  stable authored titles, summaries, canonical URLs, and shared navigation, but
  still emit no JSON-LD
- topic pages, saga detail pages, and arc detail pages exist too, but their
  machine-readable semantics are still less explicit, so widening into them now
  would push the slice into schema design rather than bounded projection

## Impacted Areas

- shared structured-data projection in
  `src/app/application/use_cases/build_site.py`
- route builders for archives, search, library, sagas, and studio
- deterministic unit and integration coverage for JSON-LD on non-article routes
- existing assertions that representative structural routes emit no JSON-LD

## Boundary Change

The static build does not gain new routes, hosting behavior, or runtime
dependencies. Instead, it broadens the machine-readable publication contract on
selected existing routes:

- homepage stays `WebSite`
- standalone pages and episodes stay `Article`
- top-level discovery hubs gain bounded `WebPage`
- recovery and more semantically ambiguous structural routes stay unchanged

## Risks

- the slice could drift into route-by-route schema specialization instead of
  staying with one generic `WebPage` contract
- structured-data fields could diverge from existing canonical, title, and
  description metadata if route values are duplicated in too many places
- tests could overfit exact JSON ordering instead of the intended schema
  payload

## Follow-On Pressure

- later slices may decide whether topic pages, saga detail pages, and arc
  detail pages justify `CollectionPage`, `CreativeWorkSeries`, or other richer
  schema types
- release review should verify that homepage, article, and discovery-hub
  structured data still present one coherent publication contract alongside
  canonical tags, social metadata, feed output, and sitemap output
