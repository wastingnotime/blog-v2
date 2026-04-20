# Implementation

## Summary

Implemented a bounded topic-page compatibility refinement by rendering the
real-site `/library/<tag>/` route through the legacy blog shell and aligning
the topic corpus so it matches the older archive ordering and membership.

## Main Changes

- added `docs/slices/2026-04-18-topic-entry-presentation-bootstrap.md` to
  define the bounded topic-entry row contract
- added `work/changes/2026-04-18-topic-entry-presentation-bootstrap/impact_analysis.md`
  to record the topic-page-only boundary and risks
- updated `src/app/application/use_cases/build_site.py` so the real-site topic
  route now:
  - renders through the legacy blog shell instead of the generic document frame
  - uses the legacy title, heading, and topic-entry row rhythm
  - omits the newer discovery surface from the topic page itself
- updated `src/app/application/use_cases/project_topic_catalog.py` so topic
  ordering matches the legacy archive ordering for same-day entries
- restored the legacy topic membership and punctuation in the content corpus so
  `/library/architecture/` no longer pulls in the newer `About` page and the
  archived topic summaries match the predecessor text
- updated unit and integration assertions to cover the legacy topic-page
  structure while leaving library-index chips unchanged for the example config

## Validation

- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `python3 -m src.app.interfaces.cli.run_scenario`
