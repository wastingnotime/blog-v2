# Impact Analysis

## Summary

The next slice should add a bounded structured-data layer so the generated
static publication exposes machine-readable publication semantics alongside the
discovery artifacts it already emits.

Current observed gap:

- the build already renders canonical URLs, feed metadata, sitemap metadata,
  social metadata, and route-specific robots metadata
- no generated route currently emits an `application/ld+json` script
- the repository already has enough stable metadata for a bounded first pass on
  homepage and content-backed routes without inventing new editorial fields

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- existing content metadata projection for pages and episodes
- possible publication-facing metadata view models if the structured-data
  payload should be projected instead of assembled inline
- deterministic unit and integration coverage for structured metadata

## Boundary Change

The static build does not gain new routes, hosting behavior, or runtime
dependencies. Instead, it extends the machine-readable publication contract in
selected existing routes:

- homepage gains a bounded `WebSite` JSON-LD payload
- standalone pages and episodes gain bounded `Article` JSON-LD payloads
- structural and recovery routes stay unchanged

## Risks

- scope could drift into a generalized schema system, breadcrumb generation, or
  route-by-route schema taxonomy instead of staying bounded to the initial
  publication surfaces
- structured-data fields could drift from canonical/meta tag values if the
  slice duplicates data assembly in too many places
- tests could overfit exact JSON field ordering instead of the intended schema
  contract

## Follow-On Pressure

- later slices may decide whether saga, archive, search, or topic routes need
  their own schema types once their publication meaning is more explicit
- release review should verify that canonical tags, social metadata, robots
  metadata, feed/sitemap output, and JSON-LD still present one coherent
  discovery contract
