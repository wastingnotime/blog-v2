# Implementation

- kept Twitter Card metadata rendering in `src/app/application/use_cases/build_site.py`
- derived `twitter:card`, title, description, URL, and image fields from the
  same canonical inputs used by Open Graph
- preserved the existing head metadata ordering and chrome behavior
- retained the Twitter Card assertions in the build and integration tests
