# Implementation

## Summary

Implemented reader-facing entry metadata for standalone pages and saga episodes
by adding a shared projection for reading time and tag links, then rendering
that metadata near the top of content entries.

## Main Changes

- added `project_entry_metadata` to compute:
  - deterministic reading-time estimates from markdown body text
  - tag links back into existing `/library/<tag>/` routes
- extended the content model with entry-metadata view records
- updated page and episode rendering in `build_site.py` to show:
  - publication date
  - reading time
  - linked tags when present
- added unit and integration coverage for entry metadata projection and
  generated output

## Validation

- `PYTHONPATH=. python3 -m pytest`
- `PYTHONPATH=. python3 -m src.app.interfaces.cli.run_scenario`
