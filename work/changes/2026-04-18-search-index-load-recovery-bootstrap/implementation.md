# Implementation: 2026-04-18 Search Index Load Recovery Bootstrap

Implemented the search index load-failure refinement in `build_site.py`:

- gave the fetch-failure branch its own `search-load-recovery` shell and message
- kept the current query, ranking, highlight, no-script, and zero-results behavior unchanged
- preserved the static `/search/` route while making the index-load failure path explicit

Updated deterministic unit and integration tests to verify the load-recovery shell without widening into retries or offline search behavior.
