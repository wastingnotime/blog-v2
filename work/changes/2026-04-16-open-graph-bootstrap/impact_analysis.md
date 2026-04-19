# Impact Analysis

## Summary

This slice formalizes the bounded Open Graph metadata already carried by the
shared document head so generated HTML pages expose deterministic social unfurl
metadata without introducing images or broader social-media features.

Current observed contract:

- generated HTML includes canonical, RSS, identity-asset, and bounded `og:*`
  metadata
- the builder derives Open Graph values from existing page metadata and
  canonical URLs

## Impacted Areas

- shared document-head rendering in the static HTML builder
- deterministic projection of per-page social metadata
- integration coverage for head metadata across representative routes

## Boundary Change

The build does not gain new routes or artifacts. Instead, generated HTML pages
carry a small set of additional head meta tags derived from existing titles,
descriptions, and canonical URLs. To keep the slice deterministic, `og:type`
remains the single literal value `website` for all routes in this bootstrap.

## Risks

- Open Graph values could drift from canonical page metadata if not derived from
  the same inputs
- adding route-specific social-type semantics now would create avoidable model
  invention pressure before the repository has explicit unfurl requirements
- scope could drift into broader SEO or social-preview image work
- additional head markup could disturb existing HTML assertions

## Follow-On Pressure

- a later slice may add social preview image support or Twitter card metadata
- release review should compare the new social metadata against actual unfurl
  needs once the bounded text-and-URL version exists
