# Impact Analysis

## Summary

The next slice should add bounded application-name metadata so the generated
static publication completes another small cross-browser identity surface in
the shared document head using title information it already owns.

Current observed gap:

- generated pages now include theme-color, mobile-web-app, referrer, and
  color-scheme metadata
- the shared head still omits `meta name="application-name"`
- the publication already has a stable site title plus manifest and Apple
  application identity fields, so the next gap is explicit browser metadata
  rather than a naming problem

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- deterministic test coverage for representative head metadata
- regression protection around unchanged theme-color, mobile-web-app,
  referrer, color-scheme, and social metadata

## Boundary Change

The build gains no new routes or assets. The boundary change is limited to
additional browser-facing metadata in generated HTML heads.

## Risks

- scope could drift into browser-specific tile metadata or broader PWA work
  instead of staying bounded to shared metadata
- tests could overfit incidental head ordering rather than the selected
  application-name contract
- the chosen value could drift from the configured site title if it stops
  deriving from the existing shared identity surface

## Follow-On Pressure

- a later slice may revisit whether any additional browser-facing identity
  metadata is justified
- release review should verify that shared application-name metadata remains
  aligned with the manifest name and Apple mobile-web-app title
