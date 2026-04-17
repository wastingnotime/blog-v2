# Impact Analysis

## Summary

The next slice should update the studio hub so its discovery guidance matches
the now-expanded static publication surface.

Current observed gap:

- the studio page still guides readers only toward sagas and library
- `/archives/` and `/search/` now exist as stable reader-facing routes
- the studio hub therefore understates the actual ways readers can move through
  the publication

## Impacted Areas

- studio-page HTML generation
- deterministic studio discovery copy and links
- integration coverage for route discoverability on `/studio/`

## Boundary Change

The build gains no new route or data projection. The boundary change is limited
to the discovery copy and outbound links rendered on `studio/index.html`.

## Risks

- scope could drift into a broader studio redesign instead of a bounded
  discovery update
- studio copy could become repetitive with shared navigation if the slice
  overstates route lists
- tests could assert overly specific prose instead of the core discoverability
  contract

## Follow-On Pressure

- a later slice may revisit richer studio composition once the top-level
  information architecture stabilizes further
- release review should verify that studio guidance stays aligned with the
  current reader-facing route set
