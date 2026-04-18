# Slice: 2026-04-18 Sagas Index Presentation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded sagas-index presentation refinement for the existing section hub:

- keep the current static builder, `/sagas/` route, and saga-summary data
- preserve the existing active-saga ordering and start-reading links
- change only the reader-facing presentation of saga rows so the sagas hub
  reads more like the rest of the refined publication surfaces

## Discovery Scope

The homepage, library index, and topic pages now use explicit editorial row or
chip treatment, but the sagas section hub still renders its active sagas
through plain list rows:

- `/sagas/` already exposes the right route and correct saga links
- saga summaries and optional start-reading links are already projected
- the section hub therefore works functionally, but its row presentation still
  lags behind the publication's recent surface refinements

This slice restores the minimum sagas-index continuity needed for the current
publication:

- render active saga rows with explicit title and secondary-summary treatment
- keep the existing start-reading affordance intact
- preserve the same saga order, routes, and discovery links

This slice does not attempt new saga metadata, saga counts on the hub,
timeline redesign, homepage changes, or archive/list redesign outside
`/sagas/`.

## Use-Case Contract

### `RenderSagasIndexRows`

Given the existing active-saga summaries, render deterministic sagas-index
markup such that:

- each saga row has one clear primary title line
- summary remains present as quieter supporting text
- the existing start-reading affordance remains intact when available

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- `/sagas/` reflects the bounded row-presentation refinement
- saga ordering, routes, and current discovery links remain unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- The sagas section hub should read like a publication navigation surface, not
  a generic list.
- The slice stays bounded to sagas-index row presentation and must not widen
  into saga-product changes.
- Existing saga-summary data and start-reading routes remain the source of
  truth.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- sagas-index renderer in `src/app/application/use_cases/build_site.py`
- existing saga-summary projection from `project_section_hubs`
- deterministic unit and integration coverage for generated sagas-index output

## Initial Test Plan

- unit test asserting `/sagas/` renders explicit saga-row presentation hooks
- unit test asserting start-reading links remain intact for sagas that have
  them
- integration test asserting generated `dist/sagas/index.html` reflects the
  bounded row treatment
- integration test asserting homepage and saga pages remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/sagas/index.html` to verify:

- active sagas render with explicit title and secondary-summary treatment
- start-reading links still resolve to the first episode when available
- route, ordering, and discovery links remain unchanged
- output remains fully static and deterministic

## Done Criteria

- `/sagas/` renders active sagas through explicit editorial row presentation
- current saga ordering, routes, and start-reading affordances remain unchanged
- deterministic tests cover the bounded sagas-index refinement without widening
  into broader saga work
