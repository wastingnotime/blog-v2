# Slice: 2026-04-17 Twitter Card Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic social metadata in the shared document head:

- add bounded Twitter Card metadata to generated HTML pages
- derive metadata from existing page title, summary, canonical URL, and site
  settings
- keep the slice limited to metadata only, without social images

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, Open Graph metadata, `CNAME`, and `.nojekyll`. The next
publication-surface gap is platform-specific social metadata: generated pages
still lack bounded `twitter:*` tags in the shared head.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders `og:*` metadata through
  the shared document head but no `twitter:*` metadata
- unit and integration tests assert Open Graph behavior, yet there is no
  coverage for Twitter Card metadata on representative routes
- the earlier Open Graph slice explicitly deferred Twitter cards as a later
  bounded metadata concern

This slice restores the minimum Twitter Card surface needed for the current
publication:

- add shared `twitter:card`, `twitter:title`, `twitter:description`, and
  `twitter:url` metadata
- derive values deterministically from existing document metadata and site
  settings
- keep rendering consistent across homepage, sections, pages, and narrative
  routes

This slice does not attempt social preview images, account handles, section
artwork, or richer per-route media treatment.

## Use-Case Contract

### `ProjectTwitterCardMetadata`

Given site settings and a generated document, project Twitter Card data such
that:

- title and description reflect the existing document metadata
- URL matches the canonical publication URL
- card type stays bounded to one deterministic literal for the current static
  publication

### `RenderTwitterCardHead`

Given a generated HTML document and the shared head renderer, render the head
metadata such that:

- each generated HTML page includes the bounded `twitter:*` tags
- existing visible chrome and Open Graph behavior remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- Twitter Card metadata must be derived from existing deterministic site
  content and settings.
- The slice stays bounded to text and URL metadata, not social image
  generation or account-specific fields.
- `twitter:card` remains one deterministic literal across generated routes in
  this bootstrap slice.
- Metadata should remain consistent across all generated HTML routes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- environment reader for site settings
- shared document-head renderer
- existing page-level title, description, and canonical URL inputs

## Initial Test Plan

- unit test asserting generated HTML pages include bounded Twitter Card tags
- unit test asserting Twitter Card URLs use the configured static-site base URL
- unit test asserting the bounded `twitter:card` rule on representative route
  families
- integration test asserting homepage and representative content routes render
  the same Twitter metadata shape with route-specific title, description, and
  URL
- integration test asserting existing Open Graph and visible chrome behavior
  remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include Twitter Card metadata in
  `<head>`
- the metadata resolves to the existing canonical URLs and summaries
- the bounded `twitter:card` value stays consistent across the static
  publication surface
- visible navigation, footer, and Open Graph behavior remain unchanged
- the publication stays free of same-origin `/api` assumptions

## Done Criteria

- generated HTML pages expose deterministic bounded Twitter Card metadata
- metadata values derive from existing site settings and route content
- the bounded `twitter:card` rule is enforced consistently across generated
  HTML routes
- deterministic tests cover head metadata and unchanged visible chrome
