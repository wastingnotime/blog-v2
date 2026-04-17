# Slice: 2026-04-17 Search Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic search-page discovery update for the expanded publication surface:

- revise the search page so it points readers toward the current complementary
  discovery routes
- add bounded affordances for Archives and Library alongside the existing
  client-side search interface
- keep the slice limited to search-page discovery copy and links

## Discovery Scope

The publication now exposes stable reader-facing discovery routes for search,
archives, and library. The search page still reflects its initial bootstrap
shape and behaves as an isolated widget surface with no complementary discovery
links.

That gap is visible in current repository artifacts:

- `build_search_page(...)` renders the search input, status, and results list,
  but no explicit affordance toward `/archives/` or `/library/`
- `/search/` is now a meaningful reader-facing route rather than a hidden
  bootstrap page
- archives and library are stable routes with shared-navigation discoverability,
  but the search page does not acknowledge them as alternate reading paths

This slice restores the minimum search discovery surface needed for the current
publication:

- update the search page so it links readers to `/archives/` and `/library/`
- preserve the existing client-side search behavior and static-index contract
- keep the change bounded to search-page discovery copy and links

This slice does not attempt ranking changes, query prefills, richer search UI,
or archive/library redesign.

## Use-Case Contract

### `BuildSearchPage`

Given site settings and the static search-index contract, generate
deterministic static output for `/search/` such that:

- the page continues to load and filter the existing `search.json` artifact
- readers can reach archives and library directly from the search page
- output remains fully static and compatible with GitHub Pages hosting

### `RenderSearchDiscovery`

Given the search route and current publication surfaces, render bounded
discovery content such that:

- the page still centers client-side search as its primary job
- archives and library are visibly represented as complementary discovery paths
- the section remains publication-oriented rather than turning into generic
  navigation chrome

## Main Business Rules

- Search-page discovery copy must stay aligned with the routes the publication
  now exposes.
- Search discovery affordances should point to stable reader-facing routes, not
  implementation artifacts.
- The slice stays bounded to search-page copy and linking rather than changing
  search indexing or shared navigation.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer
- environment reader for site settings
- existing stable routes for `/archives/`, `/library/`, and `/search/`

## Initial Test Plan

- unit test asserting the search page links directly to `/archives/` and
  `/library/`
- unit test asserting the existing search input and `search.json` reference
  remain present
- integration test asserting generated `dist/search/index.html` exposes the new
  search discovery affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/search/index.html` to verify:

- the search page still reads like a search surface
- the page links directly to archive and library discovery surfaces
- the existing client-side search interface remains unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- the search page aligns with the current publication discovery surface
- `/search/` exposes deterministic links to `/archives/` and `/library/`
- deterministic tests cover the new search affordances and unchanged
  static-only behavior
