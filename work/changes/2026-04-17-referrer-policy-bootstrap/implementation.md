# Implementation

- kept `meta name="referrer"` in the shared head renderer in
  `src/app/application/use_cases/build_site.py`
- continued using a deterministic `strict-origin-when-cross-origin` policy so
  the browser contract stays aligned across generated routes
- preserved the existing browser-facing metadata contract for format-detection,
  theme-color, mobile-web-app, Open Graph, and Twitter Card fields
- retained the referrer-policy assertions in the build and integration tests
