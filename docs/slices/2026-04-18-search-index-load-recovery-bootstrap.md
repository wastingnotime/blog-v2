# Slice: 2026-04-18 Search Index Load Recovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded load-failure recovery for the existing static search surface:

- keep `/search/` backed by the published `search.json` artifact
- preserve the current deterministic query, ranking, highlighting, tag-surface,
  no-script, and empty-results recovery contracts
- add explicit recovery guidance when the search index cannot be loaded

## Discovery Scope

The publication now has a coherent static search route for successful queries
and several reader-facing recovery paths, but one bounded failure mode still
remains underexplained:

- `/search/` depends on fetching the static `search.json` artifact at runtime
- when that fetch fails, the current behavior drops to a plain `Search index
  could not be loaded.`
- the page acknowledges the failure, but it does not provide a concrete next
  step inside the current static publication

This slice restores the minimum load-failure recovery behavior needed for the
current static publication:

- render deterministic recovery guidance when `search.json` cannot be loaded
- point readers toward stable static routes such as archives and library
- keep the change bounded to load-failure recovery rather than changing the
  search artifact or introducing backend behavior

This slice does not attempt offline caching, retry loops, mirrored search
artifacts, or a broader redesign of the search page.

## Use-Case Contract

### `RenderSearchIndexLoadRecovery`

Given the existing `/search/` route and a failure to load the static search
index, render bounded recovery behavior such that:

- the page states clearly that the search index is unavailable
- recovery guidance points readers toward stable reader-facing alternatives
- the behavior remains deterministic for the same repository state

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic client-side search behavior such that:

- successful index loads still use the current ranking and rendering path
- load failures expose bounded recovery guidance inside the page
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- Load-failure recovery should appear only when the page cannot load the static
  `search.json` artifact.
- Recovery guidance should point only to stable reader-facing routes such as
  `/archives/` and `/library/`.
- The slice stays bounded to load-failure recovery and must not widen into
  retries, offline indexing, or backend search changes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing static `search.json` publication artifact
- current browser-side fetch path on `/search/`
- current discovery routes for `/archives/` and `/library/`

## Initial Test Plan

- unit test asserting generated `/search/` markup exposes deterministic
  load-failure recovery behavior
- unit test asserting the recovery block points to stable discovery routes
  rather than inventing a backend search fallback
- integration test asserting generated `dist/search/index.html` includes the
  bounded load-failure recovery logic while preserving the current static route
  contract
- integration test asserting the page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page artifact to verify:

- successful index loads still use the current ranked result path
- the generated page includes deterministic recovery guidance for load failure
- the recovery guidance points to archives and library as stable alternatives
- URL-state, no-script recovery, and zero-results recovery remain unchanged

## Done Criteria

- `/search/` exposes deterministic recovery guidance for search-index load
  failure
- load-failure recovery points readers toward stable static routes
- successful search behavior remains unchanged
- deterministic tests cover the load-failure recovery path without widening the
  slice into broader search-product work
