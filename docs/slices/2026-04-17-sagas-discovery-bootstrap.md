# Slice: 2026-04-17 Sagas Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic sagas-hub discovery update for the expanded publication surface:

- revise the sagas index so it points readers toward the current complementary
  discovery routes
- add bounded affordances for Search and Archives alongside the existing saga
  listing and start-reading paths
- keep the slice limited to sagas-hub discovery copy and links

## Discovery Scope

The publication now exposes stable reader-facing discovery routes for sagas,
archives, and search. The sagas hub still reflects an earlier site shape and
functions only as a listing surface for active sagas.

That gap is visible in current repository artifacts:

- `build_sagas_index_page(...)` renders only the active-saga list
- `/sagas/` is a section hub and should help readers navigate the broader
  publication surface rather than acting as an isolated list
- archives and search are now first-class routes with shared-navigation
  discoverability, but the sagas hub does not acknowledge them

This slice restores the minimum sagas discovery surface needed for the current
publication:

- update the sagas hub so it links readers to `/archives/` and `/search/`
- preserve the existing active-saga list and start-reading affordances
- keep the change bounded to sagas-hub discovery copy and links

This slice does not attempt broader sagas redesign, new saga projections,
search behavior changes, or archive faceting.

## Use-Case Contract

### `BuildSagasIndex`

Given the loaded content catalog and saga projections, generate deterministic
static output for `/sagas/` such that:

- the page continues to list active sagas and start-reading links
- readers can reach search and archives directly from the sagas hub
- output remains fully static and compatible with GitHub Pages hosting

### `RenderSagasDiscovery`

Given the sagas route and current publication surfaces, render bounded
discovery content such that:

- the page still centers active saga navigation as its primary job
- archives and search are also visibly represented as complementary discovery
  paths
- the section remains publication-oriented rather than turning into generic
  navigation chrome

## Main Business Rules

- Sagas-hub discovery copy must stay aligned with the routes the publication
  now exposes.
- Sagas discovery affordances should point to stable reader-facing routes, not
  implementation artifacts.
- The slice stays bounded to sagas-hub copy and linking rather than changing
  saga projection or shared navigation.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing sagas-page renderer
- environment reader for site settings
- existing stable routes for `/search/`, `/archives/`, and `/sagas/`

## Initial Test Plan

- unit test asserting the sagas page links directly to `/archives/` and
  `/search/`
- unit test asserting the existing active-saga list and start-reading links
  remain present
- integration test asserting generated `dist/sagas/index.html` exposes the new
  sagas discovery affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/sagas/index.html` to verify:

- the sagas page still reads like a saga hub
- the page links directly to search and archive discovery surfaces
- the existing active-saga list remains unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- the sagas hub aligns with the current publication discovery surface
- `/sagas/` exposes deterministic links to `/search/` and `/archives/`
- deterministic tests cover the new sagas affordances and unchanged
  static-only behavior
