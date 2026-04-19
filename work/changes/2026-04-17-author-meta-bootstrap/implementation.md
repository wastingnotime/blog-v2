# Implementation

- kept `meta name="author"` in the shared head renderer in
  `src/app/application/use_cases/build_site.py`
- continued deriving the value from the configured publication host so it
  stays aligned with the shared site identity
- preserved the existing browser-facing metadata contract for viewport,
  application-name, color-scheme, referrer, theme-color, tile color, and
  mobile-web-app fields
- kept the head assertions in the build and integration tests aligned with the
  generated author metadata
