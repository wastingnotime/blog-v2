# Impact Analysis

## Summary

The next slice should add bounded referrer metadata so the generated static
publication makes one more browser-facing head policy explicit without
expanding into runtime-controlled security infrastructure.

Current observed gap:

- generated pages now include format-detection, theme-color, Apple
  mobile-web-app, Open Graph, and Twitter Card metadata
- the shared head still omits `meta name="referrer"`
- the publication already has a strong deterministic head contract, so the next
  gap is explicit browser metadata rather than a missing route or asset

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- deterministic test coverage for representative head metadata
- regression protection around unchanged theme-color, mobile-web-app, and
  social metadata

## Boundary Change

The build gains no new routes or assets. The boundary change is limited to
additional browser-facing metadata in generated HTML heads.

## Risks

- scope could drift into broader response-header or CDN policy work instead of
  staying bounded to shared metadata
- tests could overfit incidental head ordering rather than the selected policy
  contract
- the referrer literal could be chosen ad hoc instead of staying aligned with
  the current static publication model

## Follow-On Pressure

- a later slice may revisit whether other browser-facing head policies are
  justified
- release review should verify that shared referrer metadata remains consistent
  across representative generated routes
