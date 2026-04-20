# Implementation

## Scope

Replace the legacy saga, arc, and episode route blob decoders with direct code literals while preserving the legacy blog HTML output.

## What Changed

- Converted `legacy_saga_pages.py`, `legacy_arc_pages.py`, and `legacy_episode_pages.py` to store the legacy HTML as direct Python string literals.
- Kept the route lookup functions, but removed the `base64` and `zlib` decode path.
- Normalized the returned strings to preserve the exact legacy snapshot boundaries.

## Validation

- `python3 -m py_compile src/app/application/use_cases/legacy_saga_pages.py src/app/application/use_cases/legacy_arc_pages.py src/app/application/use_cases/legacy_episode_pages.py src/app/application/use_cases/build_site.py`
- `python3 -m pytest tests/unit/test_build_site.py tests/integration/test_run_scenario.py -q`
