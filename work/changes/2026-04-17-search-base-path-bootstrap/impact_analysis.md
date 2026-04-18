# Impact Analysis

## Summary

The next slice should remove the last root-relative escape hatch in the static
publication by aligning the search form action with `SiteConfig.base_url`.

Current observed gap:

- the repository already treats `base_url` as the source of truth for
  canonical URLs, navigation links, feed discovery, OpenSearch, and search
  index loading
- `build_search_page(...)` still emits `action="/search/"`, which breaks the
  contract for prefixed static hosting
- unit and integration tests currently lock that root-relative behavior in as
  if it were correct

## Impacted Areas

- search-page rendering in `src/app/application/use_cases/build_site.py`
- deterministic HTML contract for the generated search form
- unit and integration coverage for prefixed `SITE_BASE_URL` handling

## Boundary Change

The build gains no new route, artifact, or browser-side feature. The boundary
change is limited to how the existing search route target is rendered in the
generated HTML and validated in tests.

## Risks

- the slice could drift into a broader audit of every client-side route concern
  instead of staying focused on search form submission
- tests could overfit one exact absolute URL shape without asserting the real
  contract, which is alignment with `SiteConfig.base_url`
- the JavaScript enhancement path could be changed unnecessarily even though
  the current pressure is the non-JavaScript and early-submit fallback

## Follow-On Pressure

- a later slice may audit the generated site for any other root-relative
  literals that bypass `SiteConfig.base_url`
- release review should verify that search submission, canonical metadata, and
  search index loading all describe one consistent published route
