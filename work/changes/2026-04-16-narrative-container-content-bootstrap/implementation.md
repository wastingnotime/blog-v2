# Implementation

## Summary

Implemented authored narrative container content by retaining saga and arc body
markdown in the content model and rendering that content on saga and arc routes
before their existing navigation sections.

## Main Changes

- extended `Saga` and `Arc` to retain `body_markdown`
- updated `MarkdownContentLoader` to preserve authored markdown bodies from:
  - `content/sagas/<saga>/index.md`
  - `content/sagas/<saga>/<arc>/index.md`
- updated `build_site.py` so:
  - saga pages render authored container copy before arcs and timeline
  - arc pages render authored container copy before episode lists
- updated unit and integration tests to cover loading and rendering of
  narrative container content

## Validation

- `PYTHONPATH=. python3 -m pytest`
- `PYTHONPATH=. python3 -m src.app.interfaces.cli.run_scenario`
