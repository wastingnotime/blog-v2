# Slice: 2026-04-18 Search Status Live Region Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded announcement improvement for the existing static search surface:

- keep `/search/` backed by the published `search.json` artifact
- preserve the current deterministic query, ranking, highlighting, tag-surface,
  and recovery contracts
- add explicit live-region semantics to the existing status surface without
  changing the current route or client-side search behavior

## Discovery Scope

The publication now has a coherent static search route with explicit form and
recovery behavior, but one dynamic interaction detail still relies on implicit
browser behavior:

- the page updates `#search-status` in place as queries change
- that status already communicates result counts and recovery states
- the status region still has no explicit live-announcement contract even though
  it is the main dynamic feedback surface on the page

This slice restores the minimum live-announcement behavior needed for the
current static publication:

- declare the existing search status surface as a polite live region with an
  explicit status role
- preserve the current status text and in-place update behavior
- keep the change bounded to status semantics rather than redesigning the
  search page

This slice does not attempt broader accessibility audits, keyboard shortcuts,
result focus management, or changes to search ranking or recovery behavior.

## Use-Case Contract

### `RenderSearchStatusRegion`

Given the existing static `/search/` route and search feedback surface, render
deterministic markup such that:

- the existing status region is explicitly identified as dynamic feedback via
  a status role
- current status text remains the source of result-count and recovery messaging
- the region remains stable for the same repository state

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic page markup such that:

- the page still uses the current client-side search behavior
- the status surface becomes a bounded live region without changing its text
  contract
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- The existing search status surface should carry one explicit live-region
  contract.
- Current status messages remain authoritative; the slice should not invent a
  second competing feedback surface.
- The slice stays bounded to status semantics and must not widen into broader
  accessibility redesign or search behavior changes.
- The status role should remain search-page specific and not affect other
  feedback surfaces.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing `/search/` static route and `#search-status` markup
- current client-side search updates that already write into the status region

## Initial Test Plan

- unit test asserting generated `/search/` markup gives `#search-status`
  explicit live-region semantics
- unit test asserting the current status element remains the same node targeted
  by the existing client-side search behavior
- integration test asserting generated `dist/search/index.html` includes the
  bounded live-region attributes while preserving the current static route
  contract
- integration test asserting the page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page artifact to verify:

- `/search/` still renders the current search form and client-side behavior
- `#search-status` now carries explicit live-region semantics
- current result-count and recovery messages remain unchanged
- static-hosting assumptions remain unchanged

## Done Criteria

- `/search/` gives the existing status region explicit live-region semantics
- current status messages and client-side behavior remain unchanged
- rendering remains deterministic and static-only
- deterministic tests cover the status-region contract without widening the
  slice into broader search-product work
