# Impact Analysis

## Summary

The shared site chrome now exposes the `/archives/` route.

Current observed contract:

- `/archives/` is present in the generated navigation model
- the shared navigation renders Archives alongside the other top-level routes
- the archive page can be reached and marked active through the common frame

## Impacted Areas

- navigation-state projection for top-level routes
- shared navigation rendering across generated pages
- integration coverage for archive discoverability and active-state behavior

## Boundary Change

The build already projects the route. The boundary stays limited to the shared
chrome affordance: `Archives`.

## Risks

- active-state logic could regress for existing routes if Archives is inserted
  carelessly
- scope could drift into broader navigation redesign instead of the bounded
  link addition
- `/archives/` could remain discoverable only in some page types if chrome
  rendering is not truly shared

## Follow-On Pressure

- a later slice may revisit broader information architecture once more
  top-level routes are stabilized
- release review should verify that archives, search, library, and saga routes
  remain complementary instead of competing in the shared chrome
