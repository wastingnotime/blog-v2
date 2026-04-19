# Impact Analysis

## Summary

This slice adds bounded color-scheme metadata so the generated static
publication makes its light-only browser-facing styling contract explicit in
the shared document head.

Current observed contract:

- generated pages include theme-color, Apple mobile-web-app, and referrer
  metadata
- the shared head includes `meta name="color-scheme"`
- the shared CSS declares `color-scheme: light`, so the head metadata and CSS
  agree on the same visual contract

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- deterministic test coverage for representative head metadata
- regression protection around unchanged theme-color, mobile-web-app,
  referrer, and social metadata

## Boundary Change

The build gains no new routes or assets. The boundary change is limited to
browser-facing metadata already present in generated HTML heads.

## Risks

- scope could drift into dark-mode or broader CSS redesign work instead of
  staying bounded to shared metadata
- tests could overfit incidental head ordering rather than the selected
  color-scheme contract
- the color-scheme literal could drift from the existing shared CSS identity if
  it stops deriving from the same publication styling decision

## Follow-On Pressure

- a later slice may revisit whether richer browser-facing appearance metadata is
  justified
- release review should verify that shared color-scheme metadata remains
  aligned with the publication's existing light-only styling contract
