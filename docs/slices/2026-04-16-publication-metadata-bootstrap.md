# Slice: 2026-04-16 Publication Metadata Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed content source under repository control

## Architecture Mode

Static-site builder with machine-readable publication projections:

- project a bounded syndication feed from repository-authored content
- project a sitemap from generated static routes and content metadata
- keep publication metadata generation deterministic and base-URL aware

## Discovery Scope

The current slices restore the human-facing publication surface, but `blog-v2`
still emits only HTML pages. The old `../blog` also exposed machine-readable
publication artifacts, notably `feed.xml` and `sitemap.xml`, which matter for
readers, feed consumers, and search engines.

This slice restores the minimum publication metadata needed to make the static
site discoverable and syndication-friendly:

- generate a feed from recent standalone pages and saga episodes
- generate a sitemap from the built static route set
- derive canonical absolute URLs from the configured base URL

This slice does not attempt Atom support, robots.txt, search indexing policy,
manual priorities, or richer SEO metadata beyond feed and sitemap output.

## Use-Case Contract

### `BuildPublicationFeed`

Given site settings and the content catalog, generate deterministic static
output for `/feed.xml` such that:

- the feed contains recent published entries from repository-authored content
- each item uses an absolute canonical URL derived from `SITE_BASE_URL`
- item ordering is deterministic and repository-derived
- the feed remains valid when the site is hosted as static files only

### `BuildSitemap`

Given site settings, generated route metadata, and content metadata, generate
deterministic static output for `/sitemap.xml` such that:

- the sitemap lists the main generated routes that should be discoverable
- each URL uses an absolute canonical URL derived from `SITE_BASE_URL`
- content-backed routes include a deterministic `lastmod` value when available
- the sitemap requires no runtime service to resolve route state

### `ProjectPublicationEntries`

Given pages, sagas, arcs, episodes, and section routes, compute deterministic
publication metadata for:

- feed entries ordered by content recency and bounded to a stable limit
- sitemap entries covering human-facing generated routes
- last-modified dates derived from repository metadata rather than filesystem
  timestamps

## Main Business Rules

- Publication metadata must be derived from repository-authored content and
  generated routes, not handwritten duplicate manifests.
- `feed.xml` should include reader-relevant published content entries, not
  purely structural hub pages.
- `sitemap.xml` may include structural routes such as section hubs when they
  are real generated destinations.
- Absolute URLs must respect the configured base URL and stay compatible with
  GitHub Pages hosting.
- Publication metadata generation must remain fully static and deterministic.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for content sources
- filesystem writer for build artifacts
- environment reader for site settings

## Initial Test Plan

- unit test for deterministic feed entry projection and limiting
- unit test for sitemap entry projection with stable `lastmod` values
- integration test for generating:
  - `dist/feed.xml`
  - `dist/sitemap.xml`
- integration test asserting generated publication metadata uses absolute URLs
  from the configured base URL
- integration test asserting generated output stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
artifacts to verify:

- `feed.xml` includes recent entries with titles, summaries, dates, and
  absolute links
- `sitemap.xml` includes the main generated routes with stable canonical URLs
- content-backed routes expose repository-derived `lastmod` values where
  available
- both files remain valid static artifacts with no application server

## Done Criteria

- the build generates `/feed.xml` and `/sitemap.xml`
- feed items are ordered deterministically and use absolute canonical URLs
- sitemap entries reflect generated static routes with deterministic metadata
- deterministic tests cover projection and generated publication metadata
