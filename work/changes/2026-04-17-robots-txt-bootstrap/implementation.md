# Implementation

- kept `build_robots_txt(...)` in `src/app/application/use_cases/build_site.py`
  as the single source of the root crawler-policy artifact
- continued deriving the sitemap reference from the configured base URL so the
  policy stays aligned with the generated `sitemap.xml`
- preserved the existing root-artifact assertions in the build and integration
  tests
- kept the policy bounded to a single public-site directive plus sitemap line
