# Slice: 2026-04-18 Search Results Label Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded results-surface improvement for the existing static search route:

- keep `/search/` backed by the published `search.json` artifact
- preserve the current deterministic query, ranking, highlighting, tag-surface,
  recovery, and form-semantics contracts
- add an explicit label for the existing results container without changing the
  current route or client-side behavior

## Discovery Scope

The publication now has a coherent static search form and status surface, but
one result-structure detail still remains implicit:

- the page renders matches into `#search-results`
- the list is the primary container for successful search output and some
  recovery content
- that container still has no explicit label tying it back to the search route
  or current result meaning

This slice restores the minimum results-labeling behavior needed for the
current static publication:

- add one explicit label reference for the existing results container
- preserve the current item rendering, status text, and recovery behavior
- keep the change bounded to container semantics rather than redesigning result
  layout

This slice does not attempt result focus management, keyboard navigation,
virtualization, or changes to search ranking or recovery behavior.

## Use-Case Contract

### `RenderSearchResultsContainer`

Given the existing static `/search/` route and results list, render
deterministic markup such that:

- the results container has one explicit accessible label
- the current container identity remains stable for the same repository state
- existing result and recovery rendering still target the same node

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic page markup such that:

- the page still uses the current client-side search behavior
- the results surface becomes more explicit without changing its rendering path
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- The existing results container should carry one explicit label.
- Current result rendering and recovery behavior must keep targeting the same
  container.
- The slice stays bounded to results-container semantics and must not widen into
  broader result-layout or search behavior changes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing `/search/` static route and `#search-results` markup
- current client-side rendering path that appends matches and recovery content
  into the results container

## Initial Test Plan

- unit test asserting generated `/search/` markup gives the results container an
  explicit label contract
- unit test asserting the current results node remains the same node targeted by
  existing client-side rendering
- integration test asserting generated `dist/search/index.html` includes the
  bounded results-container label while preserving the current static route
  contract
- integration test asserting the page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page artifact to verify:

- `/search/` still renders the current search form and client-side behavior
- `#search-results` now has an explicit label contract
- current result rendering, status updates, and recovery behavior remain
  unchanged
- static-hosting assumptions remain unchanged

## Done Criteria

- `/search/` gives the existing results container an explicit label contract
- current result rendering and recovery behavior remain unchanged
- rendering remains deterministic and static-only
- deterministic tests cover the results-container contract without widening the
  slice into broader search-product work
