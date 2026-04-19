# Implementation: 2026-04-18 Search Empty Results Recovery Bootstrap

Implemented the zero-results recovery refinement in `build_site.py`:

- added an explicit `search-empty-recovery` shell for no-match and load-failure guidance
- rendered stable recovery rows pointing to `/archives/` and `/library/`
- kept the existing query, ranking, highlighting, and static route behavior unchanged

Updated deterministic unit and integration tests to verify the search-only recovery shell without widening into suggestions, alternative-query generation, or backend search behavior.
