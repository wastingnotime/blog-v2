# Implementation

- kept the shared viewport literal in `src/app/application/use_cases/build_site.py`
- rendered `viewport-fit=cover` in the shared document head for generated HTML
  pages
- preserved the existing mobile head contract around application-name,
  color-scheme, referrer, theme-color, and mobile-web-app metadata
- retained the viewport assertions in the build and integration tests
