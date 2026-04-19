# Implementation

- kept the highlight logic in `src/app/application/use_cases/build_site.py`
- used controlled DOM fragments to emphasize query matches in titles, summaries,
  metadata context, and tags
- preserved the existing static `/search/` route and ranking behavior
- retained the highlight assertions in the build and integration tests
