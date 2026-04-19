# Slice: 2026-04-18 Shared Discovery Surface Presentation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded shared-component refinement for the generic discovery surface:

- keep the current static builder, existing destination labels, and route usage
- preserve the same pages that currently use the shared discovery helper
- change only the shared helper's reader-facing presentation so generic
  discovery sections read like intentional navigation rows rather than fallback
  prose lines

## Discovery Scope

Most major publication surfaces now have explicit presentation treatment:

- homepage uses explicit row treatment
- library, topic pages, sagas hub, and archive now use explicit row or chip
  treatment
- studio now uses a dedicated page-specific discovery surface

What still lags is the shared helper used by multiple remaining routes:

- content pages, episodes, saga pages, arc pages, library index, search page,
  and similar routes still render `Other ways in` through plain paragraph lines
- the helper is still functionally correct, but visually weaker than the rest
  of the refined publication surfaces

This slice restores the minimum shared-surface continuity needed now:

- render the shared discovery destinations through explicit shared row markup
- keep the current labels, routes, and call sites unchanged
- leave the studio-specific discovery surface untouched

This slice does not attempt to merge studio back into the shared helper,
rewrite page-specific discovery choices, or redesign all supporting surfaces.

## Use-Case Contract

### `RenderSharedDiscoverySurface`

Given the existing shared discovery destinations for a route, render
deterministic discovery markup such that:

- each destination appears as one clear navigation row
- labels and destination routes remain unchanged
- the section reads like a shared publication navigation surface rather than a
  fallback text block

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- pages using the shared helper reflect the bounded row-presentation refinement
- current route-specific destination choices remain unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- The shared discovery surface should read like a reusable publication
  navigation component, not a generic fallback.
- The slice stays bounded to the shared helper and must not silently redesign
  the studio-specific discovery surface.
- Existing labels, routes, and call sites remain the source of truth.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- shared discovery helper in `src/app/application/use_cases/build_site.py`
- existing call sites that already pass route-specific destinations
- deterministic unit and integration coverage for generated discovery sections

## Initial Test Plan

- unit test asserting pages that use the shared helper render explicit shared
  discovery row hooks
- unit test asserting shared discovery rows keep the current labels and routes
- integration test asserting generated pages that use the helper reflect the
  bounded row treatment
- integration test asserting the studio-specific discovery surface remains
  unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect representative
generated pages to verify:

- shared discovery sections render through explicit row markup
- current route-specific labels and routes remain unchanged
- the studio page keeps its dedicated `In the studio` surface
- output remains fully static and deterministic

## Done Criteria

- shared discovery sections render through explicit reusable row presentation
- current labels, routes, and page-specific destination choices remain
  unchanged
- deterministic tests cover the bounded shared-surface refinement without
  widening into a broader navigation redesign
