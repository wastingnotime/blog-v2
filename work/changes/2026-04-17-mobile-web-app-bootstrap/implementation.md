# Implementation

- kept the Apple mobile-web-app metadata in the shared head renderer in
  `src/app/application/use_cases/build_site.py`
- continued deriving the values from the configured site title, theme color,
  and touch icon surface
- preserved the existing browser-facing metadata contract for manifest,
  theme-color, and identity assets
- retained the mobile-web-app assertions in the build and integration tests
