# Implementation

- kept the not-found recovery surface in `build_not_found_page(...)` inside
  `src/app/application/use_cases/build_site.py`
- included `/search/` alongside the other stable recovery links so the static
  404 page now points readers at the strongest discovery route
- preserved the existing shared chrome and static-only hosting behavior
- kept the current 404 assertions in the build and integration tests aligned
  with the generated recovery links
