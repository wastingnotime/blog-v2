# Slice: 2026-04-17 Author Meta Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic author metadata in the shared document head:

- add one bounded `author` contract to generated HTML pages
- align that metadata with the publication's existing shared identity
- keep the slice limited to metadata only, without adding per-entry authoring

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, manifest links, Open Graph metadata, Twitter Card metadata,
shared social preview image support, theme-color, Apple mobile-web-app
metadata, format-detection metadata, referrer metadata, color-scheme
metadata, application-name metadata, viewport-fit metadata, and Windows tile
color metadata. The next small browser-facing head gap is authorship
signaling: generated HTML pages still omit `meta name="author"` even though the
publication already presents a stable site-level identity.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders the shared document
  head without `meta name="author"`
- the current build contract is still publication-level rather than per-entry
  author modeling, so the next slice should stay bounded to one shared author
  literal instead of inventing route-specific bylines
- the GitHub Pages deployment target keeps the site static, so the next slice
  should remain a deterministic head-metadata improvement only

This slice restores the minimum explicit author surface needed for the current
publication:

- add one shared `meta name="author"` tag to generated HTML pages
- derive the value from the existing site-level publication identity
- keep the value stable across homepage, sections, pages, and narrative routes

This slice does not attempt per-entry author metadata, bios, contributor
models, or visible byline redesign.

## Use-Case Contract

### `ProjectAuthorMetadata`

Given the current static publication identity, project browser author metadata
such that:

- each generated HTML page exposes one deterministic author value
- the value remains shared across routes in this bootstrap slice
- metadata stays aligned with the existing publication identity

### `RenderAuthorHead`

Given a generated HTML document and the shared head renderer, render author
metadata such that:

- each generated HTML page includes the bounded `meta name="author"` tag
- existing viewport, application-name, color-scheme, referrer, theme-color,
  mobile-web-app, manifest, and social metadata remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- Author metadata must be explicit and deterministic across the generated
  static publication.
- The slice stays bounded to shared HTML head metadata rather than new content
  structures or visible byline changes.
- The selected value should derive from an existing shared publication identity
  decision rather than ad hoc route content.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer
- existing shared publication identity in `SiteConfig` or adjacent build-time
  configuration
- deterministic head metadata test coverage for representative route families

## Initial Test Plan

- unit test asserting generated HTML pages include the bounded
  `meta name="author"` tag
- unit test asserting representative route families render the same author
  value
- integration test asserting homepage and representative content routes expose
  the author metadata in `<head>`
- integration test asserting existing viewport, application-name,
  color-scheme, referrer, theme-color, mobile-web-app, Open Graph, Twitter
  Card, and visible chrome behavior remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include the bounded author
  metadata in `<head>`
- the value remains stable across generated routes
- the rest of the publication surface remains unchanged

## Done Criteria

- generated HTML routes include deterministic `author` metadata
- the selected value is enforced consistently across representative route
  families
- the slice introduces no new routes, assets, or runtime dependencies
- deterministic tests cover the shared head metadata and unchanged visible
  chrome
