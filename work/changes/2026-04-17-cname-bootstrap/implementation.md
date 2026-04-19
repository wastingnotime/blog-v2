# Implementation

- kept the root `CNAME` artifact in `build_cname(...)` inside
  `src/app/application/use_cases/build_site.py`
- continued deriving the hostname from `SITE_BASE_URL` so GitHub Pages sees
  the configured custom-domain target
- preserved the existing build output contract without adding any route or
  browser behavior changes
- retained the deterministic root-artifact assertions in the scenario and
  builder tests
