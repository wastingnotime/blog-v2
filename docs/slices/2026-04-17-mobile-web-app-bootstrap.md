# Slice: 2026-04-17 Mobile Web App Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic mobile-web-app metadata in the shared document head:

- add one bounded mobile-web-app metadata contract to generated HTML pages
- align that contract with the existing site title, theme-color, and identity
  surface
- keep the slice limited to metadata only, without changing runtime behavior or
  styling

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, manifest links, Open Graph metadata, Twitter Card metadata,
shared social preview image support, and aligned theme-color metadata. The next
browser-facing identity gap is platform-specific mobile metadata: generated HTML
pages still omit Apple mobile-web-app tags even though the publication already
ships the necessary shared identity inputs.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders the shared document head
  without any `apple-mobile-web-app-*` metadata
- the publication already ships `apple-touch-icon.png`, a stable site title,
  and bounded shared color metadata
- the current manifest and head contract are now strong enough that one bounded
  mobile-web-app metadata slice can reuse existing deterministic inputs

This slice restores the minimum mobile-web-app surface needed for the current
publication:

- add bounded `apple-mobile-web-app-capable`,
  `apple-mobile-web-app-title`, and
  `apple-mobile-web-app-status-bar-style` metadata to generated HTML pages
- derive values deterministically from the existing site title and shared color
  identity
- keep rendering consistent across homepage, sections, pages, and narrative
  routes

This slice does not attempt splash screens, status-bar platform branching,
install prompts, or broader PWA behavior.

## Use-Case Contract

### `ProjectMobileWebAppMetadata`

Given site settings and the current shared identity surface, project
mobile-web-app metadata such that:

- each generated HTML page exposes one deterministic mobile-web-app contract
- title remains aligned with the configured publication identity
- status-bar behavior stays bounded to one deterministic literal

### `RenderMobileWebAppHead`

Given a generated HTML document and the shared head renderer, render mobile
metadata such that:

- each generated HTML page includes the bounded Apple mobile-web-app tags
- existing theme-color, manifest, and social metadata remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- Mobile-web-app metadata must be derived from the existing deterministic
  publication identity, not ad hoc per-route choices.
- The slice stays bounded to shared HTML head metadata rather than page styling
  or manifest redesign.
- The mobile-web-app title should remain aligned with the configured site
  title.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer
- existing site settings in `SiteConfig`
- existing static identity assets already published by the build

## Initial Test Plan

- unit test asserting generated HTML pages include the bounded
  `apple-mobile-web-app-*` tags
- unit test asserting representative route families render the same mobile-web-
  app metadata values
- integration test asserting homepage and representative content routes expose
  the mobile-web-app tags in `<head>`
- integration test asserting existing theme-color, Open Graph, Twitter Card,
  and visible chrome behavior remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include the bounded mobile-web-app
  metadata in `<head>`
- the title and status-bar values remain stable across generated routes
- the rest of the publication surface remains unchanged

## Done Criteria

- generated HTML routes include deterministic Apple mobile-web-app metadata
- metadata values derive from the existing shared identity surface
- representative routes render the same bounded mobile-web-app contract
- deterministic tests cover the shared head metadata and unchanged visible
  chrome
