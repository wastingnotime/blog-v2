# Slice: 2026-04-17 Search URL State Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic search-state alignment for the existing `/search/` route:

- let the generated search page emit the same `?q=` contract it already reads
- keep interactive filtering and URL state synchronized on one bounded route
- keep the slice limited to search query addressability rather than ranking or
  richer search product work

## Discovery Scope

The current publication now advertises one explicit site-search entry contract:

- `2026-04-17-search-action-bootstrap` taught homepage `WebSite` JSON-LD to
  target `/search/?q={search_term_string}`
- that same slice taught `/search/` to hydrate from `?q=` on first load

But the generated search page still behaves asymmetrically after that first
load:

- typing a new query filters results in place, but the address bar does not
  update to the current `?q=` value
- the search surface therefore consumes the advertised URL contract without
  letting readers naturally reproduce or share it from the page itself
- that leaves one bounded mismatch between machine-readable search entry and
  reader-facing search behavior

This slice restores the minimum static search-state coherence needed for the
current publication:

- `/search/` should both read and write the same `?q=` contract
- interactive search should keep results and browser URL state aligned
- canonical metadata should remain centered on `/search/` rather than creating
  per-query canonical documents

This slice does not attempt ranking changes, query suggestions, result
highlighting, search analytics, or a broader search UI redesign.

## Use-Case Contract

### `ProjectSearchUrlState`

Given the generated `/search/` route and the bounded `?q=` entry contract,
project browser-side behavior such that:

- an initial `q` query still hydrates the search input and first rendered
  result state
- submitting or changing the current search updates the browser URL to the same
  `?q=` contract
- clearing the query returns the browser URL to `/search/` without a required
  empty query parameter

### `RenderSearchPage`

Given the current static search surface, render deterministic page markup such
that:

- the search control can express a shareable `GET`-style query contract
- the page keeps using the existing static `search.json` artifact for result
  filtering
- route behavior remains valid under static GitHub Pages hosting

## Main Business Rules

- The search page must honor one search-query contract end to end: `?q=` on
  `/search/`.
- Search URL state must remain route-level session state, not a new canonical
  document family.
- Clearing the search should remove the query parameter rather than publishing
  `/search/?q=`.
- The page must keep using the existing static `search.json` artifact rather
  than inventing a second search path or backend dependency.
- The slice stays bounded to URL-state coherence and must not widen into search
  ranking or broader information architecture work.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- browser-side query-string and history handling on the generated `/search/`
  route
- existing static `search.json` publication artifact
- canonical URL rendering that keeps `/search/` canonical without requiring a
  query string

## Initial Test Plan

- unit test asserting generated `/search/` markup exposes a deterministic
  `GET`-style query contract rooted at `/search/`
- unit test asserting the search-page script updates URL state for non-empty and
  cleared queries while preserving the existing filtering path
- integration test asserting generated `dist/search/index.html` contains the
  bounded URL-state hooks without changing canonical metadata
- integration test asserting the search page remains fully static and free of
  same-origin `/api` assumptions while supporting shareable query URLs

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- `dist/search/index.html` still references `search.json` and still hydrates
  from `?q=`
- the page now exposes one deterministic search submission shape rooted at
  `/search/`
- browser-side logic updates the current URL to match the active query and
  removes `q` when the query is cleared
- canonical tags, shared navigation, discovery copy, and the static-only
  hosting contract remain unchanged outside this bounded URL-state addition

## Done Criteria

- `/search/` both reads and writes the bounded `?q=` search contract
- interactive search keeps browser URL state aligned with the current query
- clearing the query restores `/search/` without an empty `q` parameter
- deterministic tests cover URL-state behavior without widening the slice into
  broader search work
