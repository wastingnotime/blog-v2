# Impact Analysis

## Summary

The next coherent slice is to tighten homepage recent-entry and saga-summary
presentation so the root route keeps its current data but reads with a more
compact editorial rhythm.

Current observed gap:

- the homepage shell and framing are now aligned with the predecessor
- recent-entry and saga-summary rows still render as plain generic list content
- the predecessor's homepage signal is stronger in row rhythm and secondary
  text treatment than in a larger layout system

## Impacted Areas

- homepage-specific list markup in `src/app/application/use_cases/build_site.py`
- homepage-specific embedded CSS in the shared document renderer
- deterministic homepage assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or data source. The boundary change is
limited to homepage row presentation:

- recent entries gain explicit homepage list hooks for title, metadata, and
  summary
- saga summaries gain explicit homepage list hooks and compact inline status
- archive, topic, and section list rendering stays unchanged

## Risks

- scope could drift into broader homepage redesign instead of staying on row
  presentation
- styling hooks could accidentally leak into non-homepage list surfaces if they
  are not kept local to homepage markup
- tests could overfit incidental whitespace instead of meaningful presentation
  contracts

## Follow-On Pressure

- later slices may decide whether homepage section spacing or library row
  treatment should move closer to the predecessor
- release review should verify that the homepage now feels more editorially
  compact without changing facts or routes
