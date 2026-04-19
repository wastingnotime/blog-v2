# Impact Analysis

## Summary

The generated static publication now exposes the bounded Twitter Card metadata
surface.

Current observed contract:

- generated pages include canonical, RSS, manifest, identity, Open Graph, and
  Twitter Card metadata
- the shared head renders the `twitter:*` fields from the existing canonical
  inputs
- the publication has one coherent social-preview contract across link
  consumers

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- deterministic head metadata coverage for representative HTML routes
- regression protection around unchanged Open Graph and visible chrome behavior

## Boundary Change

The build already renders the needed metadata. The boundary stays limited to
the social metadata fields in generated HTML heads.

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
