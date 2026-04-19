# Slice: 2026-04-18 Search Input Description Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded form-description improvement for the existing static search surface:

- keep `/search/` backed by the published `search.json` artifact
- preserve the current deterministic query, ranking, highlighting, tag-surface,
  recovery, label, and live-region contracts
- tie the existing search input explicitly to its helper and status surfaces
  without changing the current route or client-side behavior

## Discovery Scope

The publication now has a labeled search input and an explicit live status
region, but one form-semantics gap still remains:

- the page already renders helper copy and dynamic status text adjacent to the
  input
- the input itself is not explicitly associated with those explanatory surfaces
- the page therefore keeps one weaker form-description contract even though the
  descriptive text already exists in the markup

This slice restores the minimum description behavior needed for the current
static publication:

- associate the existing search input with helper and status text through one
  explicit description contract
- keep the change bounded to form semantics rather than redesigning the search
  page

This slice does not attempt broader accessibility audits, form-layout redesign,
keyboard shortcuts, or changes to search ranking or recovery behavior.

## Use-Case Contract

### `RenderSearchInputDescription`

Given the existing static `/search/` route and search form, render deterministic
form markup such that:

- the current search input is explicitly associated with its helper and status
  surfaces through description semantics
- existing helper and status text remain unchanged
- the association remains stable for the same repository state

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic page markup such that:

- the page still uses the current client-side search behavior
- the search form becomes more explicit without changing its route contract
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- The existing search input should explicitly reference the descriptive surfaces
  that already explain the field.
- The existing helper copy and status messaging remain authoritative; the slice
  must not invent a second competing guidance surface.
- The slice stays bounded to input-description semantics and must not widen into
  broader form redesign or search behavior changes.
- The description contract should remain search-page specific and not affect
  other form surfaces.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing `/search/` static route and search form markup
- current helper and status surfaces already rendered adjacent to the input

## Initial Test Plan

- unit test asserting generated `/search/` markup gives the search input an
  explicit description contract
- unit test asserting the input references the existing helper and status nodes
  rather than new duplicate elements
- integration test asserting generated `dist/search/index.html` includes the
  bounded description attributes while preserving the current static route
  contract
- integration test asserting the page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page artifact to verify:

- `/search/` still renders the current labeled search form and client-side
  behavior
- the search input now references the existing helper and status surfaces
- current helper text, status text, and recovery behavior remain unchanged
- static-hosting assumptions remain unchanged

## Done Criteria

- `/search/` gives the existing search input an explicit description contract
- current helper and status text remain unchanged
- rendering remains deterministic and static-only
- deterministic tests cover the form-description contract without widening the
  slice into broader search-product work
