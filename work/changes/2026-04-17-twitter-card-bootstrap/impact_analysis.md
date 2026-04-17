# Impact Analysis

## Summary

The next slice should add bounded Twitter Card metadata so the generated static
publication has a complete shared social-metadata surface beyond Open Graph.

Current observed gap:

- generated pages now include canonical, RSS, manifest, identity, and Open
  Graph metadata
- the shared head still omits `twitter:*` metadata
- the publication therefore remains incomplete for one major link-preview
  consumer even though the existing deterministic inputs already exist

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- deterministic head metadata coverage for representative HTML routes
- regression protection around unchanged Open Graph and visible chrome behavior

## Boundary Change

The build gains no new route or root artifact. The boundary change is limited
to additional social metadata rendered in generated HTML heads.

## Risks

- scope could drift into image generation or account-handle policy instead of
  staying bounded to shared metadata
- tests could overfit exact ordering rather than the presence and values of the
  required tags
- metadata values could drift from canonical inputs if the head renderer stops
  deriving them from the existing document contract

## Follow-On Pressure

- a later slice may revisit whether social preview images or account-specific
  metadata are justified
- release review should verify that Twitter Card metadata remains aligned with
  the same canonical title, description, and URL sources as Open Graph
