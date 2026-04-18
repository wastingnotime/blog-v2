# Implementation

## Summary

Implemented a bounded studio-page refinement by replacing the generic fallback
discovery block on `/studio/` with explicit studio discovery rows while
preserving the same destination labels, routes, and authored studio copy.

## Main Changes

- added `docs/slices/2026-04-18-studio-discovery-surface-bootstrap.md` to
  define the bounded studio discovery-surface contract
- added `work/changes/2026-04-18-studio-discovery-surface-bootstrap/impact_analysis.md`
  to record the `/studio/`-only boundary and risks
- updated `src/app/application/use_cases/build_site.py` so the studio page now:
  - renders its existing destinations through `_render_studio_discovery_surface`
  - uses explicit `studio-discovery-list`, `studio-discovery-label`, and
    `studio-discovery-path` hooks
  - preserves the existing four labels and destination routes
- updated unit and integration assertions to cover the studio-specific
  discovery surface while keeping generic shared discovery checks for other
  routes

## Validation

- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py`
- `python3 -m src.app.interfaces.cli.run_scenario`
