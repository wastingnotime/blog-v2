# Impact Analysis

## Summary

The next slice should update the search page so its discovery guidance matches
the now-expanded static publication surface and exposes the discovery block
through a stable shell hook.

Current observed gap:

- the search page still acts only as a client-side search widget surface
- `/archives/` and `/library/` now exist as stable reader-facing routes
- the search page therefore understates the actual ways readers can move
  through the publication
- the discovery block does not yet have its own shell class

## Impacted Areas

- search-page HTML generation
- deterministic search discovery copy and links
- integration coverage for route discoverability on `/search/`

## Boundary Change

The build gains no new route or data projection. The boundary change is limited
to the discovery copy and outbound links rendered on `search/index.html`.

## Risks

- scope could drift into a broader search redesign instead of a bounded
  discovery update
- search copy could become repetitive with shared navigation if the slice
  overstates route lists
- tests could assert overly specific prose instead of the core discoverability
  contract

## Follow-On Pressure

- a later slice may revisit richer search-page behavior once the top-level
  information architecture stabilizes further
- release review should verify that search-page guidance stays aligned with the
  current reader-facing route set
