# Slice: 2026-04-18 Search Noscript Recovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded recovery guidance for the existing static search surface:

- keep `/search/` backed by the published `search.json` artifact
- preserve the current deterministic query, ranking, highlight, and tag-surface
  contracts
- add explicit no-script recovery guidance when client-side search execution is
  unavailable

## Discovery Scope

The publication now has a coherent static search route, but its search behavior
still depends on browser-side script execution:

- `2026-04-17-search-page-bootstrap` established `/search/` as a client-side
  search surface
- later slices added URL-state coherence, ranking, highlighting, and result tag
  context
- the rendered page now looks richer, but it still gives no direct explanation
  when a reader reaches it without JavaScript available

That leaves one bounded recovery gap:

- the page offers a search form and query URL contract even though actual
  filtering requires script execution
- a no-script reader can land on `/search/` and see the input, but no explicit
  guidance explains the limitation or the next-best static routes
- the current page therefore preserves static hosting compatibility, but not a
  clear recovery path for this failure mode

This slice restores the minimum no-script recovery behavior needed for the
current static publication:

- render a deterministic `<noscript>` recovery shell on `/search/`
- explain that live search requires JavaScript
- point readers toward stable alternatives such as archives and library

This slice does not attempt server-side search, prerendered query results,
offline indexing, or a broader redesign of the search route.

## Use-Case Contract

### `RenderSearchNoscriptRecovery`

Given the existing static `/search/` route and its client-side filtering model,
render recovery guidance such that:

- a no-script reader is told clearly that live search requires JavaScript
- recovery guidance points only to stable reader-facing routes through explicit
  rows
- the message remains deterministic for the same repository state

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic page markup such that:

- the page still uses the current client-side search behavior when script
  execution is available
- the page exposes a bounded fallback message when script execution is not
  available
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- The search page must stay honest about its client-side execution requirement.
- No-script recovery guidance should point only to stable reader-facing routes
  such as `/archives/` and `/library/`.
- The slice stays bounded to fallback guidance and must not widen into
  prerendered search results, server-side search, or broader search-page
  redesign.
- The noscript shell should remain search-page specific and not affect script-
  enabled rendering.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing static `/search/` route and `search.json` artifact
- current discovery routes for `/archives/` and `/library/`

## Initial Test Plan

- unit test asserting generated `/search/` markup includes deterministic
  `<noscript>` recovery guidance
- unit test asserting the noscript message points to stable discovery routes
  rather than inventing a backend search fallback
- integration test asserting generated `dist/search/index.html` includes the
  bounded no-script recovery block while preserving the current static route
  contract
- integration test asserting the page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page artifact to verify:

- `/search/` still loads the published `search.json` artifact for script-enabled
  readers
- the page includes deterministic `<noscript>` recovery guidance
- the recovery message points to archives and library as stable alternatives
- ranking, highlighting, URL-state, and static-hosting assumptions remain
  unchanged

## Done Criteria

- `/search/` includes deterministic no-script recovery guidance
- the fallback message clearly states the client-side search requirement
- the page points no-script readers toward stable static routes
- deterministic tests cover the fallback block without widening the slice into
  broader search-product work
