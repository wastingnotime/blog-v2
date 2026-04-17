# Impact Analysis

## Summary

The next slice should update `404.html` so the static recovery surface includes
the now-existing `/search/` route.

Current observed gap:

- `/search/` exists as a generated route and shared-navigation destination
- `404.html` still omits Search from its recovery links
- readers hitting a missing route therefore do not see the strongest discovery
  surface added after the original 404 slice

## Impacted Areas

- static `404.html` generation
- deterministic recovery-link rendering
- integration coverage for static not-found recovery behavior

## Boundary Change

The build gains no new route or content family. The boundary change is limited
to the recovery links rendered inside the existing `404.html` artifact.

## Risks

- scope could drift into broader 404 redesign or dynamic search behavior
- recovery-link assertions may become inconsistent if the route list changes in
  only one place
- the slice could under-specify ordering if Search is inserted carelessly

## Follow-On Pressure

- a later slice may revisit richer search-assisted recovery only if the
  repository chooses to add dynamic not-found behavior
- release review should verify that `404.html` stays aligned with the current
  top-level reader-facing routes
