# Implementation

- kept the shared theme-color constant and background color in
  `src/app/application/use_cases/build_site.py`
- rendered `theme-color` in the shared document head for generated HTML pages
- propagated the same color identity into `site.webmanifest`
- preserved the existing metadata assertions in the build and integration
  tests
