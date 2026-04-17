# Impact Analysis

## Summary

The next slice should replace repeated route-discovery fragments with one
bounded shared discovery surface for generated pages.

Current observed gap:

- recent slices restored discovery links across many routes
- that behavior now lives in repeated hard-coded HTML fragments inside
  multiple page builders
- the publication therefore risks copy drift and inconsistent discovery
  structure even when the route set itself is stable

## Impacted Areas

- page rendering in `src/app/application/use_cases/build_site.py`
- deterministic HTML structure for route-level discovery guidance
- unit and integration coverage for representative route families

## Boundary Change

The build gains no new route or artifact. The boundary change is limited to how
existing discovery guidance is rendered across generated pages.

## Risks

- the slice could drift into a broader page-layout redesign instead of staying
  focused on shared discovery rendering
- over-unifying the discovery surface could erase useful route-specific
  destination differences
- tests could become brittle if they assert incidental prose instead of stable
  structural behavior and destination sets

## Follow-On Pressure

- a later slice may decide whether discovery surfaces should become authored
  content rather than builder-defined publication chrome
- release review should verify that shared rendering reduces drift without
  flattening the different jobs of archives, search, library, and narrative
  routes
