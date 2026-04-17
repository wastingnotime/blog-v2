# Impact Analysis

## Summary

The next slice should make the existing RSS output discoverable by exposing
`feed.xml` through the shared site chrome on generated HTML pages.

## Impacted Areas

- shared navigation and site-frame rendering
- HTML output across homepage, section pages, pages, and narrative routes
- integration coverage for shared chrome behavior
- publication discoverability of the existing feed artifact

## Boundary Change

The build does not gain a new artifact. Instead, the shared HTML frame expands
to expose one more publication link pointing at the already-generated
`feed.xml`.

## Risks

- the shared chrome could accidentally disturb current active-state rendering
- inconsistent feed link rendering across route types could weaken the benefit
- scope could drift into broader footer or subscription redesign work

## Follow-On Pressure

- a later slice may add dedicated subscription affordances beyond RSS
- a later release review should compare feed discoverability against the older
  site surface
