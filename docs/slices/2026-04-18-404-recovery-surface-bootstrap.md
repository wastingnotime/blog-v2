# Slice: 2026-04-18 404 Recovery Surface Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded recovery-surface refinement for the static 404 page:

- keep the current static builder, `404.html` route, and existing recovery
  destinations
- preserve the page's noindex contract and current recovery labels
- change only the reader-facing presentation of the recovery options so the
  404 page reads like the rest of the refined navigation surfaces

## Discovery Scope

Most publication-facing navigation surfaces now have explicit row or chip
presentation, but the static 404 page still uses a plain unordered recovery
list:

- `404.html` already exposes the correct recovery destinations
- the page already explains that the route may have moved during the rebuild
- the page therefore works functionally, but its recovery options still read as
  a generic list rather than an intentional recovery surface

This slice restores the minimum 404 continuity needed for the current
publication:

- render recovery destinations through an explicit 404-specific row shell
- keep the same recovery labels and destination routes
- preserve the page's current copy, route, and robots contract

This slice does not attempt search suggestions, redirect logic, personalized
recovery, or broader error-page redesign.

## Use-Case Contract

### `RenderNotFoundRecoverySurface`

Given the existing recovery destinations for the static 404 page, render
deterministic markup such that:

- each destination appears as one clear recovery row with label and path
- current labels and routes remain unchanged
- the recovery surface reads like a purposeful navigation aid rather than a
  plain fallback list

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- `404.html` reflects the bounded recovery-surface refinement
- current recovery labels, routes, and noindex behavior remain unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- The 404 page should help readers recover through a clear navigation surface,
  not a generic list.
- The slice stays bounded to 404 recovery presentation and must not widen into
  redirect or search-product behavior.
- Existing recovery labels, routes, and robots rules remain the source of
  truth.
- The row shell should remain 404-only and not affect the other navigation
  surfaces.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- 404-page renderer in `src/app/application/use_cases/build_site.py`
- existing static recovery destinations already defined in the page
- deterministic unit and integration coverage for generated 404 output

## Initial Test Plan

- unit test asserting `404.html` renders explicit recovery-row hooks
- unit test asserting recovery rows keep the current labels and routes
- integration test asserting generated `404.html` reflects the bounded recovery
  treatment
- integration test asserting the page remains `noindex,follow`

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect `dist/404.html`
to verify:

- recovery destinations render as explicit navigation rows
- current labels and routes remain unchanged
- noindex behavior remains intact
- output remains fully static and deterministic

## Done Criteria

- `404.html` renders recovery destinations through explicit row presentation
- current labels, routes, and robots behavior remain unchanged
- deterministic tests cover the bounded recovery refinement without widening
  into broader error handling work
