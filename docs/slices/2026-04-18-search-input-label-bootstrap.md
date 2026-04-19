# Slice: 2026-04-18 Search Input Label Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded accessibility improvement for the existing static search surface:

- keep `/search/` backed by the published `search.json` artifact
- preserve the current deterministic query, ranking, highlighting, tag-surface,
  and recovery contracts
- add an explicit search input label and stable hook without changing the
  current route or client-side search behavior

## Discovery Scope

The publication now has a coherent static search route with several recovery
paths, but one small interaction detail still depends on a weak browser affordance:

- the search form currently exposes only a placeholder on the `<input>`
- placeholder text helps visual orientation, but it is not the same as an
  explicit field label
- the route therefore remains usable, but it still relies on a weaker input
  contract than the rest of the static search surface

This slice restores the minimum labeling behavior needed for the current static
publication:

- add one explicit label associated with the existing search input
- preserve the current placeholder, query-state behavior, and search-result
  rendering
- expose the label and input through stable class hooks for the page shell
- keep the change bounded to input semantics rather than redesigning the form

This slice does not attempt broader accessibility audits, keyboard shortcuts,
form-layout redesign, or changes to search ranking or recovery behavior.

## Use-Case Contract

### `RenderSearchInputLabel`

Given the existing static `/search/` route and search form, render deterministic
form markup such that:

- the search input has an explicit associated label
- the existing placeholder remains available as secondary guidance
- the label and input expose stable class hooks for the page shell
- the label remains stable for the same repository state

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic page markup such that:

- the page still uses the current client-side search behavior
- the search form becomes more explicit without changing its route contract
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- The search input should have one explicit associated label.
- Placeholder text may remain as secondary guidance, but it must not be the
  only descriptor for the field.
- The slice stays bounded to input labeling and must not widen into broader
  form redesign or search behavior changes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing `/search/` static route and search form markup
- current client-side search behavior on the labeled input

## Initial Test Plan

- unit test asserting generated `/search/` markup includes an explicit label for
  the search input
- unit test asserting the label targets the existing search input rather than a
  new field
- integration test asserting generated `dist/search/index.html` includes the
  bounded search-input label while preserving the current static route contract
- integration test asserting the page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page artifact to verify:

- `/search/` still renders the current search form and client-side behavior
- the search input now has one explicit associated label
- placeholder text, URL-state behavior, and current recovery surfaces remain
  unchanged
- static-hosting assumptions remain unchanged

## Done Criteria

- `/search/` includes an explicit label associated with the current search input
- the existing placeholder and client-side behavior remain unchanged
- rendering remains deterministic and static-only
- deterministic tests cover the label contract without widening the slice into
  broader search-product work
