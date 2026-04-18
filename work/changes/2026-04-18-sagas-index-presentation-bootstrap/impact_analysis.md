# Impact Analysis

## Summary

The next coherent slice is to give the sagas section hub an explicit row
presentation so active sagas read like editorial navigation rather than plain
generic list items.

Current observed gap:

- `/sagas/` already links to the right saga and start-reading destinations
- the hub still renders active sagas through plain list rows
- recent homepage, library, and topic-page refinements make the sagas hub the
  next obvious lagging surface

## Impacted Areas

- sagas-index markup in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded saga-row treatment
- deterministic sagas-index assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or saga data. The boundary change is
limited to `/sagas/` row presentation:

- the sagas hub gets one explicit saga-row markup contract
- saga ordering, routes, and start-reading links remain unchanged
- homepage and individual saga pages remain unchanged

## Risks

- scope could drift into saga metadata redesign or section-hub redesign instead
  of staying on row presentation
- styling could accidentally affect non-sagas rows if selectors are not kept
  bounded
- tests could overfit incidental HTML formatting instead of meaningful row
  behavior

## Follow-On Pressure

- later slices may decide whether `studio` or `archives` need similarly compact
  row treatment
- release review should verify that the sagas hub now feels consistent with the
  refined publication surfaces without changing saga behavior
