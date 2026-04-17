# Slice: 2026-04-17 JSON-LD Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic structured publication metadata projected into static HTML:

- keep the current shared document-head and publication metadata model
- add one bounded JSON-LD projection for routes that already carry strong
  repository-authored publication meaning
- keep the slice limited to machine-readable metadata rather than broader SEO,
  search, or navigation changes

## Discovery Scope

The current publication surface now exposes the main static-site discovery
artifacts:

- canonical absolute URLs in document heads
- `feed.xml`
- `sitemap.xml`
- RSS autodiscovery
- Open Graph and Twitter metadata
- route-specific robots metadata so `404.html` is `noindex,follow`

One machine-readable metadata gap remains. The generated HTML does not yet
project structured data for search engines or other schema-aware consumers.
Current repository evidence confirms that gap:

- `build_site.py` renders canonical, social, manifest, browserconfig, and
  robots metadata in the shared document head, but it does not emit any
  `application/ld+json` script
- the repository already has stable route metadata for homepage, standalone
  pages, and episodes, including canonical URLs, titles, summaries, dates, and
  entry metadata such as reading time and tags
- the `404 noindex` slice restored route-specific crawl semantics, which means
  the publication-discovery contract is now internally consistent enough to add
  structured metadata without first revisiting route eligibility

This slice restores the minimum structured-data layer that matches the current
static publication:

- homepage emits bounded `WebSite` JSON-LD
- standalone pages and episode pages emit bounded `Article` JSON-LD
- route classes without clear publication semantics yet, such as `404.html`,
  search, archives, section hubs, saga index pages, and topic listings, remain
  unchanged for now

This slice does not attempt breadcrumbs, `SearchAction`, saga-level schema,
organization/person profiles beyond the current author surface, review/rating
schema, or a generalized schema registry.

## Use-Case Contract

### `ProjectStructuredData`

Given the route kind, site settings, and existing repository-authored content
metadata, project structured data such that:

- homepage routes receive a deterministic `WebSite` payload
- standalone page routes receive a deterministic `Article` payload
- episode routes receive a deterministic `Article` payload
- unsupported route classes receive no JSON-LD

### `RenderStructuredDataScript`

Given a structured-data payload for an eligible route, render one
`<script type="application/ld+json">` block such that:

- the JSON is deterministic for the same repository state
- canonical absolute URLs derive from `SITE_BASE_URL`
- title, summary, publication date, and author/site naming stay aligned with
  the existing HTML metadata contract
- the slice stays bounded to head metadata only

## Main Business Rules

- Structured data must be derived from repository-authored publication
  metadata, not from handwritten per-page JSON snippets.
- The homepage should advertise the site-level publication identity through
  `WebSite` JSON-LD.
- Standalone pages and episode pages should advertise themselves as published
  written content through `Article` JSON-LD.
- `404.html` must remain free of structured data because it is a recovery
  surface and is already explicitly `noindex,follow`.
- Search, archive, saga index, topic listing, and other structural routes stay
  out of scope until the repository decides which schema types actually express
  their business meaning.
- JSON-LD output must remain static, deterministic, and GitHub Pages
  compatible.

## Required Ports

- shared document-head rendering in `build_site.py`
- existing page and episode metadata projection
- site settings and canonical URL helpers

## Initial Test Plan

- unit test asserting homepage renders one `WebSite` JSON-LD block with the
  configured canonical base URL
- unit test asserting standalone pages and episodes render `Article` JSON-LD
  with deterministic title, description, publication date, and canonical URL
- unit test asserting `404.html` and representative structural routes still
  render no JSON-LD block
- integration test asserting scenario output contains valid
  `application/ld+json` scripts on homepage and one content route without
  changing the rest of the publication metadata contract

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- `dist/index.html` contains one `WebSite` JSON-LD script whose URL resolves to
  the configured base URL
- representative content routes such as `/about/` and one episode route contain
  one `Article` JSON-LD script with repository-derived title, summary, and
  publication date fields
- `dist/404.html` contains no JSON-LD script
- canonical tags, social metadata, feed output, sitemap output, and route-
  specific robots metadata remain unchanged outside the bounded structured-data
  addition

## Done Criteria

- the build projects deterministic JSON-LD for homepage and content-backed
  article routes
- homepage emits bounded `WebSite` JSON-LD
- standalone pages and episodes emit bounded `Article` JSON-LD
- `404.html` and representative structural routes remain unchanged
- deterministic tests cover the new structured-data contract without widening
  the slice into broader SEO strategy work
