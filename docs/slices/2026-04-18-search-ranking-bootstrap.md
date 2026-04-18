# Slice: 2026-04-18 Search Ranking Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded result-ordering improvement for the existing static search surface:

- keep `/search/` backed by the published `search.json` artifact
- replace raw catalog-order filtering with deterministic result ranking
- keep the slice limited to ordering and match-priority behavior rather than a
  broader search-product redesign

## Discovery Scope

The publication now has a coherent static search route:

- `2026-04-16-search-index-bootstrap` restored `search.json`
- `2026-04-17-search-page-bootstrap` restored `/search/`
- `2026-04-17-search-url-state-bootstrap` made `?q=` shareable

That surface is usable, but its current result behavior is still incidental:

- `build_search_page(...)` filters records with one flat substring check across
  title, summary, context, and tags
- matching records keep the original search-index order rather than an explicit
  search-result contract
- the current reader experience therefore depends on catalog ordering instead
  of search intent once more than one record matches

This slice restores the minimum ranking behavior needed for the current static
publication:

- exact and title-led matches should appear before weaker summary or tag-only
  matches
- ties should resolve deterministically rather than by incidental source order
- the page should remain fully static and client-side, without introducing a
  search backend, fuzzy library, or faceted application state

This slice does not attempt query suggestions, highlighted snippets, synonym
expansion, typo tolerance, or a redesigned search interface.

## Use-Case Contract

### `ProjectSearchResultOrder`

Given a search query and the published static search records, compute a stable
result order such that:

- exact title matches outrank partial title matches
- title matches outrank context, summary, or tag-only matches
- ties remain deterministic for the same query and repository state

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic client-side search behavior such that:

- the page still filters only against the static published artifact
- stronger matches appear first in the rendered result list
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- Search results must be ordered by an explicit match-strength contract rather
  than raw search-index order.
- Exact title matches should outrank broader substring matches.
- Title matches should outrank summary, context, and tag-only matches for the
  same query.
- Tie-breaking must stay deterministic for the same query and artifact set.
- The slice stays bounded to ranking behavior and must not widen into richer
  search UI, new metadata, or backend indexing.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing static `search.json` publication artifact
- current browser-side filtering path on `/search/`
- deterministic record fields already present in the published search index

## Initial Test Plan

- unit test asserting generated search-page script encodes a deterministic
  ranking path rather than raw filter-order behavior
- unit test asserting exact-title and title-substring matches outrank weaker
  summary, context, or tag-only matches
- integration test asserting generated `dist/search/index.html` includes the
  bounded ranking logic while preserving the current static route contract
- integration test asserting the search page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page behavior to verify:

- `/search/` still loads the published `search.json` artifact
- a query with multiple matches prefers the strongest title-aligned results
- repeated builds preserve the same result ordering for the same query
- URL-state, navigation, and static-hosting assumptions remain unchanged

## Done Criteria

- `/search/` applies deterministic ranking within the current static search
  surface
- title-aligned matches appear ahead of weaker summary, context, or tag-only
  matches
- tie-breaking is stable for the same query and repository state
- deterministic tests cover ranking behavior without widening the slice into
  broader search-product work
