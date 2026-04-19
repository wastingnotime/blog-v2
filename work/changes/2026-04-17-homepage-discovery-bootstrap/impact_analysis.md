# Impact Analysis

## Summary

The next slice should update the homepage so its editorial discovery guidance
matches the now-expanded static publication surface and exposes the discovery
block through a stable shell hook.

Current observed gap:

- the homepage body still guides readers only toward sagas and library
- `/archives/` and `/search/` now exist as stable reader-facing routes
- the homepage therefore understates the actual ways readers can move through
  the publication
- the discovery block does not yet have its own shell class

## Impacted Areas

- homepage HTML generation
- deterministic homepage discovery copy and links
- integration coverage for route discoverability on the root page

## Boundary Change

The build gains no new route or data projection. The boundary change is limited
to the discovery copy and outbound links rendered on `index.html`.

## Risks

- scope could drift into a broader homepage redesign instead of a bounded
  discovery update
- homepage copy could become repetitive with shared navigation if the slice
  overstates route lists
- tests could assert overly specific prose instead of the core discoverability
  contract

## Follow-On Pressure

- a later slice may revisit richer homepage composition once the top-level
  information architecture stabilizes further
- release review should verify that homepage discovery guidance stays aligned
  with the current reader-facing route set
