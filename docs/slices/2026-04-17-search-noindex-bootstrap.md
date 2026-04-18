# Slice: 2026-04-17 Search Noindex Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic route-specific crawl metadata for the static search surface:

- keep shared robots metadata for normal reader-facing publication routes
- project one bounded `noindex,follow` contract onto the generated `/search/`
  page
- keep the slice limited to search-route metadata semantics rather than search
  ranking, result UI, or broader SEO configuration

## Discovery Scope

The restored static publication now exposes `/search/` as a stable utility
route with:

- a generated search page under the shared site frame
- homepage `WebSite` JSON-LD that points search entry at
  `/search/?q={search_term_string}`
- browser-side URL-state behavior that keeps the current query aligned with the
  same optional `?q=` contract

One route-semantics mismatch is still visible in the current repository state:
the search route now owns shareable query-string state, but it still inherits
the same indexable robots contract as durable publication pages.

Current repository evidence confirms that gap:

- `build_search_page(...)` renders a utility surface that loads `search.json`
  client-side and treats `?q=` as route-level session state rather than as a
  family of authored documents
- `_render_document(...)` still defaults routes to
  `<meta name="robots" content="index,follow" />`
- `build_search_page(...)` keeps the canonical URL fixed at `/search/`, which
  already signals that query variants are not distinct canonical pages
- `2026-04-17-404-noindex-bootstrap` already established that route-specific
  robots metadata should distinguish utility surfaces from durable
  reader-facing content

This slice restores the minimum crawl-semantics coherence needed for the
current static publication:

- keep `/search/` available to readers and linked from the publication
- render `/search/` with `noindex,follow`
- preserve homepage `SearchAction`, canonical `/search/`, and the current
  static search behavior without widening into search product work

This slice does not attempt broader robots policy settings, environment-
specific SEO configuration, richer search behavior, or route taxonomy beyond
the generated search page.

## Use-Case Contract

### `ProjectRouteRobotsPolicy`

Given the generated route kind, project robots metadata such that:

- durable publication routes keep the current `index,follow` contract
- the generated `/search/` route uses `noindex,follow`
- the same repository state yields the same robots directives for the same
  route kind

### `RenderSearchRobotsMetadata`

Given the generated search page and shared document renderer, render metadata
such that:

- `/search/` includes one explicit `noindex,follow` robots tag
- canonical metadata remains rooted at `/search/` rather than any query string
- homepage `SearchAction`, shared navigation, and the static `search.json`
  contract remain unchanged

## Main Business Rules

- The static publication should invite indexing of durable reading routes, but
  the search utility route should not present itself as indexable content.
- Search query state on `/search/` remains optional reader session state, not a
  canonical document family.
- Route-specific robots metadata must be deterministic and derived by the
  build, not maintained through handwritten post-processing.
- The slice stays bounded to search-route crawl semantics rather than changing
  search ranking, result rendering, or shared navigation.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer in `src/app/application/use_cases/build_site.py`
- route-specific metadata projection for generated pages
- existing search-page generation path and canonical `/search/` contract

## Initial Test Plan

- unit test asserting representative durable publication routes still render
  `index,follow`
- unit test asserting `/search/` renders `noindex,follow` while preserving the
  canonical `/search/` tag and `search.json` reference
- integration test asserting generated `dist/search/index.html` carries the new
  robots contract without regressing the existing search-page behavior
- integration test asserting homepage `SearchAction` remains unchanged so the
  site still advertises search entry without making the search route itself
  indexable

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- `dist/search/index.html` includes
  `<meta name="robots" content="noindex,follow" />`
- the same page still keeps canonical `/search/`, the existing `search.json`
  reference, and the bounded `?q=` URL-state behavior
- representative publication routes such as homepage, archives, and content
  pages remain `index,follow`
- homepage structured data still points search entry at
  `/search/?q={search_term_string}`

## Done Criteria

- the build projects deterministic route-specific robots metadata for
  `/search/`
- `/search/` renders `noindex,follow` without changing its canonical or
  client-side search contract
- representative durable publication routes remain `index,follow`
- deterministic tests cover the bounded distinction without widening the slice
  into broader SEO or search work
