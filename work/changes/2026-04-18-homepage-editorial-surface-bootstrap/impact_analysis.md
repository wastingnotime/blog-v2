# Impact Analysis

## Summary

The next coherent slice is to recover the homepage's concise editorial voice
now that the shared shell has been restored.

Current observed gap:

- the site-wide shell now feels continuous with `../blog`
- the homepage content still reads like explanatory bootstrap copy
- the predecessor's homepage signal is strongest in tone and section labeling,
  not in a large layout system

## Impacted Areas

- homepage copy and section-label markup in
  `src/app/application/use_cases/build_site.py`
- deterministic homepage output assertions in unit and integration tests

## Boundary Change

The build gains no new route, layout system, or data source. The change is
limited to the homepage surface:

- homepage summary and opening copy shift toward concise editorial framing
- homepage section labels move to compact uppercase-style presentation
- recent-entry and saga-summary data remain the same

## Risks

- scope could drift into broader homepage layout redesign or list-item restyling
- copy changes could accidentally overfit to exact old text rather than the
  stable tone and presentation signal
- tests could become brittle if they assert too much incidental wording

## Follow-On Pressure

- later slices may decide whether recent-item and saga-summary formatting should
  also move closer to the predecessor presentation
- release review should verify that the homepage now feels like the same
  publication without forcing full template parity
