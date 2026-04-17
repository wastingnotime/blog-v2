# Impact Analysis

## Summary

The next slice should add bounded Open Graph metadata to the shared document
head so generated HTML pages expose deterministic social unfurl metadata
without introducing images or broader social-media features.

## Impacted Areas

- shared document-head rendering in the static HTML builder
- deterministic projection of per-page social metadata
- integration coverage for head metadata across representative routes

## Boundary Change

The build does not gain new routes or artifacts. Instead, generated HTML pages
gain a small set of additional head meta tags derived from existing titles,
descriptions, and canonical URLs.

## Risks

- Open Graph values could drift from canonical page metadata if not derived from
  the same inputs
- scope could drift into broader SEO or social-preview image work
- additional head markup could disturb existing HTML assertions

## Follow-On Pressure

- a later slice may add social preview image support or Twitter card metadata
- release review should compare the new social metadata against actual unfurl
  needs once the bounded text-and-URL version exists
