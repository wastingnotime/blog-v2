# Slice: 2026-04-16 Saga Navigation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed content source under repository control

## Architecture Mode

Static-site builder with hierarchy-aware projections from the content catalog:

- project saga-level navigation pages from saga, arc, and episode records
- project arc-level index pages with deterministic episode ordering
- project episode pages with local narrative navigation metadata

## Discovery Scope

The current markdown bootstrap proves that repository-authored content can be
loaded and rendered, but it still leaves the narrative model under-specified:
readers can reach one episode from the homepage, yet the site does not expose a
clear saga -> arc -> episode path.

This slice restores the minimum navigation structure needed for a saga-oriented
blog:

- a saga landing page that lists arcs and timeline entries
- an arc landing page that lists its episodes
- episode-level navigation back to parent structures and adjacent episodes when
  available

This slice does not attempt tags, RSS, search, archive pages, or full visual
parity with the old Go templates.

## Use-Case Contract

### `BuildSagaNavigationPages`

Given the loaded content catalog and site settings, generate deterministic
static output under `dist/` such that:

- each saga has a landing page with summary plus navigable arc links
- each arc has a landing page with ordered episode links
- saga and arc pages can be traversed without an application server
- generated links remain compatible with static hosting
- generated output contains no same-origin `/api` dependency

### `ProjectNarrativeNavigation`

Given saga, arc, and episode records, compute deterministic navigation metadata
for rendering:

- saga timeline entries ordered by episode metadata
- arc episode ordering based on explicit number, then stable metadata fallback
- previous and next episode references within an arc when applicable
- parent saga and arc references for breadcrumb-style navigation

## Main Business Rules

- A saga is a navigable narrative container, not only a metadata label.
- Arc pages must preserve the distinction between the saga container and the
  ordered episodes within that arc.
- Episode ordering must be deterministic and repository-derived, not inferred
  from filesystem traversal alone.
- Navigation must degrade cleanly for the first or last episode in an arc.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for content sources
- filesystem writer for build artifacts
- environment reader for site settings

## Initial Test Plan

- unit test for deterministic saga timeline projection from content metadata
- unit test for arc episode ordering and previous/next navigation projection
- integration test for generating:
  - `dist/sagas/hireflow/index.html`
  - `dist/sagas/hireflow/the-origin-blueprint/index.html`
  - episode pages with parent and adjacent-navigation links
- integration test asserting generated HTML stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
site to verify:

- the HireFlow saga page lists its arcs and episode timeline
- the arc page lists episode links in deterministic order
- the episode page links back to its arc and saga and exposes previous or next
  navigation when relevant
- links are static and traversable without an application server

## Done Criteria

- saga pages expose arc and timeline navigation instead of only summary text
- an arc route is generated successfully for the in-repo content set
- episode pages expose parent navigation and adjacent-episode navigation when
  available
- deterministic tests cover projection and generated output

