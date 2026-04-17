# Impact Analysis

## Summary

The next slice should update the sagas hub so its discovery guidance matches
the now-expanded static publication surface.

Current observed gap:

- the sagas page still acts only as an active-saga listing surface
- `/archives/` and `/search/` now exist as stable reader-facing routes
- the sagas hub therefore understates the actual ways readers can move through
  the publication

## Impacted Areas

- sagas-page HTML generation
- deterministic sagas discovery copy and links
- integration coverage for route discoverability on `/sagas/`

## Boundary Change

The build gains no new route or data projection. The boundary change is limited
to the discovery copy and outbound links rendered on `sagas/index.html`.

## Risks

- scope could drift into a broader sagas redesign instead of a bounded
  discovery update
- sagas copy could become repetitive with shared navigation if the slice
  overstates route lists
- tests could assert overly specific prose instead of the core discoverability
  contract

## Follow-On Pressure

- a later slice may revisit richer sagas composition once the top-level
  information architecture stabilizes further
- release review should verify that sagas guidance stays aligned with the
  current reader-facing route set
