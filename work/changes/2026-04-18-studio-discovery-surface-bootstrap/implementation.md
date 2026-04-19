# Implementation: 2026-04-18 Studio Discovery Surface Bootstrap

Implemented the studio discovery refinement in `build_site.py`:

- added an explicit `studio-discovery-row` shell around each studio destination
- kept the authored studio copy and the four destination routes unchanged
- preserved the studio page as a static section hub with no new runtime dependency

Updated deterministic unit and integration tests to verify the studio-only row shell without altering the shared discovery surface used elsewhere.
