# Impact Analysis

## Summary

The next slice should expose the new `/search/` route through the shared site
chrome so readers can discover and reach the search surface without direct URL
knowledge.

Current observed gap:

- `/search/` now exists as a generated route
- the shared navigation model still omits Search entirely

## Impacted Areas

- navigation-state projection for top-level routes
- shared navigation rendering across generated pages
- integration coverage for route discoverability and active-state behavior

## Boundary Change

The build does not gain a new content family or machine-readable artifact.
Instead, the shared chrome gains one additional top-level navigation affordance:
`Search`.

## Risks

- active-state logic could regress for existing routes if Search is inserted
  carelessly
- scope could drift into broader navigation redesign instead of a bounded link
  addition
- `/search/` could remain discoverable only in some page types if chrome
  rendering is not truly shared

## Follow-On Pressure

- a later slice may revisit broader information architecture once more top-level
  routes are stabilized
- release review should verify that search, archives, library, and saga routes
  remain complementary instead of competing in the shared chrome
