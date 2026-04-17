# Slice: 2026-04-17 Library Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic library-hub discovery update for the expanded publication surface:

- revise the library page so it acknowledges the current complementary reading
  paths
- add bounded affordances for Search and Archives alongside the existing topic
  navigation role
- keep the slice limited to library-hub discovery copy and links

## Discovery Scope

The publication now exposes stable reader-facing discovery routes for topics,
archives, and search. The library hub still reflects an earlier site shape and
frames itself only as topic navigation.

That gap is visible in current repository artifacts:

- `content/sections/library.md` explains moving by idea instead of chronology,
  but does not point readers toward the now-existing chronology or search
  surfaces
- `build_library_page(...)` renders authored intro copy plus topic links, but
  no complementary discovery affordance for `/archives/` or `/search/`
- archives and search are now first-class routes with shared-navigation
  discoverability, so the library hub understates the actual ways readers can
  move through the publication

This slice restores the minimum library discovery surface needed for the
current publication:

- update the library hub so it links readers to `/archives/` and `/search/`
- preserve the existing authored intro copy and topic-list role
- keep the change bounded to library discovery copy and links

This slice does not attempt broader library redesign, taxonomy changes, new
search behavior, or archive faceting.

## Use-Case Contract

### `BuildLibrarySectionPage`

Given authored library content and the current reader-facing routes, generate
deterministic static output for `/library/` such that:

- the page continues to explain topic-based browsing in a stable, static form
- readers can reach search and archives directly from the library hub
- output remains fully static and compatible with GitHub Pages hosting

### `RenderLibraryDiscovery`

Given the library route and current publication surfaces, render bounded
discovery content such that:

- the page still centers topic browsing as its primary job
- archives and search are also visibly represented as complementary discovery
  paths
- the section remains publication-oriented rather than turning into generic
  navigation chrome

## Main Business Rules

- Library-hub discovery copy must stay aligned with the routes the publication
  now exposes.
- Library discovery affordances should point to stable reader-facing routes,
  not implementation artifacts.
- The slice stays bounded to library-hub copy and linking rather than changing
  topic projection or shared navigation.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing library-page renderer
- environment reader for site settings
- existing stable routes for `/search/`, `/archives/`, and `/library/`

## Initial Test Plan

- unit test asserting the library page links directly to `/archives/` and
  `/search/`
- unit test asserting the existing topic list remains present
- integration test asserting generated `dist/library/index.html` exposes the
  new library discovery affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/library/index.html` to verify:

- the library page still reads like a topic hub
- the page links directly to search and archive discovery surfaces
- the existing topic list remains unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- the library hub aligns with the current publication discovery surface
- `/library/` exposes deterministic links to `/search/` and `/archives/`
- deterministic tests cover the new library affordances and unchanged
  static-only behavior
