# Impact Analysis

## Summary

The next slice should add machine-readable RSS autodiscovery metadata to the
shared document head so the existing `feed.xml` artifact becomes discoverable
to feed readers without relying on visible navigation alone.

## Impacted Areas

- shared document-head rendering in the static HTML builder
- deterministic projection of feed title and absolute feed URL
- integration coverage for shared page metadata

## Boundary Change

The build does not gain new artifacts or routes. Instead, generated HTML pages
gain one additional deterministic head link pointing at the existing `feed.xml`
artifact.

## Risks

- autodiscovery metadata could drift from the actual feed URL if both are not
  derived from the same settings
- scope could drift into broader SEO or social metadata work
- head markup changes could accidentally disturb existing HTML assertions

## Follow-On Pressure

- a later slice may revisit broader machine-readable metadata such as Open Graph
  or per-section feed variants
- release review should compare feed discoverability through both visible and
  machine-readable surfaces once implemented
