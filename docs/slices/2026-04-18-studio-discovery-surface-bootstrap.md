# Slice: 2026-04-18 Studio Discovery Surface Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded studio-surface refinement for the existing section hub:

- keep the current static builder, `/studio/` route, and authored studio copy
- preserve the existing four discovery destinations already exposed by the page
- change only the reader-facing presentation of the studio page's discovery
  surface so it reads like a publication-facing hub rather than a fallback link
  block

## Discovery Scope

The homepage, library, topic pages, sagas hub, and archive now have explicit
editorial presentation treatment, but the studio hub still depends entirely on
the shared generic discovery block:

- `/studio/` already has the correct route and authored section copy
- the page already points to sagas, library, archives, and search
- the current discovery surface therefore works functionally, but it does not
  yet read like an intentional studio navigation surface

This slice restores the minimum studio continuity needed for the current
publication:

- render the existing studio destinations through an explicit studio row shell
- keep the same four discovery routes and labels
- preserve the current authored studio intro and page metadata

This slice does not attempt new studio routes, curated featured work, contact
information, or redesign of the shared discovery surface used elsewhere.

## Use-Case Contract

### `RenderStudioDiscoverySurface`

Given the existing studio destinations, render deterministic studio markup such
that:

- each destination appears as one clear navigation row with label and path
- the current labels and destination routes remain unchanged
- the rows read as part of the studio page rather than a generic fallback
  surface

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- `/studio/` reflects the bounded discovery-surface refinement
- authored studio copy, route, and discovery destinations remain unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- The studio page should read like a deliberate navigation surface for the
  publication's work, not a generic fallback block.
- The slice stays bounded to the studio page and must not silently redesign the
  shared discovery surface used elsewhere.
- Existing destination labels and routes remain the source of truth.
- The row shell should remain studio-only and not affect the shared discovery
  surface.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- studio-page renderer in `src/app/application/use_cases/build_site.py`
- existing authored studio section content
- deterministic unit and integration coverage for generated studio output

## Initial Test Plan

- unit test asserting `/studio/` renders explicit studio-discovery row hooks
- unit test asserting studio discovery rows keep the current labels and routes
- integration test asserting generated `dist/studio/index.html` reflects the
  bounded studio-surface treatment
- integration test asserting shared discovery surfaces on other pages remain
  unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/studio/index.html` to verify:

- studio destinations render as explicit navigation rows
- current destination labels and routes remain unchanged
- authored studio copy and route remain unchanged
- output remains fully static and deterministic

## Done Criteria

- `/studio/` renders its discovery destinations through explicit page-specific
  row presentation
- current studio copy, destination labels, and routes remain unchanged
- deterministic tests cover the bounded studio refinement without widening into
  broader section-hub redesign
