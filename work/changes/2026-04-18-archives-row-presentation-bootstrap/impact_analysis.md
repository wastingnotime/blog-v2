# Impact Analysis

## Summary

The next coherent slice is to give the chronological archive an explicit
entry-row presentation so `/archives/` reads like an editorial index rather
than a generic list.

Current observed gap:

- `/archives/` already has the right chronology and routes
- the archive still renders entries through plain list rows
- recent refinements across homepage, topic pages, and section hubs make the
  archive the next obvious lagging navigation surface

## Impacted Areas

- archive-page markup in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded archive-row treatment
- deterministic archive assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or archive data. The boundary change is
limited to `/archives/` row presentation:

- the archive gets one explicit archive-row markup contract
- chronology, routes, and supporting context remain unchanged
- other list surfaces remain unchanged

## Risks

- scope could drift into archive grouping or archive-product redesign instead
  of staying on row presentation
- styling could accidentally affect non-archive rows if selectors are not kept
  bounded
- tests could overfit incidental HTML formatting instead of meaningful row
  behavior

## Follow-On Pressure

- later slices may decide whether `studio` needs a stronger publication-facing
  surface beyond shared discovery links
- release review should verify that the archive now feels consistent with the
  refined publication surfaces without changing chronology
