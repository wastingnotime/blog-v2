# Slice: 2026-04-18 Search Tag Surface Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded result-context improvement for the existing static search surface:

- keep `/search/` backed by the published `search.json` artifact
- preserve the current deterministic ranking and highlight contracts
- surface record tags in rendered results so tag-driven matches are legible
  without changing the current route or artifact model

## Discovery Scope

The publication now has a coherent, ranked, and highlighted static search
route:

- `2026-04-16-search-index-bootstrap` restored `search.json`
- `2026-04-17-search-page-bootstrap` restored `/search/`
- `2026-04-17-search-url-state-bootstrap` made `?q=` shareable
- `2026-04-18-search-ranking-bootstrap` replaced incidental source ordering
  with explicit match-priority behavior
- `2026-04-18-search-highlight-bootstrap` made query matches visible in
  rendered titles, summaries, and context metadata

One bounded reader-facing gap still remains:

- tags participate in search matching and ranking, but they are not rendered in
  the result card at all
- a query can therefore match by tag while leaving no visible explanation in
  the current result presentation
- the result surface stays functionally correct, but one important matching
  field remains hidden from the reader

This slice restores the minimum search-tag surface needed for the current
static publication:

- render tags for results that have them
- allow the current query highlight behavior to apply to surfaced tags
- render surfaced tags through explicit chip-like hooks so search results reuse
  the publication's topic language without becoming new navigation
- keep the change bounded to existing result presentation rather than adding tag
  navigation or new search filters

This slice does not attempt clickable taxonomy navigation from search results,
faceted filtering, query suggestions, or a broader redesign of the search page.

## Use-Case Contract

### `ProjectSearchResultTags`

Given one matching published record from the static search index, project
reader-facing tag context such that:

- result tags can be rendered when the record includes them
- surfaced tags remain deterministic for the same record content
- tags remain secondary context rather than replacing title or summary content
- surfaced tags read as chip-like context rather than plain comma-separated
  helper text

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic client-side search behavior such that:

- the page still filters only against the static published artifact
- tag-driven matches are visible to the reader once results render
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- Search results should surface tags only when the current record already has
  them in `search.json`.
- Surfaced tags should remain secondary context for a result rather than a new
  navigation system or filter control.
- Surfaced tags should remain presentation-only in this slice; they must not
  silently become clickable topic navigation.
- Current query highlighting may apply to surfaced tags when they contain the
  active query.
- The slice stays bounded to result-context rendering and must not widen into
  clickable tag navigation, faceting, or backend indexing changes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing static `search.json` publication artifact
- current browser-side result rendering on `/search/`
- deterministic tag fields already present in the published search index

## Initial Test Plan

- unit test asserting generated search-page script exposes a deterministic tag
  rendering path for results
- unit test asserting surfaced tags use the existing highlight behavior when a
  tag contains the active query
- unit test asserting surfaced tags render through explicit chip hooks rather
  than plain label text
- integration test asserting generated `dist/search/index.html` includes the
  bounded tag-surface logic while preserving the current static route contract
- integration test asserting the search page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page behavior to verify:

- `/search/` still loads the published `search.json` artifact
- results with tags render them as chip-like secondary context
- query highlighting can emphasize matching tags when relevant
- ranking, URL-state, and static-hosting assumptions remain unchanged

## Done Criteria

- `/search/` surfaces result tags when present in the published search record
- tag-driven matches are visible to the reader without changing the current
  ranking behavior
- rendering remains deterministic and static-only
- deterministic tests cover tag surfacing without widening the slice into
  broader search-product work
