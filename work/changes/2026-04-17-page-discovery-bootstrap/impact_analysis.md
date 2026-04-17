# Impact Analysis

## Summary

The next slice should update standalone pages so their discovery guidance
matches the now-expanded static publication surface.

Current observed gap:

- standalone pages still act only as isolated reading surfaces plus tag links
- `/archives/` and `/search/` now exist as stable reader-facing routes
- standalone pages therefore understate the actual ways readers can move
  through the publication

## Impacted Areas

- standalone-page HTML generation
- deterministic page discovery copy and links
- integration coverage for route discoverability on standalone pages

## Boundary Change

The build gains no new route or data projection. The boundary change is limited
to the discovery copy and outbound links rendered on standalone page routes.

## Risks

- scope could drift into a broader page-template redesign instead of a bounded
  discovery update
- page copy could become repetitive with shared navigation if the slice
  overstates route lists
- tests could assert overly specific prose instead of the core discoverability
  contract

## Follow-On Pressure

- a later slice may revisit richer page-template behavior once the top-level
  information architecture stabilizes further
- release review should verify that standalone-page guidance stays aligned with
  the current reader-facing route set
