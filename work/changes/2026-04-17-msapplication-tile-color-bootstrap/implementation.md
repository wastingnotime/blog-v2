# Implementation

- kept `meta name="msapplication-TileColor"` in the shared head renderer in
  `src/app/application/use_cases/build_site.py`
- continued deriving the value from the shared theme color so the head and
  browserconfig tile output stay aligned
- preserved the existing browser-facing metadata contract for viewport,
  application-name, color-scheme, referrer, theme-color, and mobile-web-app
  fields
- retained the tile-color assertions in the build and integration tests
