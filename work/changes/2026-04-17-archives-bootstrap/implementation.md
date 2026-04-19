# Implementation

- kept the chronological archive route in `build_archive_page(...)` inside
  `src/app/application/use_cases/build_site.py`
- continued projecting archive rows from repository-authored content in
  reverse-chronological order
- reused the shared site chrome and discovery surface rather than introducing a
  separate archive template family
- kept the archive assertions in the build and integration tests aligned with
  the generated `/archives/` route and row labeling
