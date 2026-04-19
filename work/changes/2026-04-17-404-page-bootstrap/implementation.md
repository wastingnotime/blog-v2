# Implementation

- kept the not-found artifact in `build_not_found_page(...)` inside
  `src/app/application/use_cases/build_site.py`
- reused the shared document frame so `404.html` matches the rest of the
  static publication chrome
- pointed recovery links at stable top-level routes: home, search, archives,
  sagas, and library
- retained the generated `404.html` assertions already present in the build
  and scenario tests
