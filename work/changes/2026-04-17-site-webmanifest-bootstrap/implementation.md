# Implementation

- kept `build_site_webmanifest(...)` in `src/app/application/use_cases/build_site.py`
  as the single source of the generated manifest
- continued deriving the name, start URL, display mode, theme color,
  background color, and icon metadata from the configured site identity
- preserved the existing identity-asset contract for favicon and touch-icon
  files
- kept the manifest assertions in the build and integration tests aligned with
  the generated `site.webmanifest`
