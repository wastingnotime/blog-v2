# Slice: 2026-04-18 Episode Navigation Presentation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded presentation refinement for existing episode-local navigation:

- keep the current static builder, episode routes, and arc sequencing
- preserve the existing breadcrumb destinations and previous/next episode logic
- change only the reader-facing presentation hooks for episode-local navigation

## Discovery Scope

Recent slices refined section hubs, search, discovery surfaces, and saga-level
navigation so route movement reads through explicit row contracts. Episode
pages still have one visible gap:

- breadcrumbs render as plain inline links inside a generic navigation shell
- previous and next episode navigation renders as plain links inside the same
  generic shell
- the episode page therefore works functionally, but its local navigation feels
  less deliberate than the rest of the publication

This slice restores the minimum continuity needed for the current publication:

- render episode breadcrumbs through an explicit breadcrumb-row shell
- render previous and next episode navigation through a dedicated adjacent-nav
  shell
- preserve current destinations, labels, numbering, and route behavior

This slice does not attempt to change episode ordering, add new destinations,
or redesign the narrative model.

## Use-Case Contract

### `RenderEpisodeNavigation`

Given the existing episode and arc view, render deterministic local navigation
markup such that:

- breadcrumbs have explicit presentation hooks for the saga and arc path and
  appear in their own compact row
- previous and next episode links render through explicit adjacent-nav hooks
  inside a dedicated nav shell
- empty previous or next slots remain structurally stable without inventing new
  destinations

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- episode routes reflect the bounded navigation-presentation refinement
- current route structure, sequencing, and discovery behavior remain unchanged
- no new runtime dependency or route is introduced

## Main Business Rules

- Episode-local navigation should feel coherent with the refined editorial
  surfaces already present across the publication.
- The slice stays bounded to presentation and must not widen into sequence or
  route logic changes.
- Existing breadcrumb and previous/next episode relationships remain the source
  of truth.
- The breadcrumb row and adjacent-nav shell should remain episode-only and not
  bleed into arc or saga pages.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- episode-page renderer in `src/app/application/use_cases/build_site.py`
- adjacent episode navigation helper used by episode routes
- deterministic unit and integration coverage for generated episode output

## Initial Test Plan

- unit test asserting generated episode markup includes explicit breadcrumb and
  adjacent-navigation hooks
- unit test asserting previous and next episode labels remain unchanged
- integration test asserting generated `dist/` episode routes reflect the
  bounded episode-navigation treatment
- integration test asserting discovery and metadata behavior remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
episode routes to verify:

- breadcrumbs and adjacent episode links render through explicit hooks
- current destinations and episode numbering remain unchanged
- the site stays fully static and deterministic

## Done Criteria

- episode breadcrumbs render through explicit presentation hooks
- previous and next episode navigation render through explicit presentation
  hooks inside an episode-only shell
- current episode sequencing and discovery behavior remain unchanged
- deterministic tests cover the bounded navigation-presentation refinement
