# Slice: 2026-04-18 Search Result Presentation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded presentation refinement for the existing static search results:

- keep the current static builder, `/search/` route, and `search.json` model
- preserve the existing query, ranking, highlighting, and recovery behavior
- change only the reader-facing presentation hooks used when browser-side
  results render

## Discovery Scope

The search route now has explicit input semantics, URL state, ranking,
highlighting, tag surfacing, recovery behavior, and shared discovery
navigation. One visible gap still remains:

- rendered search results are still built as plain generic DOM nodes
- metadata, summary, and tag context appear functionally, but without a
  coherent result-row presentation contract
- this makes the route feel less integrated with the publication's refined
  editorial surfaces

This slice restores the minimum search-result continuity needed for the current
publication:

- render result rows with explicit title, metadata, summary, and tag hooks
- keep the same ranking, highlighting, and recovery messages intact
- preserve the existing fully static search model

This slice does not attempt search-product changes such as suggestions, backend
search, filtering, or ranking redesign.

## Use-Case Contract

### `RenderSearchResults`

Given the existing browser-side search results, render deterministic result-row
markup such that:

- each result has one clear primary title line
- metadata and summary render as quieter supporting context
- surfaced tags remain secondary context and keep the current highlight
  behavior

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- `/search/` reflects the bounded result-presentation refinement
- current search ranking, highlighting, recovery, and route behavior remain
  unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- Search should keep its current static behavior while gaining a clearer result
  presentation contract.
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
  result-presentation hooks
- unit test asserting the browser-side renderer applies those hooks without
  changing ranking or highlight logic
- integration test asserting generated `dist/search/index.html` reflects the
  bounded result-row treatment
- integration test asserting shared discovery and recovery behavior remain
  unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/search/index.html` to verify:

- search results render with explicit row, metadata, summary, and tag hooks
- ranking, highlighting, and recovery behavior remain unchanged
- the route stays fully static and deterministic

## Done Criteria

- `/search/` renders result rows through explicit presentation hooks
- current search behavior and recovery remain unchanged
- deterministic tests cover the bounded result-presentation refinement without
  widening into broader search-product work
