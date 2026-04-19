# Slice: 2026-04-18 Shared Breadcrumb Presentation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded presentation refinement for existing breadcrumb navigation outside
episode pages:

- keep the current static builder, topic routes, and arc routes
- preserve the existing breadcrumb destinations and route structure
- change only the reader-facing presentation hooks for arc and topic
  breadcrumbs

## Discovery Scope

Episode pages already render breadcrumbs through explicit crumb hooks. Two
reader-facing routes still lag behind:

- arc pages render the parent saga breadcrumb as a plain inline link
- topic pages render the library breadcrumb as a plain inline link
- this leaves breadcrumb treatment inconsistent across the publication

This slice restores the minimum continuity needed for the current publication:

- render arc breadcrumbs through the same explicit breadcrumb hooks already used
  on episode pages
- render topic breadcrumbs through the same explicit breadcrumb hooks
- preserve current destinations, labels, and route behavior

This slice does not attempt to change breadcrumb depth, add new destinations,
or redesign route structure.

## Use-Case Contract

### `RenderBreadcrumbs`

Given existing arc and topic routes, render deterministic breadcrumb markup
such that:

- breadcrumb links use one explicit shared presentation contract
- existing breadcrumb destinations and labels remain unchanged
- routes without multi-step breadcrumbs do not invent extra path segments

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- arc and topic routes reflect the bounded breadcrumb-presentation refinement
- current route structure and discovery behavior remain unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- Breadcrumb treatment should be coherent across routes that already expose path
  navigation.
- The slice stays bounded to presentation and must not widen into route or
  hierarchy changes.
- Existing breadcrumb destinations remain the source of truth.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- arc and topic page renderers in `src/app/application/use_cases/build_site.py`
- shared breadcrumb styling already present in the document shell
- deterministic unit and integration coverage for generated arc and topic
  output

## Initial Test Plan

- unit test asserting arc and topic routes include explicit breadcrumb hooks
- integration test asserting generated `dist/` arc and topic routes reflect the
  bounded breadcrumb treatment
- regression coverage asserting breadcrumb labels and destinations remain
  unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
arc and topic routes to verify:

- breadcrumbs render through explicit crumb hooks
- current breadcrumb destinations remain unchanged
- the site stays fully static and deterministic

## Done Criteria

- arc breadcrumbs render through explicit breadcrumb hooks
- topic breadcrumbs render through explicit breadcrumb hooks
- current route structure and discovery behavior remain unchanged
- deterministic tests cover the bounded breadcrumb-presentation refinement
