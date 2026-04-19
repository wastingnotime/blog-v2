# Slice: 2026-04-19 Search Result Row Emphasis Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded presentation refinement for the existing static search results:

- keep the current static builder, `/search/` route, and `search.json` model
- preserve the existing query, ranking, highlighting, tag surfacing, and
  recovery behavior
- add explicit row treatment to search results so the result surface reads like
  the rest of the publication's editorial navigation surfaces

## Discovery Scope

The search route now has explicit input semantics, URL state, ranking,
highlighting, tag surfacing, recovery behavior, and chip-like tag context. One
visible gap still remains:

- rendered search results still sit inside plain list items without a dedicated
  row shell
- metadata, summary, and tags are visible, but the result surface still reads
  flatter than the rest of the refined publication
- the current items therefore work functionally but do not yet feel like
  intentional search-result cards

This slice restores the minimum row-emphasis continuity needed for the current
publication:

- render search results with explicit item-shell treatment
- keep the same ranking, highlighting, and recovery messages intact
- preserve the existing fully static search model

This slice does not attempt search-product changes such as suggestions, backend
search, filtering, or ranking redesign.

## Use-Case Contract

### `RenderSearchResults`

Given the existing browser-side search results, render deterministic result-row
markup such that:

- each result keeps the current title, metadata, summary, and tag hooks
- the row itself gains a dedicated shell treatment distinct from the list
  container
- surfaced tags remain secondary context and keep the current highlight
  behavior

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- `/search/` reflects the bounded result-row emphasis refinement
- current search ranking, highlighting, recovery, and route behavior remain
  unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- Search should keep its current static behavior while gaining a clearer
  result-row contract.
- The slice stays bounded to presentation and must not widen into search
  product behavior changes.
- Existing query handling, ranking, and result data remain the source of truth.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- search-page renderer in `src/app/application/use_cases/build_site.py`
- existing browser-side result-rendering script on `/search/`
- deterministic unit and integration coverage for generated search output

## Initial Test Plan

- unit test asserting generated `/search/` markup includes explicit
  result-row shell hooks
- unit test asserting the browser-side renderer applies those hooks without
  changing ranking or highlight logic
- integration test asserting generated `dist/search/index.html` reflects the
  bounded row-shell treatment
- integration test asserting shared discovery and recovery behavior remain
  unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect `dist/search/index.html`
to verify:

- search results render with explicit row-shell treatment
- ranking, highlighting, and recovery behavior remain unchanged
- the route stays fully static and deterministic

## Done Criteria

- `/search/` renders result rows through explicit shell treatment
- current search behavior and recovery remain unchanged
- deterministic tests cover the bounded row-emphasis refinement without
  widening into broader search-product work
