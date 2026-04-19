# Implementation

- kept `.nojekyll` in `build_nojekyll()` inside
  `src/app/application/use_cases/build_site.py`
- continued emitting the root artifact through the same static build pipeline
  that GitHub Pages deploys
- preserved the deterministic root-artifact assertions in the build and
  integration tests
- kept the GitHub Pages workflow aligned with serving the generated `dist/`
  directory as static files
