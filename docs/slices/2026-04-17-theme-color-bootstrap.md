# Slice: 2026-04-17 Theme Color Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic browser-facing color metadata in the shared head and manifest:

- add one bounded theme-color contract to generated HTML pages
- align the manifest with the same static color identity fields
- keep the slice limited to metadata only, without redesigning visual styling

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, manifest links, Open Graph metadata, Twitter Card metadata,
and a shared social preview image. The next browser-facing identity gap is
color metadata: generated HTML pages still lack a `theme-color` meta tag, and
`site.webmanifest` still omits `theme_color` and `background_color`.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders the shared document head
  without any `theme-color` metadata
- the generated `site.webmanifest` contains name, start URL, display, and icon
  fields but no color identity fields
- the shared CSS already defines a stable visual palette, so the publication has
  enough deterministic information to expose bounded browser color metadata

This slice restores the minimum browser-facing color surface needed for the
current publication:

- add one shared `theme-color` meta tag to generated HTML pages
- add deterministic `theme_color` and `background_color` fields to
  `site.webmanifest`
- keep the chosen colors aligned with the existing static identity surface

This slice does not attempt dark mode, per-route theming, status-bar platform
special cases, or broader visual redesign.

## Use-Case Contract

### `ProjectThemeColorMetadata`

Given site settings and the current shared visual palette, project browser color
metadata such that:

- the HTML head exposes one deterministic `theme-color`
- manifest color fields use the same bounded identity contract
- colors remain stable across generated routes

### `RenderThemeColorHeadAndManifest`

Given a generated HTML document and the manifest renderer, render color metadata
such that:

- each generated HTML page includes the bounded `theme-color` tag
- `site.webmanifest` includes matching color fields
- existing visible chrome and metadata behavior remain unchanged

## Main Business Rules

- Browser-facing color metadata must be derived from the existing deterministic
  publication identity, not ad hoc per-route choices.
- The slice stays bounded to shared HTML and manifest metadata rather than page
  styling changes.
- HTML and manifest color fields should remain aligned with each other.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer
- manifest renderer in `build_site.py`
- existing static visual palette already defined in the shared CSS

## Initial Test Plan

- unit test asserting generated HTML pages include the bounded `theme-color`
  meta tag
- unit test asserting `site.webmanifest` includes `theme_color` and
  `background_color`
- integration test asserting homepage and representative content routes render
  the same `theme-color` value
- integration test asserting the manifest color fields stay aligned with the
  shared head metadata
- integration test asserting existing Open Graph, Twitter Card, and visible
  chrome behavior remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include `theme-color` in `<head>`
- `site.webmanifest` includes matching color identity fields
- the chosen colors remain stable across the static publication surface
- the rest of the publication surface remains unchanged

## Done Criteria

- generated HTML routes include deterministic `theme-color` metadata
- `site.webmanifest` includes aligned `theme_color` and `background_color`
  fields
- color values derive from the existing static identity surface
- deterministic tests cover both shared head metadata and manifest fields
