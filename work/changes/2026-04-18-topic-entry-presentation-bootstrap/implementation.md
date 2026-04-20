# Implementation

## Summary

Implemented a bounded topic-page presentation refinement by rendering topic
pages through the legacy blog shell on `/library/<tag>/` without changing
topic discovery, topic ordering, or topic routes.

## Main Changes

- added `docs/slices/2026-04-18-topic-entry-presentation-bootstrap.md` to
  define the bounded topic-entry row contract
- added `work/changes/2026-04-18-topic-entry-presentation-bootstrap/impact_analysis.md`
  to record the topic-page-only boundary and risks
- updated `src/app/application/use_cases/build_site.py` so topic pages now:
  - render through the legacy blog shell instead of the generic document frame
  - keep the same discovered entry ordering, routes, and supporting context
  - render entry rows with the older compact blog rhythm rather than the newer
    generic topic list
- updated unit and integration assertions to cover the topic-entry row
  treatment while leaving library-index chips unchanged

## Validation

- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `python3 -m src.app.interfaces.cli.run_scenario`
