# Slice: 2026-04-18 Entry Tag Chip Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded entry-metadata presentation refinement for standalone pages and saga
episodes:

- keep the current static builder, page routes, episode routes, and metadata
  facts
- preserve the existing publication date, reading-time, and tag-link
  destinations
- change only the reader-facing presentation of tag links inside entry
  metadata so article headers read closer to the publication's outlined topic
  language

## Discovery Scope

The library index now uses explicit topic chips, but long-form entry headers
still surface tags as plain inline links inside the metadata line:

- page and episode routes already expose the correct tag destinations
- entry metadata already includes publication date, reading time, and the right
  tag set
- the extracted predecessor style signals explicitly include outlined topic
  chips or pills as part of the publication's discovery language
- tag links therefore work functionally today, but their current presentation
  lags behind the bounded chip treatment already used on `/library/`

This slice restores the minimum entry-header continuity needed now:

- render page and episode tag links through explicit chip-like metadata hooks
- keep the same tag labels and destination routes
- preserve the current publication date and reading-time facts

This slice does not attempt related-entry surfacing, taxonomy changes,
click-through analytics, or broader article-header redesign.

## Use-Case Contract

### `RenderEntryMetadata`

Given existing page or episode entry metadata, render deterministic metadata
markup such that:

- publication date and reading time remain visible and unchanged
- tags, when present, render through one explicit chip-like presentation
  contract
- each chip remains a link to the existing `/library/<tag>/` route

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- long-form page and episode routes reflect the bounded entry-tag chip
  refinement
- current routes, metadata facts, and discovery behavior remain unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- Entry-header tags should read like part of the publication's established
  topic language rather than plain inline metadata.
- The slice stays bounded to tag presentation inside entry metadata and must
  not widen into content-model or taxonomy changes.
- Existing publication date, reading time, tag labels, and routes remain the
  source of truth.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- entry-metadata renderer in `src/app/application/use_cases/build_site.py`
- existing page and episode metadata projections from `project_entry_metadata`
- deterministic unit and integration coverage for generated long-form output

## Initial Test Plan

- unit test asserting page and episode metadata render explicit entry-tag chip
  hooks when tags are present
- unit test asserting entry-tag chips keep the current labels and `/library/`
  destinations
- integration test asserting generated long-form routes reflect the bounded
  entry-tag chip treatment
- regression coverage asserting publication date and reading-time text remain
  unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
page and episode routes to verify:

- tags render as explicit chip-like links inside entry metadata
- publication date and reading-time text remain unchanged
- tag routes still resolve to the current topic pages
- output remains fully static and deterministic

## Done Criteria

- page and episode entry metadata render tag links through explicit chip hooks
- current metadata facts and topic routes remain unchanged
- deterministic tests cover the bounded entry-tag refinement without widening
  into broader article-header work
