# Implementation: 2026-04-18 Homepage List Presentation Bootstrap

Implemented the homepage recent-entry row refinement in `build_site.py`:

- added an explicit `homepage-recent-row` shell around recent-entry title and metadata
- kept the existing homepage recent-entry facts, saga summaries, route, and navigation links unchanged
- preserved the compact inline saga-summary status treatment already present on the homepage

Updated deterministic unit and integration tests to verify the homepage-only recent-entry row shell without widening into archive, topic, or section list rendering.
