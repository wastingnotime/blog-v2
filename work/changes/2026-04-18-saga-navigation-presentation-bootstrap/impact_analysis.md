# Impact Analysis

## Summary

The next coherent slice is to give saga and arc navigation rows an explicit
presentation contract so the publication's narrative routes feel consistent
with the already refined homepage, archive, search, library, and discovery
surfaces.

Current observed gap:

- saga and arc routes already have the right content and route structure
- their internal navigation lists still render through plain generic rows
- the publication therefore feels less intentional exactly where readers move
  between arcs and episodes

## Impacted Areas

- generated saga-page markup in `src/app/application/use_cases/build_site.py`
- generated arc-page markup in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded saga-navigation treatment
- deterministic saga and arc assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or content model. The boundary change is
limited to presentation on saga and arc routes:

- arc rows get explicit primary-label and supporting-meta row shells
- timeline rows get explicit primary-label and supporting-meta row shells
- arc episode rows get explicit primary-label and supporting-meta row shells
- chronology, counts, labels, and discovery links remain unchanged

## Risks

- scope could drift into changing saga ordering or information architecture
  instead of staying on presentation
- shared CSS hooks could accidentally affect non-saga surfaces if selectors are
  not kept bounded
- tests could overfit incidental markup text instead of meaningful row
  contracts

## Follow-On Pressure

- later slices may decide whether saga routes need richer summaries or adjacent
  navigation after the row contracts are explicit
- release review should verify that internal saga movement now feels coherent
  with the rest of the publication
