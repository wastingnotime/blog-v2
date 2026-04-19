# Slice: 2026-04-18 Archives Row Presentation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded archives presentation refinement for the existing chronological hub:

- keep the current static builder, `/archives/` route, and chronological
  ordering
- preserve the existing archive-entry data and destination routes
- change only the reader-facing presentation of archive rows so the chronology
  hub reads like the rest of the refined publication surfaces

## Discovery Scope

The homepage, topic pages, library index, and sagas hub now use explicit
editorial row or chip treatment, but the chronological archive still renders
entries as plain generic list rows:

- `/archives/` already exposes the correct route and newest-first ordering
- archive entries already include the right title, date, optional saga
  context, and summary
- the archive therefore works functionally, but its row presentation lags
  behind the publication's other refined navigation surfaces

This slice restores the minimum archive continuity needed for the current
publication:

- render archive entries with an explicit row shell and compact header row
- keep date and optional saga context as quieter supporting metadata
- keep the same entry titles, summaries, chronology, and routes

This slice does not attempt archive grouping, pagination, counts by year,
archive intro changes, or redesign of other list surfaces.

## Use-Case Contract

### `RenderArchiveRows`

Given the existing chronological archive entries, render deterministic archive
markup such that:

- each entry has one clear primary title line linking to its current route
- date and optional saga context render in a compact row alongside the title
- summary remains present but visually secondary

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- `/archives/` reflects the bounded row-presentation refinement
- chronology, routes, and current discovery links remain unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- The chronological archive should read like a navigable editorial index, not a
  generic list.
- The slice stays bounded to archive-row presentation and must not widen into
  archive-product changes.
- Existing archive ordering and entry data remain the source of truth.
- The row shell should be archive-only and not affect the homepage, topic
  pages, or saga surfaces.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- archive-page renderer in `src/app/application/use_cases/build_site.py`
- existing archive projection from `project_archive_index`
- deterministic unit and integration coverage for generated archive output

## Initial Test Plan

- unit test asserting `/archives/` renders explicit archive-row presentation
  hooks
- unit test asserting archive rows keep the current chronology and supporting
  context
- integration test asserting generated `dist/archives/index.html` reflects the
  bounded row treatment
- integration test asserting topic pages and sagas hub remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/archives/index.html` to verify:

- archive entries render with explicit title, supporting metadata, and
  secondary summary treatment
- newest-first ordering remains unchanged
- routes and discovery links remain unchanged
- output remains fully static and deterministic

## Done Criteria

- `/archives/` renders discovered entries through explicit editorial row
  presentation
- current chronology, entry data, and routes remain unchanged
- deterministic tests cover the bounded archive refinement without widening
  into broader archive work
