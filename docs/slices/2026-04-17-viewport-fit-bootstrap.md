# Slice: 2026-04-17 Viewport Fit Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic viewport-fit metadata in the shared document head:

- extend the bounded viewport contract for generated HTML pages
- align the head metadata with the existing mobile-web-app publication surface
- keep the slice limited to metadata only, without changing layout or styling

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, manifest links, Open Graph metadata, Twitter Card metadata,
shared social preview image support, theme-color, Apple mobile-web-app
metadata, format-detection metadata, referrer metadata, color-scheme
metadata, and application-name metadata. The next small browser-facing head
gap is viewport-fit signaling: generated HTML pages still use the minimal
`width=device-width, initial-scale=1` viewport contract and do not explicitly
declare `viewport-fit=cover`.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders a shared viewport tag
  without `viewport-fit=cover`
- the publication already exposes a bounded Apple mobile-web-app contract and
  theme metadata, so this is now a small mobile-display metadata gap rather
  than a broader responsive-layout problem
- the GitHub Pages deployment target keeps the site static, so the next slice
  should stay bounded to one deterministic viewport literal instead of runtime
  device handling

This slice restores the minimum explicit viewport-fit surface needed for the
current publication:

- update the shared viewport tag to include `viewport-fit=cover`
- keep the viewport literal deterministic across homepage, sections, pages, and
  narrative routes
- preserve the current visual layout and route structure

This slice does not attempt safe-area CSS, route-specific mobile layouts,
dark-mode behavior, or broader responsive redesign.

## Use-Case Contract

### `ProjectViewportMetadata`

Given the current static publication and shared mobile metadata surface,
project viewport metadata such that:

- each generated HTML page exposes one deterministic viewport literal
- the viewport contract includes `viewport-fit=cover` in this bootstrap slice
- metadata remains stable across generated routes

### `RenderViewportHead`

Given a generated HTML document and the shared head renderer, render viewport
metadata such that:

- each generated HTML page includes the bounded viewport literal with
  `viewport-fit=cover`
- existing application-name, color-scheme, referrer, theme-color,
  mobile-web-app, manifest, and social metadata remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- Viewport metadata must be explicit and deterministic across the generated
  static publication.
- The slice stays bounded to shared HTML head metadata rather than layout or
  CSS redesign.
- The selected viewport literal should remain one deterministic shared value in
  this bootstrap slice.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer
- deterministic head metadata test coverage for representative route families
- existing mobile-web-app and theme metadata already published by the build

## Initial Test Plan

- unit test asserting generated HTML pages include the bounded viewport literal
  with `viewport-fit=cover`
- unit test asserting representative route families render the same viewport
  value
- integration test asserting homepage and representative content routes expose
  the updated viewport metadata in `<head>`
- integration test asserting existing application-name, color-scheme,
  referrer, theme-color, mobile-web-app, Open Graph, Twitter Card, and visible
  chrome behavior remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include the bounded viewport
  metadata with `viewport-fit=cover` in `<head>`
- the chosen viewport value remains stable across generated routes
- the rest of the publication surface remains unchanged

## Done Criteria

- generated HTML routes include deterministic viewport metadata with
  `viewport-fit=cover`
- the selected viewport value is enforced consistently across representative
  route families
- the slice introduces no new routes, assets, or runtime dependencies
- deterministic tests cover the shared head metadata and unchanged visible
  chrome
