# Implementation

- kept the ranking logic in `src/app/application/use_cases/build_site.py`
- sorted `/search/` results by match strength before rendering them
- preserved the existing static search route, query-state behavior, and
  highlighting path
- retained the ranking assertions in the build and integration tests
