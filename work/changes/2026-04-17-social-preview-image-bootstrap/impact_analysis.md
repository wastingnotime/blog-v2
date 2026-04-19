# Impact Analysis

## Summary

This slice adds one bounded social preview image so the generated static
publication completes the shared image side of its social metadata surface.

Current observed contract:

- generated pages include bounded Open Graph and Twitter text metadata
- the shared head includes `og:image` and `twitter:image`
- the generated root artifact set includes a shared social preview image

## Impacted Areas

- static build output for repository-owned assets
- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- deterministic integration coverage for copied assets and representative head
  metadata

## Boundary Change

The build gains one static asset plus additional head metadata. No new route
or browser-side runtime behavior is required.

## Risks

- scope could drift into generated per-route cards or broader branding work
  instead of staying bounded to one shared asset
- tests could overfit exact asset filenames without asserting the actual
  publication contract
- metadata and copied asset paths could drift if the head renderer stops
  deriving image URLs from the published asset location

## Follow-On Pressure

- a later slice may revisit whether per-route preview images are justified
- release review should verify that the social preview asset remains aligned
  with the rest of the static identity surface
