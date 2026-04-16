# Implementation

## Summary

Implemented the homepage editorial bootstrap by moving root-route projection
rules into a dedicated application use case and replacing the bootstrap status
card with publication-oriented homepage sections.

## Main Changes

- added `project_homepage_surface` to compute:
  - bounded recent entries for `/`
  - saga summaries with episode count and last release date
- extended content view models with homepage-specific summary types instead of
  overloading section-hub projections
- updated homepage rendering in `build_site.py` to:
  - use editorial intro copy
  - show deterministic recent-entry metadata
  - render active saga summaries derived from real content
- added deterministic unit coverage for homepage projection and updated
  generated-output tests for the new homepage contract

## Validation

- `PYTHONPATH=. python3 -m pytest`
- `PYTHONPATH=. python3 -m src.app.interfaces.cli.run_scenario`
