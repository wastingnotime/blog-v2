# Slice: 2026-04-17 Arc Page Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic arc-page discovery update for the expanded publication surface:

- revise arc detail pages so they expose the current complementary discovery
  routes
- add bounded affordances for Search and Archives alongside the existing body
  and episode-list sections
- keep the slice limited to arc-page discovery copy and links

## Discovery Scope

The publication now exposes stable reader-facing discovery routes for arc
detail pages, archives, and search. Arc detail pages still reflect an earlier
site shape and behave as isolated narrative surfaces aside from their episode
list and breadcrumb.

That gap is visible in current repository artifacts:

- `build_arc_page(...)` renders breadcrumb navigation, arc body content, and an
  episode list, but no complementary discovery affordance for `/archives/` or
  `/search/`
- arc detail pages such as `/sagas/hireflow/the-origin-blueprint/` are
  meaningful reader-facing routes, not just internal drill-down views
- archives and search are now first-class routes with shared-navigation
  discoverability, but arc detail pages do not acknowledge them explicitly

This slice restores the minimum arc-page discovery surface needed for the
current publication:

- update arc detail pages so they link readers to `/archives/` and `/search/`
- preserve the existing breadcrumb, body, and episode-list rendering
- keep the change bounded to arc-page discovery copy and links

This slice does not attempt broader arc-page redesign, new narrative
projections, related-content algorithms, or search behavior changes.

## Use-Case Contract

### `BuildArcPage`

Given a projected arc view and the current reader-facing routes, generate
deterministic static output for `/sagas/<saga>/<arc>/` such that:

- the page continues to render breadcrumb navigation, arc body, and episode
  list content
- readers can reach search and archives directly from the arc page
- output remains fully static and compatible with GitHub Pages hosting

### `RenderArcDiscovery`

Given an arc route and current publication surfaces, render bounded discovery
content such that:

- the page still centers arc narrative structure as its primary job
- archives and search are visibly represented as complementary discovery paths
- the section remains publication-oriented rather than turning into generic
  navigation chrome

## Main Business Rules

- Arc-page discovery copy must stay aligned with the routes the publication now
  exposes.
- Arc discovery affordances should point to stable reader-facing routes, not
  implementation artifacts.
- The slice stays bounded to arc-page copy and linking rather than changing arc
  projection or shared navigation.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing arc-page renderer
- environment reader for site settings
- existing stable routes for `/search/`, `/archives/`, and
  `/sagas/<saga>/<arc>/`

## Initial Test Plan

- unit test asserting an arc page links directly to `/archives/` and `/search/`
- unit test asserting the existing breadcrumb and episode-list sections remain
  present
- integration test asserting generated `dist/sagas/<saga>/<arc>/index.html`
  exposes the new arc discovery affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect a generated
arc page such as `dist/sagas/hireflow/the-origin-blueprint/index.html` to
verify:

- the page still reads like an arc landing page
- the page links directly to search and archive discovery surfaces
- the existing breadcrumb, body, and episode list remain unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- arc detail pages align with the current publication discovery surface
- `/sagas/<saga>/<arc>/` pages expose deterministic links to `/search/` and
  `/archives/`
- deterministic tests cover the new arc-page affordances and unchanged
  static-only behavior
