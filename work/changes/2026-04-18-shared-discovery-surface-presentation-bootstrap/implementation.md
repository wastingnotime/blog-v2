# Implementation

## Summary

Implemented a bounded shared discovery-surface refinement by rendering generic
`Other ways in` sections through explicit row hooks while preserving current
labels, routes, and route-specific destination choices.

## Main Changes

- added `docs/slices/2026-04-18-shared-discovery-surface-presentation-bootstrap.md`
  to define the bounded shared discovery-row contract
- added `work/changes/2026-04-18-shared-discovery-surface-presentation-bootstrap/impact_analysis.md`
  to record the shared-helper boundary and risks
- updated `src/app/application/use_cases/build_site.py` so the shared helper
  now:
  - renders destinations inside `discovery-list`
  - renders each row through `discovery-label` and `discovery-path` hooks
  - preserves existing labels, routes, and page-specific destination choices
- updated unit and integration assertions to cover the new shared row treatment
  while leaving the studio-specific discovery surface unchanged

## Validation

- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `python3 -m src.app.interfaces.cli.run_scenario`
