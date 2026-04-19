# Impact Analysis

## Summary

This slice adds bounded Apple mobile-web-app metadata so the generated static
publication completes another small browser-facing identity surface using
inputs it already owns.

Current observed contract:

- generated pages include theme-color, manifest, and identity assets
- the shared head includes `apple-mobile-web-app-*` metadata
- the publication has a stable title, touch icon, and bounded color identity
  that support one deterministic mobile-web-app contract

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- deterministic test coverage for representative head metadata
- regression protection around unchanged theme-color and social metadata

## Boundary Change

The build gains no new routes or assets. The boundary change is limited to
browser-facing metadata already present in generated HTML heads.

## Risks

- scope could drift into broader platform-specific PWA behavior instead of
  staying bounded to shared metadata
- tests could overfit platform-specific assumptions beyond the selected bounded
  literals
- the mobile-web-app metadata could drift from the rest of the identity surface
  if it stops deriving from the same site title and shared color choices

## Follow-On Pressure

- a later slice may revisit whether other platform-specific head metadata is
  justified
- release review should verify that shared mobile-web-app metadata remains
  aligned with the publication's existing manifest and touch-icon surface
