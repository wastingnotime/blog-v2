# Impact Analysis

## Summary

The next coherent slice is to give the library index an explicit topic-chip
presentation so discovered topics read like a navigation surface rather than a
generic list.

Current observed gap:

- `/library/` already discovers topics and links to topic pages correctly
- the page still renders topics as plain list items
- the extracted predecessor style signals include outlined topic chips or pills
  as a recognizable part of the publication's discovery language

## Impacted Areas

- library-index markup in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded topic-chip treatment
- deterministic library-page assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or topic data. The boundary change is
limited to `/library/` topic presentation:

- the library index gets one explicit topic-chip markup contract
- discovered topic ordering and destination routes remain unchanged
- topic pages and other list surfaces remain unchanged

## Risks

- scope could drift into topic counts, summaries, or taxonomy redesign instead
  of staying on chip presentation
- styling could accidentally affect non-library links if the selectors are not
  kept bounded
- tests could overfit incidental HTML formatting instead of meaningful chip
  behavior

## Follow-On Pressure

- later slices may decide whether topic pages themselves need a more editorial
  entry-row treatment
- release review should verify that the library now feels more like a
  publication navigation surface without changing topic behavior
