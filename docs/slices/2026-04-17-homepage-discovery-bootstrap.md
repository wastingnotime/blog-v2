# Slice: 2026-04-17 Homepage Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic homepage discovery update for the expanded publication surface:

- revise the homepage editorial body so it points readers toward the current
  reading paths
- add bounded affordances for Search and Archives alongside the existing saga
  and library guidance
- keep the slice limited to homepage discovery copy, links, and a stable shell
  hook

## Discovery Scope

The publication now exposes four stable reader-facing paths beyond individual
entries: `/sagas/`, `/library/`, `/archives/`, and `/search/`. The homepage
body still reflects an earlier site shape and only directs readers toward the
saga index and library.

That gap is visible in current repository artifacts:

- `build_homepage(...)` still says readers should follow the longer arcs
  through the saga index and library
- the homepage sections include direct calls to action for sagas and library,
  but no parallel affordance for archives or search
- archives and search are now first-class routes with shared-navigation
  discoverability, so the homepage editorial surface is behind the actual site
  shape

This slice restores the minimum homepage discovery surface needed for the
current publication:

- update homepage copy so it names chronology and search as supported reading
  paths
- add direct homepage affordances for `/archives/` and `/search/`
- preserve the existing recent-content and active-saga structure
- expose the discovery block through a stable page-shell class

This slice does not attempt a broader homepage redesign, new projections,
visual-system overhaul, or richer search/archive behavior.

## Use-Case Contract

### `BuildEditorialHomepage`

Given site settings and the current homepage surface, generate deterministic
static output for `/` such that:

- the editorial introduction reflects the routes the publication actually
  offers today
- readers can reach search and archives directly from the homepage body
- output remains fully static and compatible with GitHub Pages hosting

### `RenderHomepageDiscovery`

Given the homepage route and current reader-facing publication surfaces, render
bounded discovery content such that:

- the homepage continues to frame the site as a publication rather than a
  status page
- chronology, topic browsing, narrative browsing, and search are all visibly
  represented
- existing recent-entry and saga-summary sections remain intact
- the discovery block uses a stable shell hook

## Main Business Rules

- Homepage editorial copy must stay aligned with the routes the publication now
  exposes.
- Homepage discovery affordances should point to stable reader-facing routes,
  not implementation artifacts.
- The slice stays bounded to homepage copy and linking rather than changing
  homepage projections or navigation chrome.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing homepage renderer
- environment reader for site settings
- existing stable routes for `/search/`, `/archives/`, `/sagas/`, and
  `/library/`

## Initial Test Plan

- unit test asserting homepage copy mentions chronology and search discovery
- unit test asserting homepage HTML links directly to `/archives/` and
  `/search/`
- integration test asserting generated `dist/index.html` exposes the new
  homepage affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect `dist/index.html`
to verify:

- the homepage still reads like a publication landing page
- the page links directly to search and archive discovery surfaces
- existing recent-content and saga-summary sections remain unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- homepage editorial copy aligns with the current publication surface
- `/` exposes deterministic discovery links to `/search/` and `/archives/`
- deterministic tests cover the new homepage affordances and unchanged
  static-only behavior
