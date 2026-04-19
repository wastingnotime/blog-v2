# Implementation

- kept the studio hub rendering in `src/app/application/use_cases/build_site.py`
- used the shared discovery surface to link to sagas, topics, chronology, and
  search from `/studio/`
- preserved the existing route destinations and the surrounding studio body
  content
- retained the studio discovery assertions in the build and integration tests
