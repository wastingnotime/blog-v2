# Slice: 2026-04-18 Homepage Editorial Surface Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded homepage-surface refinement on top of the restored shared editorial
shell:

- keep the current static builder, routes, and shared dark shell
- preserve homepage data sources and list semantics
- recover the predecessor's concise homepage tone and compact section labeling
  without redesigning the broader information architecture

## Discovery Scope

The shared renderer now matches the predecessor's dark editorial atmosphere,
but the homepage surface still carries generic bootstrap phrasing:

- the current homepage summary and opening section read like explanatory starter
  copy rather than the original publication voice
- homepage section headings still use mixed-case labels instead of the compact
  editorial labeling seen in `../blog`
- the old homepage signal is specific and bounded: short intro copy plus terse
  section presentation for `RECENT` and `SAGAS`

This slice restores the minimum homepage-specific continuity needed after the
shared shell recovery:

- align homepage summary and opening copy with the predecessor's concise
  editorial tone
- shift homepage section labels toward the compact uppercase style signaled by
  the original repo through one explicit homepage label treatment rather than
  relying only on heading text content
- keep the existing recent entries, saga summaries, and library link structure
  intact

This slice does not attempt homepage layout restructuring, item-card redesign,
new homepage sections, or full parity with the old template.

## Use-Case Contract

### `RenderHomepageEditorialSurface`

Given the current homepage data, render deterministic homepage markup such
that:

- the top-of-page summary and opening copy read as concise publication framing
  rather than generic explanatory text
- the homepage opening surface stays bounded to:
  - one concise framing sentence
  - one short wayfinding line that still links to the current search, archive,
    and library routes
- homepage section labels use compact editorial presentation through explicit
  homepage markup and styling
- the underlying recent-entry and saga-summary data remain unchanged

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- the homepage surface reflects the extracted predecessor tone
- homepage routing, structured data, and shared shell remain intact
- no new runtime dependency or route is introduced

## Main Business Rules

- The homepage should feel like the front page of the same publication, not a
  generic starter scaffold.
- Tone recovery should happen through concise copy and section presentation, not
  through layout expansion.
- The slice should preserve the existing homepage heading, route, and data
  projections while tightening only the reader-facing framing around them.
- The slice must stay bounded to homepage editorial surface and must not widen
  into broader discovery-model or content-structure changes.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- homepage renderer in `src/app/application/use_cases/build_site.py`
- existing homepage recent-entry and saga-summary renderers
- deterministic unit and integration coverage for generated homepage output

## Initial Test Plan

- unit test asserting homepage summary and opening copy reflect the refined
  editorial tone
- unit test asserting homepage section labels use the bounded compact
  presentation
- integration test asserting generated `dist/index.html` reflects the restored
  homepage tone while preserving the same route and content data
- integration test asserting the homepage remains static-only and structurally
  compatible with the current builder

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect `dist/index.html`
to verify:

- the homepage summary reads with the concise predecessor tone
- the homepage opening surface is shorter and more editorial than the earlier
  bootstrap copy while still linking to current discovery routes
- section labels present as compact editorial markers through explicit homepage
  styling
- recent entries, saga summaries, and library navigation remain intact

## Done Criteria

- homepage summary and opening copy reflect the predecessor's concise editorial
  framing
- homepage section labels shift to compact editorial presentation
- current homepage data and route behavior remain unchanged
- deterministic tests cover the bounded homepage-surface recovery without
  widening into a redesign
