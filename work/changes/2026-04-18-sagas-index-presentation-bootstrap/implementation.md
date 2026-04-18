# Implementation

## Summary

Implemented a bounded sagas-index presentation refinement by rendering active
sagas through explicit editorial row hooks on `/sagas/` without changing saga
ordering, saga routes, or start-reading destinations.

## Main Changes

- added `docs/slices/2026-04-18-sagas-index-presentation-bootstrap.md` to
  define the bounded sagas-index row contract
- added `work/changes/2026-04-18-sagas-index-presentation-bootstrap/impact_analysis.md`
  to record the `/sagas/`-only boundary and risks
- updated `src/app/application/use_cases/build_site.py` so the sagas hub now:
  - renders active sagas inside `saga-index-list`
  - renders each row through explicit `saga-index-link` and
    `saga-index-summary` hooks
  - keeps `start reading` as a bounded secondary affordance through
    `saga-index-start`
- updated unit and integration assertions to cover the sagas-index row
  treatment while leaving homepage and individual saga pages unchanged

## Validation

- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `python3 -m src.app.interfaces.cli.run_scenario`
