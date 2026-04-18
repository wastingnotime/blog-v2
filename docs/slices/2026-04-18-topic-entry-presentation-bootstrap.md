# Slice: 2026-04-18 Topic Entry Presentation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded topic-page presentation refinement for discovered tagged entries:

- keep the current static builder, discovered topics, and `/library/<tag>/`
  routes
- preserve the existing topic-entry data and ordering
- change only the reader-facing presentation of topic-page entry rows so topic
  pages read more like editorial navigation surfaces

## Discovery Scope

The library index now renders topics as outlined chips, but topic pages still
present their entries through plain generic list rows:

- topic discovery, topic routing, and entry ordering are already working
- `/library/<tag>/` still renders title, metadata, and summary without an
  explicit topic-page presentation contract
- the publication's recent homepage refinements and predecessor signals both
  point toward quieter metadata and secondary summaries rather than plain
  default list output

This slice restores the minimum topic-page continuity needed after the library
index refinement:

- render topic entries with explicit topic-page row markup
- keep date and optional saga context as quieter supporting metadata
- keep the same topic-entry titles, summaries, and routes

This slice does not attempt topic counts, tag hierarchies, faceted filtering,
topic-page intro copy changes, or archive/list redesign outside topic pages.

## Use-Case Contract

### `RenderTopicEntries`

Given the existing discovered entries for one topic page, render deterministic
topic-page markup such that:

- each entry has one clear primary title line linking to its current route
- date and optional saga context render as quieter supporting metadata
- summary remains present but visually secondary

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- `/library/<tag>/` reflects the bounded topic-entry presentation refinement
- discovered topic-entry ordering, routes, and library-index behavior remain
  unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- Topic pages should read like navigable editorial collections, not generic
  unstyled lists.
- The slice stays bounded to topic-page entry presentation and must not widen
  into taxonomy-product changes.
- Existing topic-entry data and ordering remain the source of truth.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- topic-page renderer in `src/app/application/use_cases/build_site.py`
- existing topic-entry projection from `project_topic_catalog`
- deterministic unit and integration coverage for generated topic-page output

## Initial Test Plan

- unit test asserting `/library/<tag>/` renders explicit topic-entry row hooks
- unit test asserting topic-entry rows keep the current routes and supporting
  context
- integration test asserting generated topic pages reflect the bounded row
  treatment
- integration test asserting library-index chips and discovery links remain
  unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/library/architecture/index.html` to verify:

- topic entries render with explicit title, supporting metadata, and secondary
  summary treatment
- entry links still resolve to the current page and episode routes
- library-index chips and topic routing remain unchanged
- output remains fully static and deterministic

## Done Criteria

- topic pages render discovered entries through explicit editorial row
  presentation
- current topic-entry data, ordering, and routes remain unchanged
- deterministic tests cover the bounded topic-page refinement without widening
  into broader taxonomy work
