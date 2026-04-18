# Implementation

## Summary

Implemented bounded browser-search autodiscovery for the static publication by:

- generating `opensearch.xml` from existing site settings and the current
  `/search/?q=` contract
- advertising that artifact from the shared HTML head with
  `rel="search"` metadata
- extending deterministic unit and integration coverage for both the root
  artifact and shared head contract

## Changed Areas

- `src/app/application/use_cases/build_site.py`
- `tests/unit/test_build_site.py`
- `tests/integration/test_run_scenario.py`

## Notes

- The OpenSearch description stays aligned with the existing static search
  route instead of introducing a second endpoint.
- The change remains metadata-only; search ranking, query handling, and route
  inventory are unchanged.
