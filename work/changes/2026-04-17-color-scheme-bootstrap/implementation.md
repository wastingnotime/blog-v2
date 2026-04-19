# Implementation

- kept `meta name="color-scheme"` in the shared head renderer in
  `src/app/application/use_cases/build_site.py`
- kept the value aligned with the existing `color-scheme: light` CSS contract
  in the generated HTML
- preserved the current browser-facing metadata contract for theme-color,
  mobile-web-app, referrer, and application-name fields
- retained the head assertions in the build and integration tests that verify
  the generated color-scheme metadata
