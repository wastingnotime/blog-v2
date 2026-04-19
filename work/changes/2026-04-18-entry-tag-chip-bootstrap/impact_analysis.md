# Impact Analysis

## Summary

The next coherent slice is to give long-form entry metadata an explicit
tag-chip presentation so page and episode headers reuse the publication's
outlined topic language instead of plain inline tag links.

Current observed gap:

- `/library/` already renders topics as explicit chips
- page and episode routes still render metadata tags as plain inline links
- the extracted predecessor style signals call out outlined topic chips or
  pills as a stable part of the publication's visual language

## Impacted Areas

- entry-metadata markup in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded entry-tag chip treatment
- deterministic page and episode assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or metadata fact. The boundary change is
limited to tag presentation inside existing entry metadata:

- page and episode metadata get one explicit tag-chip markup contract
- publication date, reading time, tag labels, and destination routes remain
  unchanged
- library pages and other discovery surfaces remain unchanged

## Risks

- scope could drift into broader article-header redesign instead of staying on
  tag presentation
- styling could accidentally affect library chips or unrelated links if the
  selectors are not kept bounded
- tests could overfit incidental HTML formatting instead of meaningful chip
  behavior

## Follow-On Pressure

- later slices may decide whether article headers need further editorial
  tightening beyond tags
- release review should verify that long-form pages now feel more consistent
  with the library topic language without changing metadata behavior
