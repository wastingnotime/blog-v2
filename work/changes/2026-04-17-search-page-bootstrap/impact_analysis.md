# Impact Analysis

## Summary

The next slice should add a bounded `/search/` route so the static publication
exposes a reader-facing search surface that actually uses the already-generated
`search.json` artifact.

Current observed gap:

- `search.json` exists, but there is still no generated search page
- the search-index slice explicitly deferred the page and live filtering UI

## Impacted Areas

- static HTML generation for one additional reader-facing route
- shared-frame rendering for a lightweight client-side search interface
- integration coverage for the relationship between `/search/` and `search.json`

## Boundary Change

The build gains one new route: `/search/`. That route should remain fully
static, load the existing `search.json` artifact, and avoid introducing any
backend search dependency.

## Risks

- scope could drift into advanced ranking, faceting, or client application
  state instead of a bounded bootstrap surface
- the search page could duplicate search-index record-shaping logic instead of
  consuming the published artifact
- client-side script behavior could undermine deterministic expectations if the
  page lacks a stable empty state

## Follow-On Pressure

- a later slice may improve ranking, filtering, or visual result treatment once
  the basic search route exists
- release review should compare `/search/`, `search.json`, archives, and topic
  routes so discovery surfaces stay coherent rather than redundant
