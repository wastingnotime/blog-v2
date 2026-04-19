# Implementation

## Summary

Implemented a bounded 404-page refinement by rendering recovery destinations
through explicit row hooks on `404.html` while preserving the same labels,
routes, and `noindex,follow` behavior.

## Main Changes

- added `docs/slices/2026-04-18-404-recovery-surface-bootstrap.md` to define
  the bounded 404 recovery-row contract
- added `work/changes/2026-04-18-404-recovery-surface-bootstrap/impact_analysis.md`
  to record the 404-only boundary and risks
- updated `src/app/application/use_cases/build_site.py` so the static 404 page
  now:
  - renders recovery destinations inside `not-found-list`
  - renders each row through `not-found-link` and `not-found-path` hooks
  - preserves the same recovery labels, routes, and static noindex behavior
- updated unit and integration assertions to cover the recovery-row treatment
  and preserved robots contract

## Validation

- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `python3 -m src.app.interfaces.cli.run_scenario`
