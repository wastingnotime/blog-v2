# Impact Analysis

## Summary

The next slice should expose the existing `/archives/` route through the shared
site chrome so readers can discover and reach the chronological archive without
direct URL knowledge.

Current observed gap:

- `/archives/` already exists as a generated route
- the shared navigation model still omits Archives entirely
- the archive page therefore cannot be reached or marked active through the
  common frame

## Impacted Areas

- navigation-state projection for top-level routes
- shared navigation rendering across generated pages
- integration coverage for archive discoverability and active-state behavior

## Boundary Change

The build does not gain a new content family or machine-readable artifact.
Instead, the shared chrome gains one additional top-level navigation affordance:
`Archives`.

## Risks

- active-state logic could regress for existing routes if Archives is inserted
  carelessly
- scope could drift into broader navigation redesign instead of a bounded link
  addition
- `/archives/` could remain discoverable only in some page types if chrome
  rendering is not truly shared

## Follow-On Pressure

- a later slice may revisit broader information architecture once more
  top-level routes are stabilized
- release review should verify that archives, search, library, and saga routes
  remain complementary instead of competing in the shared chrome
