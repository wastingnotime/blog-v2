# Slice: 2026-04-17 Studio Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic studio-hub discovery update for the expanded publication surface:

- revise the studio page's navigation section so it points readers toward the
  current discovery routes
- add bounded affordances for Search and Archives alongside the existing sagas
  and library links
- keep the slice limited to studio-hub copy and links

## Discovery Scope

The publication now exposes stable reader-facing discovery routes for sagas,
library, archives, and search. The studio hub still reflects an earlier site
shape and only directs readers toward `/sagas/` and `/library/`.

That gap is visible in current repository artifacts:

- `build_studio_page(...)` still renders a `Navigate` section with links only
  to sagas and library
- the studio page is intended to explain the broader spaces of the site, so its
  discovery guidance should keep pace with the current route set
- archives and search are now first-class routes with shared-navigation
  discoverability, but the studio hub does not acknowledge them

This slice restores the minimum studio discovery surface needed for the current
publication:

- update the studio page's navigation section so it includes search and archive
  affordances
- preserve the existing authored intro copy and section-hub role
- keep the change bounded to studio discovery copy and links

This slice does not attempt broader studio redesign, new section projections,
or richer search/archive behavior.

## Use-Case Contract

### `BuildStudioSectionPage`

Given authored studio content and the current reader-facing routes, generate
deterministic static output for `/studio/` such that:

- the page continues to explain the site's spaces in a stable, static form
- readers can reach search and archives directly from the studio hub
- output remains fully static and compatible with GitHub Pages hosting

### `RenderStudioDiscovery`

Given the studio route and current publication surfaces, render bounded
discovery content such that:

- the page still links to sagas and library
- archives and search are also visibly represented as discovery paths
- the section remains publication-oriented rather than turning into generic
  navigation chrome

## Main Business Rules

- Studio-hub discovery copy must stay aligned with the routes the publication
  now exposes.
- Studio discovery affordances should point to stable reader-facing routes, not
  implementation artifacts.
- The slice stays bounded to studio-hub copy and linking rather than changing
  shared navigation or section-body authorship.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing studio-page renderer
- environment reader for site settings
- existing stable routes for `/search/`, `/archives/`, `/sagas/`, and
  `/library/`

## Initial Test Plan

- unit test asserting the studio page links directly to `/archives/` and
  `/search/`
- unit test asserting existing links to `/sagas/` and `/library/` remain
  present
- integration test asserting generated `dist/studio/index.html` exposes the new
  studio discovery affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/studio/index.html` to verify:

- the studio page still reads like a section hub
- the page links directly to search and archive discovery surfaces
- existing saga and library links remain unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- the studio hub aligns with the current publication discovery surface
- `/studio/` exposes deterministic links to `/search/` and `/archives/`
- deterministic tests cover the new studio affordances and unchanged
  static-only behavior
