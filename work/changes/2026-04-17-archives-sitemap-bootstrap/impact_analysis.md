# Impact Analysis

## Summary

The next slice should close a route-inventory gap in the generated sitemap by
including the durable `/archives/` route in `sitemap.xml`.

Current observed gap:

- `/archives/` is now a first-class reader-facing route in navigation and page
  discovery surfaces
- `project_publication_metadata(...)` still omits `/archives/` from sitemap
  projection
- generated `sitemap.xml` therefore understates the current static publication
  surface

## Impacted Areas

- sitemap metadata projection in
  `src/app/application/use_cases/project_publication_metadata.py`
- deterministic sitemap assertions in `tests/unit/test_build_site.py`
- scenario-level sitemap assertions in `tests/integration/test_run_scenario.py`

## Boundary Change

The build gains no new route or artifact. The boundary change is limited to one
additional durable route entry inside generated `sitemap.xml`.

## Risks

- scope could drift into a broader crawl-policy redesign instead of staying
  bounded to sitemap completeness
- tests could overfit exact XML ordering rather than the presence and meaning
  of the archive entry
- archive `lastmod` could drift if it stops deriving from the same publication
  chronology already used by archive and feed projections

## Follow-On Pressure

- a later slice may revisit whether any other durable hub routes need distinct
  sitemap treatment once the route inventory stabilizes further
- release review should verify that sitemap projection remains aligned with the
  publication routes the site intentionally wants indexed
