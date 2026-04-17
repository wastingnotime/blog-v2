# Impact Analysis

## Summary

The next slice should add bounded browser color metadata so the generated static
publication completes its shared identity contract beyond icons, manifest links,
and social metadata.

Current observed gap:

- generated pages still omit a `theme-color` meta tag
- `site.webmanifest` still lacks `theme_color` and `background_color`
- the publication already has a stable shared palette, so the missing fields are
  now a metadata gap rather than a design gap

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- manifest generation in `src/app/application/use_cases/build_site.py`
- deterministic test coverage for representative head and manifest metadata

## Boundary Change

The build gains no new routes or assets. The boundary change is limited to
additional browser-facing metadata in HTML heads and `site.webmanifest`.

## Risks

- scope could drift into visual redesign or dark-mode policy instead of staying
  bounded to metadata
- tests could overfit exact CSS implementation details rather than the shared
  color contract
- manifest and head color values could drift if they stop deriving from one
  bounded identity decision

## Follow-On Pressure

- a later slice may revisit whether platform-specific mobile-web-app metadata is
  justified
- release review should verify that shared color metadata remains aligned with
  the publication's stable visual identity
