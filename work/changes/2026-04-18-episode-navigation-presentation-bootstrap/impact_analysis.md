# Impact Analysis

## Summary

The next coherent slice is to give episode-local navigation an explicit
presentation contract so episode pages feel consistent with the refined
navigation and discovery surfaces already present across the site.

Current observed gap:

- episode pages already have the right breadcrumb destinations and previous/next
  relationships
- those local navigation controls still render through plain inline links
- the publication therefore feels less intentional at the exact point where a
  reader moves within an arc

## Impacted Areas

- generated episode-page markup in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded episode-navigation treatment
- deterministic episode assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or sequence rule. The boundary change is
limited to presentation on episode routes:

- breadcrumb links get explicit crumb hooks
- previous and next episode links get explicit adjacent-nav hooks
- current sequencing, labels, numbering, and discovery links remain unchanged

## Risks

- scope could drift into changing episode ordering or breadcrumb logic instead
  of staying on presentation
- shared CSS hooks could accidentally affect non-episode surfaces if selectors
  are not kept bounded
- tests could overfit exact whitespace instead of meaningful navigation
  contracts

## Follow-On Pressure

- later slices may decide whether episode-local navigation needs richer context
  labels after the explicit hooks exist
- release review should verify that moving through episodes now feels coherent
  with the rest of the publication
