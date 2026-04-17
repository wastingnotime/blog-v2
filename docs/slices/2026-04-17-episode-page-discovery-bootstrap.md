# Slice: 2026-04-17 Episode Page Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic episode-page discovery update for the expanded publication
surface:

- revise episode detail pages so they expose the current complementary
  discovery routes
- add bounded affordances for Search and Archives alongside the existing
  breadcrumb, entry metadata, body, and adjacent navigation
- keep the slice limited to episode-page discovery copy and links

## Discovery Scope

The publication now exposes stable reader-facing discovery routes for episode
detail pages, archives, and search. Episode pages still reflect an earlier site
shape and behave as isolated narrative leaves aside from their breadcrumb,
entry metadata, and prev/next navigation.

That gap is visible in current repository artifacts:

- `build_episode_page(...)` renders breadcrumb navigation, entry metadata,
  episode body, and adjacent navigation, but no complementary discovery
  affordance for `/archives/` or `/search/`
- episode detail pages such as
  `/sagas/hireflow/the-origin-blueprint/the-first-brick/` are meaningful
  reader-facing routes, not just internal drill-down views
- archives and search are now first-class routes with shared-navigation
  discoverability, but episode pages do not acknowledge them explicitly

This slice restores the minimum episode-page discovery surface needed for the
current publication:

- update episode detail pages so they link readers to `/archives/` and
  `/search/`
- preserve the existing breadcrumb, entry metadata, body, and adjacent
  navigation rendering
- keep the change bounded to episode-page discovery copy and links

This slice does not attempt broader episode-page redesign, related-content
algorithms, richer next-step recommendations, or search behavior changes.

## Use-Case Contract

### `BuildEpisodePage`

Given a projected episode view and the current reader-facing routes, generate
deterministic static output for `/sagas/<saga>/<arc>/<episode>/` such that:

- the page continues to render breadcrumb navigation, entry metadata, episode
  body, and adjacent episode navigation
- readers can reach search and archives directly from the episode page
- output remains fully static and compatible with GitHub Pages hosting

### `RenderEpisodeDiscovery`

Given an episode route and current publication surfaces, render bounded
discovery content such that:

- the page still centers the episode itself as its primary job
- archives and search are visibly represented as complementary discovery paths
- the section remains publication-oriented rather than turning into generic
  navigation chrome

## Main Business Rules

- Episode-page discovery copy must stay aligned with the routes the publication
  now exposes.
- Episode discovery affordances should point to stable reader-facing routes,
  not implementation artifacts.
- The slice stays bounded to episode-page copy and linking rather than changing
  episode projection or shared navigation.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing episode-page renderer
- environment reader for site settings
- existing stable routes for `/search/`, `/archives/`, and
  `/sagas/<saga>/<arc>/<episode>/`

## Initial Test Plan

- unit test asserting an episode page links directly to `/archives/` and
  `/search/`
- unit test asserting the existing breadcrumb, entry metadata, and adjacent
  navigation remain present
- integration test asserting generated
  `dist/sagas/<saga>/<arc>/<episode>/index.html` exposes the new episode
  discovery affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect a generated
episode page such as
`dist/sagas/hireflow/the-origin-blueprint/the-first-brick/index.html` to
verify:

- the page still reads like an episode detail page
- the page links directly to search and archive discovery surfaces
- the existing breadcrumb, metadata, body, and adjacent navigation remain
  unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- episode detail pages align with the current publication discovery surface
- `/sagas/<saga>/<arc>/<episode>/` pages expose deterministic links to
  `/search/` and `/archives/`
- deterministic tests cover the new episode-page affordances and unchanged
  static-only behavior
