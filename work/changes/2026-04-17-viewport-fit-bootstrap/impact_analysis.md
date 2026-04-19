# Impact Analysis

## Summary

The generated static publication now exposes the explicit viewport-fit
contract in the shared document head.

Current observed contract:

- generated pages include application-name, color-scheme, referrer,
  theme-color, mobile-web-app, and viewport-fit metadata
- the shared head uses `viewport-fit=cover`
- the publication keeps the viewport contract aligned with the rest of the
  bounded mobile head surface

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- deterministic test coverage for representative head metadata
- regression protection around unchanged application-name, color-scheme,
  referrer, theme-color, mobile-web-app, and social metadata

## Boundary Change

The build already includes the needed viewport literal. The boundary stays
limited to the browser-facing viewport metadata in generated HTML heads.

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
