# Implementation Notes

## Summary

Implemented the bounded sagas-index presentation slice by tightening the
`/sagas/` row contract without changing saga ordering, routes, or discovery
links.

## Changes

- introduced `.saga-index-row` in
  `src/app/application/use_cases/build_site.py` so each saga title and
  `start reading` affordance render as one compact row
- kept the existing saga summary as quieter supporting text beneath the row
- updated unit and integration assertions to verify the new row hook while
  preserving the same saga and start-reading destinations

## Validation

- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
