# Implementation

## Summary

Implemented the bounded sitemap completeness slice by:

- adding `/archives/` to projected sitemap entries
- deriving the archive entry `lastmod` from the same latest publication date
  already used for the homepage chronology
- extending unit and scenario coverage to keep `/archives/` present and
  `/search/` absent

## Changed Areas

- `src/app/application/use_cases/project_publication_metadata.py`
- `tests/unit/test_project_publication_metadata.py`
- `tests/unit/test_build_site.py`
- `tests/integration/test_run_scenario.py`

## Notes

- The change stays limited to sitemap projection and does not alter route
  inventory, crawl directives, or page rendering.
- `/search/` remains outside the sitemap because the current route contract is
  intentionally `noindex,follow`.
