# Impact Analysis

## Summary

The next slice should update saga detail pages so their discovery guidance
matches the now-expanded static publication surface and exposes the discovery
block through a stable shell hook.

Current observed gap:

- saga detail pages still act only as narrative reading surfaces plus arc and
  timeline structure
- `/archives/` and `/search/` now exist as stable reader-facing routes
- saga pages therefore understate the actual ways readers can move through the
  publication
- the discovery block does not yet have its own shell class

## Impacted Areas

- saga-page HTML generation
- deterministic saga discovery copy and links
- integration coverage for route discoverability on saga detail pages

## Boundary Change

The build gains no new route or data projection. The boundary change is limited
to the discovery copy and outbound links rendered on saga detail page routes.

## Risks

- scope could drift into a broader saga-page redesign instead of a bounded
  discovery update
- saga-page copy could become repetitive with shared navigation if the slice
  overstates route lists
- tests could assert overly specific prose instead of the core discoverability
  contract

## Follow-On Pressure

- a later slice may revisit richer saga-page behavior once the top-level
  information architecture stabilizes further
- release review should verify that saga-page guidance stays aligned with the
  current reader-facing route set
