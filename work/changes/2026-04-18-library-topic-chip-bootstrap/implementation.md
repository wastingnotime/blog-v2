# Implementation

## Summary

Implemented a bounded library-index presentation refinement by rendering
discovered topics as explicit outlined chip links on `/library/` without
changing topic discovery, topic routes, or other list surfaces.

## Main Changes

- added `docs/slices/2026-04-18-library-topic-chip-bootstrap.md` to define the
  bounded library-topic chip contract
- added `work/changes/2026-04-18-library-topic-chip-bootstrap/impact_analysis.md`
  to record the `/library/`-only boundary and risks
- updated `src/app/application/use_cases/build_site.py` so the library index
  now:
  - renders discovered topics inside `library-topic-list`
  - renders each topic through a `topic-link` outlined chip treatment
  - preserves the same discovered topic ordering and `/library/<tag>/` routes
- updated unit and integration assertions to cover the chip markup on
  `/library/` while leaving topic pages unchanged

## Validation

- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `python3 -m src.app.interfaces.cli.run_scenario`
