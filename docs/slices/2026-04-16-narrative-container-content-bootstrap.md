# Slice: 2026-04-16 Narrative Container Content Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed content source under repository control

## Architecture Mode

Static-site builder with authored content on narrative container routes:

- retain markdown body content for saga and arc records
- render authored container copy alongside existing navigation projections
- keep saga and arc pages static, deterministic, and repository-driven

## Discovery Scope

The current slices restore authored content for entries and section hubs, but
the saga and arc containers still drop the markdown body already present in
their source files. Their pages render summaries plus navigation only, which
leaves container routes thinner than both the authored source material and the
rest of the publication surface.

This slice restores the minimum authored narrative content needed for container
routes to behave like real publication surfaces:

- preserve markdown body content for saga records
- preserve markdown body content for arc records
- render that authored copy before the existing arc and episode navigation

This slice does not attempt per-container reading time, richer container tags,
or redesign of the existing narrative navigation structure.

## Use-Case Contract

### `LoadNarrativeContainerContent`

Given saga and arc markdown sources, load deterministic typed records such that:

- saga records retain authored markdown body content
- arc records retain authored markdown body content
- missing or malformed container content still fails deterministically

### `BuildSagaContainerPage`

Given a saga record with authored body content and existing saga projections,
generate deterministic static output for `/sagas/<slug>/` such that:

- the page renders authored saga body content
- the page still lists arcs and the saga timeline
- the route remains compatible with static hosting

### `BuildArcContainerPage`

Given an arc record with authored body content and existing arc projections,
generate deterministic static output for `/sagas/<saga>/<arc>/` such that:

- the page renders authored arc body content
- the page still lists its ordered episodes
- the route remains compatible with static hosting

## Main Business Rules

- Saga and arc container pages should render repository-authored markdown when
  that content exists.
- Container body content must be loaded from the same repository sources that
  already define their summaries and metadata.
- Existing narrative navigation remains intact; authored container content is
  additive, not a replacement for arc and episode lists.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for content sources
- filesystem writer for build artifacts
- environment reader for site settings

## Initial Test Plan

- unit test for loading saga and arc body markdown into typed records
- integration test asserting saga pages render authored container copy plus arc
  and timeline navigation
- integration test asserting arc pages render authored container copy plus
  episode links
- integration test asserting generated HTML stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
container pages to verify:

- the HireFlow saga page renders its authored intro copy from markdown
- the Origin Blueprint arc page renders its authored intro copy from markdown
- both pages keep their existing navigation outcomes
- the routes remain fully static and traversable without an application server

## Done Criteria

- saga records retain authored markdown body content
- arc records retain authored markdown body content
- saga and arc routes render authored container copy before their navigation
  lists
- deterministic tests cover loading and rendering of container content
