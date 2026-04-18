# Slice: 2026-04-18 Search Submit Affordance Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded form-affordance improvement for the existing static search route:

- keep `/search/` backed by the published `search.json` artifact
- preserve the current deterministic query, ranking, highlighting, tag-surface,
  recovery, and form-semantics contracts
- add one explicit submit affordance to the existing search form without
  changing the current route or client-side search behavior

## Discovery Scope

The publication now has a labeled and described search input, but the form
still depends on one implicit interaction:

- the existing search form is submittable, but only through the keyboard Enter
  path or script-driven live updates
- the page therefore has a weaker visible submit contract than the rest of the
  search surface
- the route remains usable, but one bounded affordance is still missing from the
  form itself

This slice restores the minimum submit behavior needed for the current static
publication:

- add one explicit submit control to the existing search form
- preserve the current query-state behavior, placeholder, and search-result
  rendering
- keep the change bounded to form affordance rather than redesigning the search
  page

This slice does not attempt broader form-layout redesign, clear buttons,
keyboard shortcuts, or changes to search ranking or recovery behavior.

## Use-Case Contract

### `RenderSearchSubmitAffordance`

Given the existing static `/search/` route and search form, render deterministic
form markup such that:

- the form exposes one explicit submit control
- the existing search input remains the same field targeted by current
  client-side behavior
- the submit affordance remains stable for the same repository state

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic page markup such that:

- the page still uses the current client-side search behavior
- the search form gains an explicit submit path without changing its route
  contract
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- The existing search form should expose one explicit submit control.
- The submit affordance should preserve the current `/search/` query contract.
- The slice stays bounded to submit affordance and must not widen into broader
  form redesign or search behavior changes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing `/search/` static route and search form markup
- current client-side search behavior bound to the existing form

## Initial Test Plan

- unit test asserting generated `/search/` markup includes an explicit submit
  control in the existing search form
- unit test asserting the submit control keeps the current form contract rather
  than introducing a second search field or route
- integration test asserting generated `dist/search/index.html` includes the
  bounded submit affordance while preserving the current static route contract
- integration test asserting the page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page artifact to verify:

- `/search/` still renders the current labeled and described search form
- the form now exposes one explicit submit control
- current query-state behavior, status messaging, and recovery behavior remain
  unchanged
- static-hosting assumptions remain unchanged

## Done Criteria

- `/search/` includes one explicit submit affordance in the existing form
- current search behavior remains unchanged
- rendering remains deterministic and static-only
- deterministic tests cover the submit-affordance contract without widening the
  slice into broader search-product work
