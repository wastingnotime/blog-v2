# Implementation: 2026-04-18 404 Recovery Surface Bootstrap

Implemented the 404 recovery refinement in `build_site.py`:

- added an explicit `not-found-row` shell around each recovery destination
- kept the current recovery labels, destination routes, copy, and robots contract unchanged
- preserved the 404 page as a static recovery surface with no new runtime dependency

Updated deterministic unit and integration tests to verify the 404-only row shell without widening into redirect or search-product behavior.
