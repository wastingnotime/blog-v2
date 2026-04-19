# Implementation

- kept footer projection in `project_footer_attribution(...)` and the shared
  document renderer in `src/app/application/use_cases/build_site.py`
- preserved deterministic footer attribution text and publication year across
  homepage, section pages, content pages, and narrative routes
- kept the footer outside route-specific body content so the shared chrome stays
  consistent across generated pages
- retained the current assertions in `tests/unit/test_project_footer_attribution.py`
  and the page-level integration coverage in the site build tests
