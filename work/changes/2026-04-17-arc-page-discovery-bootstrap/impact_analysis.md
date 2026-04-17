# Impact Analysis

## Summary

The next slice should update arc detail pages so their discovery guidance
matches the now-expanded static publication surface.

Current observed gap:

- arc detail pages still act only as narrative reading surfaces plus episode
  listings
- `/archives/` and `/search/` now exist as stable reader-facing routes
- arc pages therefore understate the actual ways readers can move through the
  publication

## Impacted Areas

- arc-page HTML generation
- deterministic arc discovery copy and links
- integration coverage for route discoverability on arc detail pages

## Boundary Change

The build gains no new route or data projection. The boundary change is limited
to the discovery copy and outbound links rendered on arc detail page routes.

## Risks

- scope could drift into a broader arc-page redesign instead of a bounded
  discovery update
- arc-page copy could become repetitive with shared navigation if the slice
  overstates route lists
- tests could assert overly specific prose instead of the core discoverability
  contract

## Follow-On Pressure

- a later slice may revisit richer arc-page behavior once the top-level
  information architecture stabilizes further
- release review should verify that arc-page guidance stays aligned with the
  current reader-facing route set
