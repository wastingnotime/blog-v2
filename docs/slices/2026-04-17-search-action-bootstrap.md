# Slice: 2026-04-17 Search Action Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic static search-entry contract across structured data and the
existing `/search/` surface:

- extend the bounded homepage `WebSite` JSON-LD with one explicit search
  action target
- teach the generated search page to hydrate its query from a stable `?q=`
  URL contract
- keep the slice limited to search entry semantics rather than broader search
  ranking or new schema work

## Discovery Scope

The publication now exposes both halves of a search discovery story, but they
still do not connect to each other:

- `2026-04-17-json-ld-bootstrap` added homepage `WebSite` structured data, but
  it explicitly deferred `SearchAction`
- `2026-04-17-search-page-bootstrap` added `/search/` backed by the static
  `search.json` artifact, but the page only filters after direct typing and
  does not project an addressable query contract

That leaves one coherent machine-readable gap in the current static
publication:

- schema-aware consumers can see the site as a `WebSite`, but they cannot see
  how the site's own search should be invoked
- readers can use `/search/`, but direct links such as `/search/?q=hireflow`
  do not yet behave deterministically on first load

This slice restores the minimum static search-entry surface needed for the
current publication:

- homepage `WebSite` JSON-LD includes one bounded `SearchAction`
- the search page reads an initial query from `?q=`
- the search input, initial status, and first rendered results stay aligned
  with the same static URL contract

This slice does not attempt fuzzy ranking, query suggestions, `BreadcrumbList`,
schema expansion for additional route families, or a broader search UI rewrite.

## Use-Case Contract

### `ProjectWebsiteSearchAction`

Given the configured site base URL and the existing homepage structured-data
projection, add a deterministic site-search action such that:

- homepage `WebSite` JSON-LD advertises one `SearchAction`
- the action target resolves to `/search/?q={search_term_string}` under the
  configured base URL
- the slice stays bounded to the current site-level search surface rather than
  introducing a generalized schema registry

### `HydrateSearchPageFromQuery`

Given the generated `/search/` route and a browser request URL, render bounded
client-side behavior such that:

- a `q` query parameter pre-populates the search input
- the page performs the same static-index filtering it already supports for
  typed input
- empty or missing query values keep the current deterministic guidance state

## Main Business Rules

- The site should advertise only search behavior that the generated static
  publication actually supports.
- The `SearchAction` target must use a stable query-string contract rooted at
  `/search/`, not a backend endpoint or hash fragment.
- Search-page query hydration must reuse the existing static `search.json`
  artifact rather than inventing a second search path.
- The canonical URL for `/search/` remains the route URL without a required
  query string; user-entered queries are session-level search state, not new
  canonical documents.
- The slice stays bounded to site-search entry semantics and must not widen
  into ranking changes or richer search product behavior.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- homepage structured-data projection in `src/app/application/use_cases/build_site.py`
- existing search-page renderer and client-side filtering script
- canonical URL and base URL helpers
- existing static `search.json` publication artifact

## Initial Test Plan

- unit test asserting homepage `WebSite` JSON-LD now includes one
  `SearchAction` targeting `/search/?q={search_term_string}`
- unit test asserting the generated search page script reads the initial `q`
  parameter and applies the existing filtering logic on first load
- integration test asserting `dist/index.html` exposes the bounded
  `SearchAction` payload without changing the rest of the JSON-LD contract
- integration test asserting a generated search page supports deep-link entry
  via the `?q=` URL contract without introducing any same-origin `/api`
  dependency

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- `dist/index.html` contains one homepage `WebSite` JSON-LD payload with a
  `SearchAction` target rooted at `https://wastingnotime.org/search/?q=`
- `dist/search/index.html` still references `search.json` and now contains the
  client-side logic required to read an initial `q` query value
- the same filtering behavior remains available for interactive typing after
  first load
- canonical tags, discovery copy, search index output, and the static-only
  hosting contract remain unchanged outside this bounded search-entry addition

## Done Criteria

- homepage `WebSite` JSON-LD advertises one deterministic `SearchAction`
- `/search/` supports bounded deep-link entry through the `?q=` contract
- the search page keeps using the existing static `search.json` artifact
- deterministic tests cover both homepage structured-data output and search-page
  query hydration without widening the slice into broader search work
