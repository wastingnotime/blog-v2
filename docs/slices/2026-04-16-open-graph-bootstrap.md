# Slice: 2026-04-16 Open Graph Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic social metadata in the shared document head:

- add bounded Open Graph metadata to generated HTML pages
- derive metadata from existing page title, summary, canonical URL, and site
  settings
- keep the slice limited to metadata only, without social images

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, search metadata, and footer attribution. The next publication
surface gap is social link unfurl metadata: generated pages still lack bounded
Open Graph tags for title, description, type, and canonical URL.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders canonical, RSS, and
  identity-asset head metadata but no `og:*` tags
- generated `dist/index.html` includes the shared static head metadata and
  likewise contains no Open Graph metadata

This slice restores the minimum Open Graph surface needed for the current
publication:

- add shared `og:title`, `og:description`, `og:type`, `og:url`, and
  `og:site_name` metadata
- derive values deterministically from existing page data and site settings
- keep rendering consistent across homepage, sections, pages, and narrative
  routes

This slice does not attempt social preview images, Twitter cards, section-level
custom artwork, or richer per-route media treatment.

## Use-Case Contract

### `ProjectOpenGraphMetadata`

Given site settings and a generated document, project Open Graph data such
that:

- title and description reflect the existing document metadata
- URL matches the canonical publication URL
- type stays bounded as `website` for all routes in this bootstrap slice
- site name remains stable for the configured publication

### `RenderOpenGraphHead`

Given a generated HTML document and the shared head renderer, render the head
metadata such that:

- each generated HTML page includes the bounded Open Graph tags
- existing visible chrome and active-state behavior remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- Open Graph metadata must be derived from existing deterministic site content
  and settings.
- The slice stays bounded to text and URL metadata, not social image
  generation.
- `og:type` remains the single literal value `website` in this slice so build
  can ship deterministic metadata without inventing per-route social semantics.
- Metadata should remain consistent across all generated HTML routes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- environment reader for site settings
- shared document-head renderer
- existing page-level title, description, and canonical URL inputs

## Initial Test Plan

- unit test asserting generated HTML pages include bounded Open Graph tags
- unit test asserting Open Graph URLs use the configured static-site base URL
- unit test asserting `og:type` remains `website` on homepage, section, page,
  saga, and episode routes
- integration test asserting homepage and representative content routes render
  the same metadata shape with route-specific title, description, and URL
- integration test asserting visible chrome behavior remains unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include Open Graph metadata in
  `<head>`
- the metadata resolves to the existing canonical URLs and summaries
- `og:type` stays `website` across the bounded static publication surface
- visible navigation and footer behavior remain unchanged
- the publication stays free of same-origin `/api` assumptions

## Done Criteria

- generated HTML pages expose deterministic bounded Open Graph metadata
- metadata values derive from existing site settings and route content
- the bounded `og:type=website` rule is enforced consistently across generated
  HTML routes
- deterministic tests cover head metadata and unchanged visible chrome
