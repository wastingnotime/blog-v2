# Slice: 2026-04-17 Search Base Path Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic base-path alignment for the static search surface:

- remove the remaining root-relative search form target
- keep the search page aligned with the repository-wide `SITE_BASE_URL`
  contract
- stay bounded to search submission behavior and deterministic rendering

## Discovery Scope

The current static build already treats `SiteConfig.base_url` as the source of
truth for canonical URLs, navigation links, feed discovery, OpenSearch, the
search index fetch URL, and other generated assets. One inconsistent route
escape still remains on the search page itself.

That gap is explicit in current repository state:

- `src/app/domain/models/site_config.py` makes `base_url` part of the build
  configuration contract
- `src/app/application/use_cases/build_site.py` derives most publication URLs
  through `_absolute_url(config.base_url, ...)`
- `build_search_page(...)` still emits `action="/search/"`, which bypasses the
  configured base path during non-JavaScript submission or early browser
  navigation
- existing unit and integration tests currently codify that root-relative
  action, so the wrong contract is locked in by tests as well as renderer code

This slice restores the minimum base-path-safe search behavior needed for the
current publication:

- project the search form action from `SiteConfig.base_url`
- preserve current client-side query-state behavior and static search index
  loading
- keep the slice limited to search-route submission alignment rather than a
  broader routing rewrite

This slice does not introduce server-side search, change search ranking, alter
search result rendering, or redesign shared navigation.

## Use-Case Contract

### `BuildSearchPage`

Given site settings and the static search route, generate deterministic output
for `/search/` such that:

- the rendered form action resolves to the configured search route under
  `SiteConfig.base_url`
- the page remains fully functional as a static document when JavaScript is
  unavailable
- the existing client-side search enhancement continues to work unchanged once
  the page loads

### `RenderSearchSubmissionTarget`

Given the repository-wide base URL contract and the stable search route, render
the search submission target such that:

- the action never assumes deployment at origin root
- the target remains deterministic across local tests and GitHub Pages-style
  prefixed hosting
- the rendered route stays aligned with the canonical search URL

## Main Business Rules

- The search page must honor the same `SiteConfig.base_url` contract as the
  rest of the generated publication.
- Non-JavaScript form submission must land on the configured `/search/` route
  without assuming origin-root hosting.
- The slice stays bounded to route-target alignment and must not expand into a
  broader client router or application-shell change.
- Existing search query URL-state behavior remains part of the current
  contract.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- `SiteConfig.base_url`
- existing search page renderer in `src/app/application/use_cases/build_site.py`
- existing `_absolute_url(...)` path projection
- deterministic unit and integration tests for generated HTML

## Initial Test Plan

- unit test asserting search page form action derives from `SiteConfig.base_url`
- unit test asserting a prefixed base URL such as
  `https://example.com/blog/` renders a prefixed search action target
- integration test asserting scenario output keeps the search form aligned with
  the configured base URL
- regression test asserting existing client-side search index loading and query
  URL-state behavior remain unchanged
- regression test asserting generated output remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI with a prefixed base URL such as
`SITE_BASE_URL=https://example.com/blog/` and inspect `dist/search/index.html`
to verify:

- the form action targets `https://example.com/blog/search/`
- the canonical URL, search index fetch URL, and form action all describe the
  same published search route
- typing still updates the query string on the prefixed route
- the artifact remains fully static and GitHub Pages compatible

## Done Criteria

- the rendered search form action derives from `SiteConfig.base_url`
- prefixed deployments keep search submission on the published static route
- existing client-side search behavior remains intact
- deterministic tests cover both root-hosted and prefixed-base-url search
  rendering
