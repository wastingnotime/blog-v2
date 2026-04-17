# Slice: 2026-04-17 Application Name Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic application-name metadata in the shared document head:

- add one bounded application-name contract to generated HTML pages
- align that metadata with the existing site title and manifest identity
- keep the slice limited to metadata only, without changing install behavior

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, manifest links, Open Graph metadata, Twitter Card metadata,
shared social preview image support, theme-color, Apple mobile-web-app
metadata, format-detection metadata, referrer metadata, and explicit
color-scheme metadata. The next small browser-facing head gap is application
identity signaling: generated HTML pages still omit `meta name="application-name"`
even though the publication already has a stable site title and manifest name.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders the shared document
  head without `meta name="application-name"`
- `site.webmanifest` already exposes `name` and `short_name`, and the shared
  head already exposes `apple-mobile-web-app-title`, so this is now a missing
  cross-browser identity metadata surface rather than a naming gap
- the GitHub Pages deployment target keeps the site static, so the next slice
  should stay bounded to one deterministic metadata literal derived from
  existing site settings

This slice restores the minimum explicit application-name surface needed for
the current publication:

- add one shared `meta name="application-name"` tag to generated HTML pages
- derive the value deterministically from the configured site title
- keep the value stable across homepage, sections, pages, and narrative routes

This slice does not attempt install prompts, manifest redesign, browser-specific
tile metadata, or broader PWA behavior.

## Use-Case Contract

### `ProjectApplicationNameMetadata`

Given site settings and the current static publication identity, project
browser application-name metadata such that:

- each generated HTML page exposes one deterministic application-name value
- the value remains aligned with the configured site title
- metadata stays stable across generated routes

### `RenderApplicationNameHead`

Given a generated HTML document and the shared head renderer, render
application-name metadata such that:

- each generated HTML page includes the bounded
  `meta name="application-name"` tag
- existing theme-color, mobile-web-app, referrer, color-scheme, manifest, and
  social metadata remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- Application-name metadata must be explicit and deterministic across the
  generated static publication.
- The slice stays bounded to shared HTML head metadata rather than install
  flows or browser-specific platform contracts.
- The selected value should derive from the configured site title rather than
  ad hoc per-route content.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer
- existing site settings in `SiteConfig`
- deterministic head metadata test coverage for representative route families

## Initial Test Plan

- unit test asserting generated HTML pages include the bounded
  `meta name="application-name"` tag
- unit test asserting representative route families render the same
  application-name value
- integration test asserting homepage and representative content routes expose
  the application-name metadata in `<head>`
- integration test asserting existing theme-color, mobile-web-app, referrer,
  color-scheme, Open Graph, Twitter Card, and visible chrome behavior remain
  unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include the bounded
  application-name metadata in `<head>`
- the value remains aligned with the configured site title across generated
  routes
- the rest of the publication surface remains unchanged

## Done Criteria

- generated HTML routes include deterministic application-name metadata
- the selected value is enforced consistently across representative route
  families
- the slice introduces no new routes, assets, or runtime dependencies
- deterministic tests cover the shared head metadata and unchanged visible
  chrome
