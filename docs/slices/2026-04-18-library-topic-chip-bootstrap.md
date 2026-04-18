# Slice: 2026-04-18 Library Topic Chip Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded library-index presentation refinement for discovered topics:

- keep the current static builder, topic discovery, and `/library/` route
- preserve the existing discovered tag set and topic-page routing
- change only the reader-facing presentation of library topics so the library
  index better reflects the predecessor's outlined topic treatment

## Discovery Scope

The homepage now carries a more compact editorial rhythm, but the library index
still presents topics as a plain unordered list of links:

- topic discovery and routing are already working
- `/library/` still renders discovered tags without any distinct editorial
  treatment
- the extracted predecessor style signals explicitly include outlined topic
  chips or pills rather than plain list links

This slice restores the minimum library-topic continuity needed for the current
publication:

- render discovered topics on `/library/` with explicit chip-like markup and
  styling
- keep the same discovered tag set and destination routes
- preserve the existing authored library intro and discovery links

This slice does not attempt topic counts, topic summaries, faceted filtering,
topic-page redesign, or broader taxonomy changes.

## Use-Case Contract

### `RenderLibraryTopicChips`

Given the existing discovered library topics, render deterministic library
markup such that:

- each topic remains a link to its current `/library/<tag>/` route
- topics render with one explicit chip-like presentation contract
- the same repository state yields the same topic ordering and destinations

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- `/library/` reflects the bounded topic-chip treatment
- topic discovery, topic routing, and current library copy remain unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- The library index should visually distinguish topics from generic prose or
  ordinary list links.
- The slice stays bounded to library-index topic presentation and must not
  widen into taxonomy-product changes.
- Existing discovered topics and topic routes remain the source of truth.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- library-page renderer in `src/app/application/use_cases/build_site.py`
- existing discovered-topic projection from `project_topic_catalog`
- deterministic unit and integration coverage for generated library output

## Initial Test Plan

- unit test asserting `/library/` renders explicit topic-chip markup for
  discovered topics
- unit test asserting topic-chip links still target the current topic routes
- integration test asserting generated `dist/library/index.html` reflects the
  bounded topic-chip treatment
- integration test asserting topic pages and discovery links remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/library/index.html` to verify:

- discovered topics render as outlined chip-like links
- topic links still resolve to current `/library/<tag>/` pages
- authored library copy and discovery links remain intact
- output remains fully static and deterministic

## Done Criteria

- `/library/` renders discovered topics through explicit chip-like presentation
- current topic routes and discovered-topic data remain unchanged
- deterministic tests cover the bounded library-index refinement without
  widening into broader taxonomy work
