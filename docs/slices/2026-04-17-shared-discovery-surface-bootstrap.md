# Slice: 2026-04-17 Shared Discovery Surface Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic shared discovery-surface update for the expanded publication:

- restore one bounded discovery section shape across generated route families
- keep route-level discovery links aligned without repeating ad hoc copy in
  each page builder
- stay within the current static publication contract and existing route set

## Discovery Scope

The publication now exposes stable reader-facing routes for archives, search,
library, sagas, studio, and standalone reading surfaces. Recent slices restored
discovery guidance across most route families, but that guidance is now encoded
as repeated hard-coded paragraphs inside multiple page builders.

That pressure is visible in current repository artifacts:

- `build_archive_page(...)`, `build_search_page(...)`, `build_page(...)`,
  `build_episode_page(...)`, `build_saga_page(...)`, `build_arc_page(...)`,
  `build_library_page(...)`, `build_topic_page(...)`, `build_sagas_index_page(...)`,
  and `build_studio_page(...)` all render route-discovery copy directly inside
  `build_site.py`
- the wording and structure already drift slightly by page family, even when
  the intent is the same
- further route-level discovery changes will keep getting more expensive and
  easier to desynchronize if each builder owns its own discovery markup

This slice restores the minimum shared discovery behavior needed for the
current publication:

- render one consistent discovery section shape for generated HTML pages that
  expose complementary routes
- allow each route family to declare which stable reader-facing destinations it
  should surface
- keep the slice bounded to shared discovery rendering rather than changing the
  current route inventory or broader information architecture

This slice does not add new routes, change search behavior, redesign shared
navigation, or move authored markdown into a CMS-like composition model.

## Use-Case Contract

### `RenderDiscoverySurface`

Given the current route being rendered and a bounded set of complementary
reader-facing destinations, render deterministic discovery markup such that:

- the section has a stable structure across generated pages
- the current route is not redundantly listed as one of its own discovery
  destinations
- only first-class static publication routes are surfaced

### `BuildPageWithDiscoverySurface`

Given any generated page that should expose additional ways into the
publication, include the shared discovery surface such that:

- the route keeps its current primary content role
- discovery links remain complementary rather than replacing the page's main
  job
- output stays fully static and compatible with GitHub Pages hosting

## Main Business Rules

- Discovery guidance should be rendered through one bounded shared surface
  rather than many ad hoc inline fragments.
- Discovery destinations must point only to stable reader-facing routes.
- A route must not list itself inside its own discovery surface.
- The shared discovery surface should preserve current route-level intent rather
  than forcing every page to expose the exact same destinations.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing page builders in `build_site.py`
- existing stable routes for `/archives/`, `/search/`, `/library/`, and any
  other surfaced top-level destinations
- current document rendering flow in `_render_document(...)`

## Initial Test Plan

- unit test asserting representative route families render the same discovery
  section shape
- unit test asserting discovery destinations remain route-specific and do not
  include the current route
- integration test asserting generated artifacts still expose the expected
  discovery links after the shared rendering change
- integration test asserting the output remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect representative
generated artifacts such as:

- `dist/archives/index.html`
- `dist/search/index.html`
- `dist/library/index.html`
- one narrative route such as an episode page

Verify that:

- each page exposes a shared discovery section shape
- each page still links only to complementary destinations for that route
- the page's primary content remains unchanged
- the artifacts remain fully static and compatible with GitHub Pages

## Done Criteria

- route-level discovery guidance is rendered through one bounded shared surface
- representative route families keep their intended complementary destinations
- deterministic tests cover both shared structure and route-specific link sets
- generated output remains static-only and GitHub Pages compatible
