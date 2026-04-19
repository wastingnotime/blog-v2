# Impact Analysis

## Summary

The studio hub now reflects the expanded static publication surface.

Current observed contract:

- the studio page guides readers toward sagas, topics, chronology, and search
- `/archives/` and `/search/` appear alongside the existing hub destinations
- the studio hub matches the actual reader-facing routes now available in the
  publication

## Impacted Areas

- studio-page HTML generation
- deterministic studio discovery copy and links
- integration coverage for route discoverability on `/studio/`

## Boundary Change

The build already exposes the relevant routes. The boundary stays limited to
the discovery copy and outbound links rendered on `studio/index.html`.

## Risks

- scope could drift into a broader studio redesign instead of the bounded
  discovery surface
- studio copy could become repetitive with shared navigation if it overstates
  the route list
- tests could assert overly specific prose instead of the discoverability
  contract that matters

## Follow-On Pressure

- a later slice may revisit richer studio composition once the top-level
  information architecture changes again
- release review should verify that studio guidance stays aligned with the
  current reader-facing route set
