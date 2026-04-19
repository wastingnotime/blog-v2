# Slice: 2026-04-18 Search Empty Results Recovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded zero-results recovery for the existing static search surface:

- keep `/search/` backed by the published `search.json` artifact
- preserve the current deterministic query, ranking, highlighting, tag-surface,
  and no-script recovery contracts
- add explicit recovery guidance when a query returns no matches

## Discovery Scope

The publication now has a coherent and well-explained static search route for
successful matches, but one bounded recovery gap still remains:

- the page already supports query URLs, ranking, highlighting, surfaced tags,
  and a no-script fallback
- when a query returns no matches, the current behavior is still limited to a
  plain `No results for "..."`
- the reader gets failure feedback, but not a useful next step inside the same
  search surface

This slice restores the minimum empty-results recovery behavior needed for the
current static publication:

- render deterministic recovery guidance when the current query yields no
  matches through an explicit recovery shell
- point readers toward stable static routes such as archives and library
- keep the change bounded to zero-results recovery rather than changing search
  ranking, indexing, or route structure

This slice does not attempt suggestions, synonyms, spell correction,
alternative-query generation, or a broader redesign of the search page.

## Use-Case Contract

### `RenderEmptySearchRecovery`

Given the current `/search/` route and a query with zero matches, render
bounded recovery behavior such that:

- the page states clearly that no matches were found
- the recovery surface points readers to stable reader-facing alternatives via
  explicit rows
- the behavior remains deterministic for the same query and repository state

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic client-side search behavior such that:

- successful matches still render through the current ranking and highlight
  paths
- zero-match queries expose bounded recovery guidance inside the page
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- Empty-results recovery should appear only when the current query yields zero
  matches.
- Recovery guidance should point only to stable reader-facing routes such as
  `/archives/` and `/library/`.
- The slice stays bounded to zero-results recovery and must not widen into
  generated suggestions, alternative queries, or backend search changes.
- The recovery shell should remain search-only and not affect successful
  results.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing static `search.json` publication artifact
- current browser-side result rendering on `/search/`
- current discovery routes for `/archives/` and `/library/`

## Initial Test Plan

- unit test asserting generated `/search/` markup exposes deterministic
  zero-results recovery behavior
- unit test asserting the recovery block points to stable discovery routes
  rather than inventing a backend search fallback
- integration test asserting generated `dist/search/index.html` includes the
  bounded zero-results recovery logic while preserving the current static route
  contract
- integration test asserting the page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page behavior to verify:

- successful queries still render through the current ranked result path
- zero-match queries expose deterministic recovery guidance
- the recovery guidance points to archives and library as stable alternatives
- URL-state, no-script fallback, and static-hosting assumptions remain
  unchanged

## Done Criteria

- `/search/` exposes deterministic recovery guidance for zero-match queries
- empty-results recovery points readers toward stable static routes
- successful result behavior remains unchanged
- deterministic tests cover the zero-results recovery path without widening the
  slice into broader search-product work
