# Impact Analysis

## Summary

The next slice should correct route-specific crawl semantics so the generated
static publication keeps real reader-facing routes indexable while preventing
the shared `404.html` recovery page from advertising itself as indexable
content.

Current observed gap:

- `_render_document(...)` currently emits one shared
  `<meta name="robots" content="index,follow" />` tag for every generated page
- `build_not_found_page(...)` inherits that metadata unchanged, so the not-found
  route presents the same crawl contract as valid publication pages
- `robots.txt` already exists for site-wide crawler policy, which makes the
  remaining gap specifically route-level robots metadata rather than another
  root artifact

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- route-specific metadata projection for generated pages
- deterministic test coverage for homepage versus `404.html` robots behavior

## Boundary Change

The build does not gain new routes or new root artifacts. Instead, one existing
shared metadata contract becomes route-aware: `404.html` should render
`noindex,follow` while the current public publication routes keep
`index,follow`.

## Risks

- scope could drift into broader route taxonomy or generalized SEO settings
  instead of staying bounded to the 404 distinction
- tests could overfit exact head ordering instead of the intended route-specific
  robots values
- a future renderer change could accidentally collapse route-specific metadata
  back into one shared default if the distinction is not made explicit

## Follow-On Pressure

- a later slice may revisit richer machine-readable publication semantics such
  as JSON-LD once crawl semantics are internally consistent
- release review should verify that `robots.txt`, canonical URLs, and route-
  specific robots metadata still form one coherent publication-discovery
  contract
