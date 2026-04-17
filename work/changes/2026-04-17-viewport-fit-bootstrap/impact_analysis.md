# Impact Analysis

## Summary

The next slice should extend the shared viewport metadata so the generated
static publication makes one more small mobile-display contract explicit in the
document head.

Current observed gap:

- generated pages now include application-name, color-scheme, referrer,
  theme-color, and mobile-web-app metadata
- the shared head still uses a minimal viewport literal without
  `viewport-fit=cover`
- the publication already has a bounded mobile-web-app identity surface, so the
  next gap is explicit shared viewport metadata rather than a layout problem

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- deterministic test coverage for representative head metadata
- regression protection around unchanged application-name, color-scheme,
  referrer, theme-color, mobile-web-app, and social metadata

## Boundary Change

The build gains no new routes or assets. The boundary change is limited to an
updated browser-facing viewport literal in generated HTML heads.

## Risks

- scope could drift into safe-area CSS or broader responsive redesign instead of
  staying bounded to shared metadata
- tests could overfit incidental head ordering rather than the selected
  viewport contract
- viewport metadata could drift from the rest of the mobile head contract if it
  stops being treated as one shared deterministic literal

## Follow-On Pressure

- a later slice may revisit whether any safe-area styling changes are justified
- release review should verify that the shared viewport contract remains
  consistent across representative generated routes
