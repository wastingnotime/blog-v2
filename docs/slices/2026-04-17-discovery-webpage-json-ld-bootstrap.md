# Slice: 2026-04-17 Discovery WebPage JSON-LD Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic structured metadata for stable discovery hubs:

- extend the current shared document-head JSON-LD support to selected
  reader-facing hub routes
- keep the metadata bounded to one generic schema shape that matches the
  current publication truth
- avoid route-specific schema taxonomies until the repository has stronger
  semantic evidence for them

## Discovery Scope

The current publication already emits deterministic JSON-LD on the homepage and
article-like routes:

- homepage emits `WebSite`
- standalone pages emit `Article`
- episode pages emit `Article`

Current repository evidence also shows a remaining machine-readable gap on the
stable discovery hubs:

- `src/app/application/use_cases/build_site.py` projects JSON-LD only for
  homepage, standalone pages, and episodes
- `/archives/`, `/search/`, `/library/`, `/sagas/`, and `/studio/` are now
  durable reader-facing routes with authored titles, summaries, canonical URLs,
  shared navigation, and deterministic static output
- tests currently assert that representative structural routes emit no JSON-LD,
  which was correct for the earlier bounded slice but no longer reflects the
  maturity of the top-level discovery surface

This slice restores the next bounded machine-readable layer that fits the
current publication:

- emit one deterministic `WebPage` JSON-LD payload for the stable top-level
  discovery hubs
- keep the payload aligned with existing route title, summary, and canonical
  URL metadata
- leave topic pages, saga detail pages, arc detail pages, and `404.html`
  unchanged until their route semantics are refined more explicitly

This slice does not attempt breadcrumbs, search-result schema, collection-item
enumeration, organization profiles, topic taxonomies, or a generalized schema
registry.

## Use-Case Contract

### `ProjectDiscoveryRouteStructuredData`

Given the route kind, site settings, and existing repository-authored route
metadata, project structured data such that:

- `/archives/`, `/search/`, `/library/`, `/sagas/`, and `/studio/` receive one
  deterministic `WebPage` payload
- the payload derives from existing title, summary, and canonical URL values
- unsupported route classes continue to emit no JSON-LD in this slice

### `RenderStructuredDataScript`

Given a structured-data payload for an eligible discovery route, render one
`<script type="application/ld+json">` block such that:

- the JSON is deterministic for the same repository state
- canonical absolute URLs derive from `SITE_BASE_URL`
- route titles and descriptions stay aligned with the existing HTML metadata
- the slice stays bounded to head metadata only

## Main Business Rules

- Structured data for discovery hubs must derive from repository-authored route
  metadata, not handwritten per-page JSON snippets.
- The stable top-level discovery routes should expose one bounded `WebPage`
  contract because they are reader-facing pages, but they do not yet justify
  richer schema specialization.
- Homepage `WebSite` JSON-LD and article-route `Article` JSON-LD remain
  unchanged.
- `404.html` remains free of structured data because it is a recovery surface
  and already carries `noindex,follow`.
- Topic pages, saga detail pages, and arc detail pages remain out of scope
  until the repository makes their machine-readable semantics explicit.
- JSON-LD output must remain static, deterministic, and GitHub Pages
  compatible.

## Required Ports

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- existing route builders for archives, search, library, sagas, and studio
- site settings and canonical URL helpers
- deterministic JSON serialization used by the current structured-data renderer

## Initial Test Plan

- unit test asserting `/archives/`, `/search/`, `/library/`, `/sagas/`, and
  `/studio/` render one `WebPage` JSON-LD block with deterministic canonical
  URLs
- unit test asserting homepage `WebSite` JSON-LD and article-route `Article`
  JSON-LD remain unchanged
- unit test asserting `404.html`, topic pages, saga detail pages, and arc
  detail pages still render no JSON-LD block
- integration test asserting scenario output contains `WebPage` JSON-LD on the
  stable top-level discovery hubs without changing the rest of the publication
  metadata contract

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- `dist/archives/index.html`, `dist/search/index.html`, `dist/library/index.html`,
  `dist/sagas/index.html`, and `dist/studio/index.html` each contain one
  `application/ld+json` script
- each payload uses `@type: WebPage` and resolves its `url` to the configured
  canonical route
- homepage and representative article routes keep their existing JSON-LD shape
- `dist/404.html` and representative topic or saga-detail routes remain
  unchanged outside this bounded discovery-hub addition

## Done Criteria

- the build projects deterministic `WebPage` JSON-LD for the stable top-level
  discovery hubs
- existing homepage and article-route structured-data behavior remains
  unchanged
- `404.html`, topic pages, saga detail pages, and arc detail pages remain out
  of scope
- deterministic tests cover the new discovery-hub contract without widening the
  slice into richer schema strategy work
