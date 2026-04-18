# Slice: 2026-04-18 Search Highlight Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded result-legibility improvement for the existing static search surface:

- keep `/search/` backed by the published `search.json` artifact
- preserve the current deterministic ranking contract
- add explicit query-match highlighting to rendered results without changing the
  current route or artifact model

## Discovery Scope

The publication now has a coherent and ranked static search route:

- `2026-04-16-search-index-bootstrap` restored `search.json`
- `2026-04-17-search-page-bootstrap` restored `/search/`
- `2026-04-17-search-url-state-bootstrap` made `?q=` shareable
- `2026-04-18-search-ranking-bootstrap` replaced incidental source ordering
  with explicit match-priority behavior

That surface is usable, but one reader-facing gap still remains:

- the page now orders stronger matches first, but it still renders titles and
  summaries as plain text
- readers therefore cannot quickly see what part of a result matched the
  current query
- ranking becomes more intentional, but its reasoning stays visually opaque

This slice restores the minimum search-legibility behavior needed for the
current static publication:

- highlight matched query text in rendered result titles, summaries, and
  metadata context when present
- keep highlighting bounded to the current query and current result rendering
- preserve static hosting, deterministic output, and current ranking behavior

This slice does not attempt fuzzy highlighting, typo tolerance, suggestion UI,
snippet generation, or a broader visual redesign of the search page.

## Use-Case Contract

### `ProjectSearchHighlight`

Given a search query and one matching published record, compute safe browser-side
rendering behavior such that:

- matched text can be visually emphasized in title, summary, and context fields
- non-matching text remains unchanged
- highlighting remains deterministic for the same query and record content

### `RenderSearchPage`

Given the existing `/search/` route and `search.json` contract, render
deterministic client-side search behavior such that:

- the page still filters only against the static published artifact
- the current query is visually legible inside rendered matches
- the route remains valid under GitHub Pages hosting with no same-origin API
  dependency

## Main Business Rules

- Search highlighting must reflect the current query text only.
- Highlighting should appear only in already-rendered result fields rather than
  inventing new snippets or excerpts.
- Titles, summaries, and context metadata may be highlighted when they contain
  the current query.
- Rendering must remain safe and deterministic; highlight behavior must not
  depend on raw HTML injection from the search index.
- The slice stays bounded to result legibility and must not widen into richer
  search UI, new metadata, or backend indexing.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing search-page renderer in `src/app/application/use_cases/build_site.py`
- existing static `search.json` publication artifact
- current browser-side result rendering on `/search/`
- deterministic record fields already present in the published search index

## Initial Test Plan

- unit test asserting generated search-page script exposes a deterministic
  query-highlight rendering path
- unit test asserting rendered result fields use the current query to produce
  bounded highlight markup rather than raw text-only output
- integration test asserting generated `dist/search/index.html` includes the
  bounded highlight logic while preserving the current static route contract
- integration test asserting the search page remains fully static and free of
  same-origin `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
search page behavior to verify:

- `/search/` still loads the published `search.json` artifact
- matching query text is visually emphasized in rendered results when present
- ranking, URL-state, navigation, and static-hosting assumptions remain
  unchanged
- repeated builds preserve the same highlight behavior for the same query and
  repository state

## Done Criteria

- `/search/` highlights current-query matches inside rendered result fields
- highlighting stays bounded to existing result content and preserves current
  ranking behavior
- rendering remains deterministic and static-only
- deterministic tests cover the highlight path without widening the slice into
  broader search-product work
