# Implementation

- kept the shared social preview image in `assets/site/current/social-preview.png`
- continued deriving `og:image` and `twitter:image` from the published asset
  path in `src/app/application/use_cases/build_site.py`
- preserved the existing Open Graph and Twitter Card text metadata contract
- kept the copied-asset and head-metadata assertions in the build and
  integration tests aligned with the generated social preview surface
