# Slice: 2026-04-18 Homepage List Presentation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded homepage list-presentation refinement on top of the restored editorial
shell and homepage tone:

- keep the current static builder, homepage route, and homepage data sources
- preserve existing recent-entry and saga-summary facts
- tighten only the homepage list markup and styling so recent items and saga
  summaries read closer to the predecessor's compact editorial presentation

## Discovery Scope

The shared shell and homepage framing are now aligned, but the homepage list
surfaces still read more like generic default lists than the predecessor's
editorial front page:

- recent entries still render as plain list items with unscoped metadata and
  paragraph copy
- saga summaries still render as a title followed by separate metadata and
  summary blocks with no homepage-specific presentation contract
- `../blog/templates/home.gohtml` shows a more compact homepage rhythm:
  - recent entries use one primary title line
  - metadata sits in a quieter secondary line
  - summaries remain visibly secondary
  - saga status reads inline with the title rather than as a detached block

This slice restores the minimum homepage-list continuity needed after the
homepage surface refinement:

- give recent-entry rows explicit homepage markup and secondary-text treatment
- give saga-summary rows explicit homepage markup with compact inline status
- keep the same homepage data and navigation links intact

This slice does not attempt homepage layout restructuring, card design,
homepage data changes, new sections, or parity with all old template details.

## Use-Case Contract

### `RenderHomepageRecentEntries`

Given the existing homepage recent-entry projection, render deterministic
homepage markup such that:

- each recent entry has one clear primary title line
- date and optional saga context render as quieter supporting metadata
- summary remains present but visually secondary

### `RenderHomepageSagaSummaries`

Given the existing homepage saga-summary projection, render deterministic
homepage markup such that:

- each saga keeps the same title, status, episode count, and last release data
- status reads inline in a compact homepage-specific presentation
- summary remains present but visually secondary

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- homepage list presentation reflects the extracted predecessor rhythm
- homepage route, structured data, and underlying data stay intact
- no new runtime dependency or route is introduced

## Main Business Rules

- The homepage should feel editorially compact without dropping existing
  homepage facts.
- Presentation changes should remain homepage-specific rather than leaking into
  archive, topic, or section list rendering.
- Recent-entry and saga-summary projections remain the source of truth; only
  homepage markup and styling change here.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- homepage renderer in `src/app/application/use_cases/build_site.py`
- existing homepage recent-entry and saga-summary renderers
- deterministic unit and integration coverage for generated homepage output

## Initial Test Plan

- unit test asserting homepage recent entries render explicit homepage-specific
  metadata and summary hooks
- unit test asserting homepage saga summaries render compact inline status
  presentation without changing the underlying facts
- integration test asserting generated `dist/index.html` reflects the bounded
  homepage list-presentation refinement
- integration test asserting homepage remains static-only and structurally
  compatible with the current builder

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect `dist/index.html`
to verify:

- recent entries render with compact homepage-specific title, metadata, and
  summary treatment
- saga summaries render compact inline status near the title while keeping the
  same factual data
- homepage route and supporting navigation remain unchanged
- output remains fully static and deterministic

## Done Criteria

- homepage recent entries use explicit compact editorial presentation
- homepage saga summaries use explicit compact inline status presentation
- existing homepage data remains intact
- deterministic tests cover the bounded homepage-list refinement without
  widening into a redesign
