# Slice: 2026-04-17 Page Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic standalone-page discovery update for the expanded publication
surface:

- revise standalone page rendering so it exposes the current complementary
  discovery routes
- add bounded affordances for Search and Archives alongside the existing entry
  metadata and authored body
- keep the slice limited to standalone-page discovery copy and links

## Discovery Scope

The publication now exposes stable reader-facing discovery routes for
standalone pages, archives, and search. Standalone pages still reflect an
earlier site shape and behave as isolated reading surfaces aside from their tag
links.

That gap is visible in current repository artifacts:

- `build_content_page(...)` renders entry metadata and the authored markdown
  body, but no complementary discovery affordance for `/archives/` or
  `/search/`
- standalone pages such as `/about/` are meaningful reader-facing routes, not
  just incidental content leaves
- archives and search are now first-class routes with shared-navigation
  discoverability, but standalone pages do not acknowledge them explicitly

This slice restores the minimum page discovery surface needed for the current
publication:

- update standalone pages so they link readers to `/archives/` and `/search/`
- preserve the existing entry metadata and authored body rendering
- keep the change bounded to standalone-page discovery copy and links

This slice does not attempt broader page-template redesign, related-content
algorithms, author bios, or search behavior changes.

## Use-Case Contract

### `BuildContentPage`

Given a standalone page and the current reader-facing routes, generate
deterministic static output for `/<slug>/` such that:

- the page continues to render entry metadata and authored markdown content
- readers can reach search and archives directly from the page
- output remains fully static and compatible with GitHub Pages hosting

### `RenderPageDiscovery`

Given a standalone page route and current publication surfaces, render bounded
discovery content such that:

- the page still centers the authored content as its primary job
- archives and search are visibly represented as complementary discovery paths
- the section remains publication-oriented rather than turning into generic
  navigation chrome

## Main Business Rules

- Standalone-page discovery copy must stay aligned with the routes the
  publication now exposes.
- Page discovery affordances should point to stable reader-facing routes, not
  implementation artifacts.
- The slice stays bounded to standalone-page copy and linking rather than
  changing page metadata projection or shared navigation.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing standalone-page renderer
- environment reader for site settings
- existing stable routes for `/search/`, `/archives/`, and `/<slug>/`

## Initial Test Plan

- unit test asserting a standalone page links directly to `/archives/` and
  `/search/`
- unit test asserting the existing entry metadata and authored body remain
  present
- integration test asserting generated `dist/about/index.html` exposes the new
  page discovery affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect a generated
standalone page such as `dist/about/index.html` to verify:

- the page still reads like a standalone authored page
- the page links directly to search and archive discovery surfaces
- the existing metadata and body content remain unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- standalone pages align with the current publication discovery surface
- `/<slug>/` pages expose deterministic links to `/search/` and `/archives/`
- deterministic tests cover the new page affordances and unchanged static-only
  behavior
