# Impact Analysis

## Summary

The next slice should update topic pages so their discovery guidance matches
the now-expanded static publication surface.

Current observed gap:

- topic pages still act only as isolated entry listings
- `/archives/` and `/search/` now exist as stable reader-facing routes
- topic pages therefore understate the actual ways readers can move through the
  publication

## Impacted Areas

- topic-page HTML generation
- deterministic topic discovery copy and links
- integration coverage for route discoverability on `/library/<tag>/`

## Boundary Change

The build gains no new route or data projection. The boundary change is limited
to the discovery copy and outbound links rendered on topic pages.

## Risks

- scope could drift into a broader topic-page redesign instead of a bounded
  discovery update
- topic-page copy could become repetitive with shared navigation if the slice
  overstates route lists
- tests could assert overly specific prose instead of the core discoverability
  contract

## Follow-On Pressure

- a later slice may revisit richer topic-page composition once the top-level
  information architecture stabilizes further
- release review should verify that topic-page guidance stays aligned with the
  current reader-facing route set
