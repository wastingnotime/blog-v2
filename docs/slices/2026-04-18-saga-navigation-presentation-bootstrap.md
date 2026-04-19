# Slice: 2026-04-18 Saga Navigation Presentation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded presentation refinement for existing saga and arc route navigation:

- keep the current static builder, saga routes, arc routes, and content model
- preserve the existing saga body, arc body, chronology, and discovery behavior
- change only the reader-facing presentation hooks used for arc, timeline, and
  episode navigation rows

## Discovery Scope

Recent slices refined the homepage, archives, search, library, topic, 404, and
  discovery surfaces so the publication reads through explicit row contracts.
The saga routes still have one visible gap:

- saga arc lists still render as plain generic list rows
- saga timeline entries still render through unstyled inline links and metadata
- arc episode lists still render as plain generic rows

This leaves the core narrative navigation inside sagas weaker than the rest of
the publication.

This slice restores the minimum continuity needed for the current publication:

- render saga arcs through explicit navigation-row hooks
- render saga timeline entries through explicit navigation-row hooks
- render arc episode rows through explicit navigation-row hooks
- preserve the current routes, labels, dates, counts, and discovery links

This slice does not attempt to change saga sequencing, introduce new metadata,
or redesign the information architecture of sagas.

## Use-Case Contract

### `RenderSagaNavigation`

Given the existing saga and arc views, render deterministic navigation markup
such that:

- each arc row has one clear primary label and one supporting status line
- each timeline row has one clear primary episode line and one supporting
  chronology line
- each arc episode row has one clear primary episode line and one supporting
  date line

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- saga and arc routes reflect the bounded navigation-presentation refinement
- current route structure, chronology, and discovery behavior remain unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- Saga and arc navigation should feel coherent with the refined editorial
  surfaces already present on the rest of the site.
- The slice stays bounded to presentation and must not widen into narrative or
  chronology rule changes.
- Existing saga, arc, and episode data remain the source of truth.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- saga and arc page renderers in `src/app/application/use_cases/build_site.py`
- saga navigation helper renderers used by those routes
- deterministic unit and integration coverage for generated saga and arc output

## Initial Test Plan

- unit test asserting generated saga markup includes explicit arc and timeline
  presentation hooks
- unit test asserting generated arc markup includes explicit episode-row
  presentation hooks
- integration test asserting generated `dist/` saga and arc routes reflect the
  bounded row treatment
- integration test asserting chronology labels, counts, dates, and discovery
  behavior remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
saga and arc routes to verify:

- arcs, timeline entries, and episode rows render through explicit row hooks
- current labels, counts, dates, and routes remain unchanged
- the site stays fully static and deterministic

## Done Criteria

- saga arc rows render through explicit presentation hooks
- saga timeline rows render through explicit presentation hooks
- arc episode rows render through explicit presentation hooks
- current narrative structure and discovery behavior remain unchanged
- deterministic tests cover the bounded navigation-presentation refinement
