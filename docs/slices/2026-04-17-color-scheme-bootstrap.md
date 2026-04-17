# Slice: 2026-04-17 Color Scheme Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic color-scheme metadata in the shared document head:

- add one bounded color-scheme contract to generated HTML pages
- align the head metadata with the publication's existing light-only palette
- keep the slice limited to metadata only, without redesigning styling

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, manifest links, Open Graph metadata, Twitter Card metadata,
shared social preview image support, theme-color, Apple mobile-web-app
metadata, format-detection metadata, and explicit referrer metadata. The next
small browser-facing head gap is color-scheme signaling: generated HTML pages
still omit an explicit `meta name="color-scheme"` tag even though the shared
CSS already commits the publication to a light-only palette.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders `:root { color-scheme:
  light; }` in the shared CSS but no `meta name="color-scheme"` in `<head>`
- the publication already has aligned theme-color and manifest color metadata,
  so this is now a head-contract gap rather than a visual-design gap
- the GitHub Pages deployment target keeps the site static, so the next slice
  should stay bounded to one deterministic browser-facing metadata literal

This slice restores the minimum explicit color-scheme surface needed for the
current publication:

- add one shared `meta name="color-scheme"` tag to generated HTML pages
- keep the chosen literal deterministic across homepage, sections, pages, and
  narrative routes
- align the metadata with the existing light-only publication styling

This slice does not attempt dark mode, alternate palettes, route-specific color
behavior, or broader CSS redesign.

## Use-Case Contract

### `ProjectColorSchemeMetadata`

Given the current static publication styling and shared palette, project
browser color-scheme metadata such that:

- each generated HTML page exposes one deterministic color-scheme value
- the chosen value remains bounded to one literal for this bootstrap slice
- metadata stays aligned with the existing publication styling contract

### `RenderColorSchemeHead`

Given a generated HTML document and the shared head renderer, render
color-scheme metadata such that:

- each generated HTML page includes the bounded `meta name="color-scheme"` tag
- existing theme-color, mobile-web-app, referrer, manifest, and social
  metadata remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- Color-scheme metadata must be explicit and deterministic across the generated
  static publication.
- The slice stays bounded to shared HTML head metadata rather than CSS redesign
  or runtime theme switching.
- The selected color-scheme value should remain one deterministic literal in
  this bootstrap slice.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer
- existing shared CSS identity surface in `build_site.py`
- deterministic head metadata test coverage for representative route families

## Initial Test Plan

- unit test asserting generated HTML pages include the bounded
  `meta name="color-scheme"` tag
- unit test asserting representative route families render the same
  color-scheme value
- integration test asserting homepage and representative content routes expose
  the color-scheme metadata in `<head>`
- integration test asserting existing theme-color, mobile-web-app, referrer,
  Open Graph, Twitter Card, and visible chrome behavior remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include the bounded color-scheme
  metadata in `<head>`
- the chosen color-scheme value remains stable across generated routes
- the rest of the publication surface remains unchanged

## Done Criteria

- generated HTML routes include deterministic color-scheme metadata
- the selected color-scheme value is enforced consistently across
  representative route families
- the slice introduces no new routes, assets, or runtime dependencies
- deterministic tests cover the shared head metadata and unchanged visible
  chrome
