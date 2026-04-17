# Slice: 2026-04-17 MSApplication Tile Color Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic Windows tile color metadata in the shared document head:

- add one bounded `msapplication-TileColor` contract to generated HTML pages
- align that metadata with the existing shared theme-color identity
- keep the slice limited to metadata only, without adding new assets

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, manifest links, Open Graph metadata, Twitter Card metadata,
shared social preview image support, theme-color, Apple mobile-web-app
metadata, format-detection metadata, referrer metadata, color-scheme
metadata, application-name metadata, and an explicit viewport-fit contract.
The next small browser-facing head gap is Windows tile identity signaling:
generated HTML pages still omit `meta name="msapplication-TileColor"` even
though the publication already has a stable shared theme color.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders a shared
  `theme-color` tag but no `msapplication-TileColor`
- the publication already has a deterministic cross-browser color identity, so
  this is now a small platform-facing metadata gap rather than a design gap
- the GitHub Pages deployment target keeps the site static, so the next slice
  should stay bounded to one deterministic metadata literal derived from the
  existing publication palette

This slice restores the minimum explicit Windows tile color surface needed for
the current publication:

- add one shared `meta name="msapplication-TileColor"` tag to generated HTML
  pages
- derive the value deterministically from the existing shared theme color
- keep the value stable across homepage, sections, pages, and narrative routes

This slice does not attempt browserconfig XML, pinned-site assets, route-
specific theming, or broader platform-specific install behavior.

## Use-Case Contract

### `ProjectMSApplicationTileColorMetadata`

Given the current static publication identity and shared theme-color choice,
project Windows tile color metadata such that:

- each generated HTML page exposes one deterministic tile color value
- the value remains aligned with the existing theme-color contract
- metadata stays stable across generated routes

### `RenderMSApplicationTileColorHead`

Given a generated HTML document and the shared head renderer, render tile color
metadata such that:

- each generated HTML page includes the bounded
  `meta name="msapplication-TileColor"` tag
- existing viewport, application-name, color-scheme, referrer, theme-color,
  mobile-web-app, manifest, and social metadata remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- Tile color metadata must be explicit and deterministic across the generated
  static publication.
- The slice stays bounded to shared HTML head metadata rather than new assets
  or browser-specific configuration files.
- The selected tile color value should derive from the existing shared
  theme-color identity.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer
- existing shared theme-color identity in `build_site.py`
- deterministic head metadata test coverage for representative route families

## Initial Test Plan

- unit test asserting generated HTML pages include the bounded
  `meta name="msapplication-TileColor"` tag
- unit test asserting representative route families render the same tile color
  value
- integration test asserting homepage and representative content routes expose
  the tile color metadata in `<head>`
- integration test asserting existing viewport, application-name, color-scheme,
  referrer, theme-color, mobile-web-app, Open Graph, Twitter Card, and visible
  chrome behavior remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include the bounded tile color
  metadata in `<head>`
- the value remains aligned with the existing shared theme color across
  generated routes
- the rest of the publication surface remains unchanged

## Done Criteria

- generated HTML routes include deterministic `msapplication-TileColor`
  metadata
- the selected value is enforced consistently across representative route
  families
- the slice introduces no new routes, assets, or runtime dependencies
- deterministic tests cover the shared head metadata and unchanged visible
  chrome
