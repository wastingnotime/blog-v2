# Implementation

- kept `meta name="application-name"` in the shared head renderer in
  `src/app/application/use_cases/build_site.py`
- continued deriving the value directly from the configured site title so it
  stays aligned with the manifest and mobile-web-app title fields
- preserved the existing theme-color, mobile-web-app, referrer, and
  color-scheme metadata contract
- kept the existing head assertions in the build and integration tests aligned
  with the generated browser identity metadata
