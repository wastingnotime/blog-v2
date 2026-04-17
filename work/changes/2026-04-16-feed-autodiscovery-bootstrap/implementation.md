# Implementation

## Summary

Implemented RSS autodiscovery by adding a deterministic `rel="alternate"`
link for the existing `feed.xml` artifact in the shared HTML document head.

## Main Changes

- updated `build_site.py` shared document rendering to emit:
  - one RSS autodiscovery link targeting `feed.xml`
  - a stable feed title derived from the configured site title
- added unit and integration coverage for:
  - autodiscovery metadata on representative generated pages
  - absolute feed URLs derived from the configured base URL
  - unchanged visible shared chrome behavior

## Validation

- `PYTHONPATH=. python3 -m pytest`
- `PYTHONPATH=. python3 -m src.app.interfaces.cli.run_scenario`
