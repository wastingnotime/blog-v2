# Implementation

- kept the build anchored on `src/app/interfaces/cli/run_scenario.py` and the
  `StaticSiteBuilder` pipeline so `dist/` remains the single deployment
  artifact
- preserved the GitHub Pages workflow in `.github/workflows/gh-pages.yml`
  with `pytest` before `python -m src.app.interfaces.cli.run_scenario`
- preserved the no-`/api` static-site contract already asserted in
  `tests/unit/test_build_site.py` and
  `tests/integration/test_run_scenario.py`
- kept the deployment target compatible with the static output that the local
  build and CI both produce
