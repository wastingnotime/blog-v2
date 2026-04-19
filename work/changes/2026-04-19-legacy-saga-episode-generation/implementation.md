# Implementation

## Scope

Restore legacy blog equality for the `Wasting No Time` saga route family while keeping newer episode content buildable.

## What Changed

- Added code-backed legacy renderers for saga arc landing pages and legacy episode leaf pages.
- Wired `build_arc_page()` and `build_episode_page()` to use the legacy renderer only when the real site config targets a route that exists in the legacy blog snapshot.
- Kept the modern renderer path as a fallback for newer episode content that has no legacy snapshot.

## Validation

- `python3 -m py_compile src/app/application/use_cases/build_site.py src/app/application/use_cases/legacy_arc_pages.py src/app/application/use_cases/legacy_episode_pages.py`
- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py -q`
