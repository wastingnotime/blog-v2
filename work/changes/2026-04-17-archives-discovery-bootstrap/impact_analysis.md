# Impact Analysis

## Summary

The next slice should update the archive page so its discovery guidance matches
the now-expanded static publication surface.

Current observed gap:

- the archive page still acts only as a chronological listing surface
- `/search/` and `/library/` now exist as stable reader-facing routes
- the archive page therefore understates the actual ways readers can move
  through the publication

## Impacted Areas

- archive-page HTML generation
- deterministic archive discovery copy and links
- integration coverage for route discoverability on `/archives/`

## Boundary Change

The build gains no new route or data projection. The boundary change is limited
to the discovery copy and outbound links rendered on `archives/index.html`.

## Risks

- scope could drift into a broader archive redesign instead of a bounded
  discovery update
- archive copy could become repetitive with shared navigation if the slice
  overstates route lists
- tests could assert overly specific prose instead of the core discoverability
  contract

## Follow-On Pressure

- a later slice may revisit richer archive behavior once the top-level
  information architecture stabilizes further
- release review should verify that archive-page guidance stays aligned with the
  current reader-facing route set
