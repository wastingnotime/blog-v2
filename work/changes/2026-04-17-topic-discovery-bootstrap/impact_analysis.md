# Impact Analysis

## Summary

Topic pages now match the expanded static publication surface.

Current observed contract:

- topic pages guide readers toward archives and search
- `/archives/` and `/search/` appear as stable reader-facing routes
- the topic pages reflect the actual ways readers can move through the
  publication

## Impacted Areas

- topic-page HTML generation
- deterministic topic discovery copy and links
- integration coverage for route discoverability on `/library/<tag>/`

## Boundary Change

The build already exposes the required routes. The boundary stays limited to
the discovery copy and outbound links rendered on topic pages.

## Risks

- scope could drift into a broader topic-page redesign instead of the bounded
  discovery surface
- topic-page copy could become repetitive with shared navigation if it
  overstates the route list
- tests could assert overly specific prose instead of the discoverability
  contract that matters

## Follow-On Pressure

- a later slice may revisit richer topic-page composition once the top-level
  information architecture changes again
- release review should verify that topic-page guidance stays aligned with the
  current reader-facing route set
