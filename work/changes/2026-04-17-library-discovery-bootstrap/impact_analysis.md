# Impact Analysis

## Summary

The next slice should update the library hub so its discovery guidance matches
the now-expanded static publication surface.

Current observed gap:

- the library page still frames itself only as topic browsing
- `/archives/` and `/search/` now exist as stable reader-facing routes
- the library hub therefore understates the actual ways readers can move
  through the publication

## Impacted Areas

- library-page HTML generation
- deterministic library discovery copy and links
- integration coverage for route discoverability on `/library/`

## Boundary Change

The build gains no new route or data projection. The boundary change is limited
to the discovery copy and outbound links rendered on `library/index.html`.

## Risks

- scope could drift into a broader library redesign instead of a bounded
  discovery update
- library copy could become repetitive with shared navigation if the slice
  overstates route lists
- tests could assert overly specific prose instead of the core discoverability
  contract

## Follow-On Pressure

- a later slice may revisit richer library composition once the top-level
  information architecture stabilizes further
- release review should verify that library guidance stays aligned with the
  current reader-facing route set
