# Implementation Notes

## Summary

Implemented a bounded shared-shell polish by replacing the flat background with
subtle layered gradients in the existing document renderer.

## Changes

- updated the shared `body` background in
  `src/app/application/use_cases/build_site.py` to use layered radial and
  linear gradients instead of a flat fill
- kept the dark editorial tokens, typography, links, borders, and routing
  unchanged
- added shell assertions in unit and integration tests to verify the layered
  background contract

## Validation

- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
