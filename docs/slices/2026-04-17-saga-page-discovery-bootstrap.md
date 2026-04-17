# Slice: 2026-04-17 Saga Page Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic saga-page discovery update for the expanded publication surface:

- revise saga detail pages so they expose the current complementary discovery
  routes
- add bounded affordances for Search and Archives alongside the existing arc
  and timeline sections
- keep the slice limited to saga-page discovery copy and links

## Discovery Scope

The publication now exposes stable reader-facing discovery routes for saga
detail pages, archives, and search. Saga detail pages still reflect an earlier
site shape and behave as isolated narrative surfaces aside from their arc and
timeline structure.

That gap is visible in current repository artifacts:

- `build_saga_page(...)` renders saga body content, arc summaries, and a
  timeline, but no complementary discovery affordance for `/archives/` or
  `/search/`
- saga detail pages such as `/sagas/hireflow/` are meaningful reader-facing
  routes, not just supporting internals
- archives and search are now first-class routes with shared-navigation
  discoverability, but saga detail pages do not acknowledge them explicitly

This slice restores the minimum saga-page discovery surface needed for the
current publication:

- update saga detail pages so they link readers to `/archives/` and `/search/`
- preserve the existing body, arc, and timeline rendering
- keep the change bounded to saga-page discovery copy and links

This slice does not attempt broader saga-page redesign, new narrative
projections, related-content algorithms, or search behavior changes.

## Use-Case Contract

### `BuildSagaPage`

Given a projected saga view and the current reader-facing routes, generate
deterministic static output for `/sagas/<slug>/` such that:

- the page continues to render saga body, arcs, and timeline content
- readers can reach search and archives directly from the saga page
- output remains fully static and compatible with GitHub Pages hosting

### `RenderSagaDiscovery`

Given a saga route and current publication surfaces, render bounded discovery
content such that:

- the page still centers saga narrative structure as its primary job
- archives and search are visibly represented as complementary discovery paths
- the section remains publication-oriented rather than turning into generic
  navigation chrome

## Main Business Rules

- Saga-page discovery copy must stay aligned with the routes the publication
  now exposes.
- Saga discovery affordances should point to stable reader-facing routes, not
  implementation artifacts.
- The slice stays bounded to saga-page copy and linking rather than changing
  saga projection or shared navigation.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing saga-page renderer
- environment reader for site settings
- existing stable routes for `/search/`, `/archives/`, and `/sagas/<slug>/`

## Initial Test Plan

- unit test asserting a saga page links directly to `/archives/` and
  `/search/`
- unit test asserting the existing arc and timeline sections remain present
- integration test asserting generated `dist/sagas/<slug>/index.html` exposes
  the new saga discovery affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect a generated
saga page such as `dist/sagas/hireflow/index.html` to verify:

- the page still reads like a saga landing page
- the page links directly to search and archive discovery surfaces
- the existing body, arc summaries, and timeline remain unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- saga detail pages align with the current publication discovery surface
- `/sagas/<slug>/` pages expose deterministic links to `/search/` and
  `/archives/`
- deterministic tests cover the new saga-page affordances and unchanged
  static-only behavior
