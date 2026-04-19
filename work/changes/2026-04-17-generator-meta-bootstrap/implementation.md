# Implementation

- kept `meta name="generator"` in the shared head renderer in
  `src/app/application/use_cases/build_site.py`
- continued using a deterministic static-builder label so generated pages
  identify the build process without exposing mutable version metadata
- preserved the existing browser-facing metadata contract for viewport,
  author, application-name, color-scheme, referrer, theme-color, Windows tile
  color, and mobile-web-app fields
- retained the generator-meta assertions in the build and integration tests
