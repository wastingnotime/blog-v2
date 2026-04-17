# Implementation

## Summary

Implemented shared RSS discoverability by exposing the existing `feed.xml`
artifact through the common site navigation on generated HTML pages.

## Main Changes

- updated `build_site.py` shared navigation rendering to append a stable `RSS`
  link targeting `feed.xml`
- kept existing active-state rendering for Home, Sagas, Library, Studio, and
  About unchanged
- added unit and integration coverage for:
  - RSS link rendering in shared chrome
  - absolute feed link URLs derived from the configured base URL
  - unchanged active section behavior across representative routes

## Validation

- `PYTHONPATH=. python3 -m pytest`
- `PYTHONPATH=. python3 -m src.app.interfaces.cli.run_scenario`
