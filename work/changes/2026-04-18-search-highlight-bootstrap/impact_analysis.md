# Impact Analysis

## Summary

The next coherent slice is to make the ranked static search results explain
themselves visually by highlighting current-query matches inside rendered
result fields.

Current observed gap:

- `/search/` now ranks stronger matches first
- titles, summaries, and metadata still render as plain text
- readers therefore get better ordering without an equally clear explanation of
  what actually matched

## Impacted Areas

- generated search-page script in `src/app/application/use_cases/build_site.py`
- deterministic reader-facing result rendering on `/search/`
- unit and integration coverage for search-result presentation behavior

## Boundary Change

The build gains no new route, artifact, or backend dependency. The boundary
change is limited to result presentation semantics inside the existing static
search page:

- `/search/` stays the canonical route
- `search.json` stays the only search artifact
- client-side rendering gains one bounded contract for visually emphasizing
  matched query text in existing result fields

## Risks

- scope could drift into snippet generation, richer styling, or broader search
  redesign rather than staying on bounded result highlighting
- highlight rendering could become unsafe or brittle if the slice relies on raw
  HTML injection rather than controlled DOM behavior
- tests could overfit exact markup details instead of meaningful highlight
  behavior

## Follow-On Pressure

- later slices may decide whether richer result treatment such as generated
  excerpts or suggestions is warranted once current-query matches are legible
- release review should verify that highlight behavior clarifies ranked results
  without changing the current static-only hosting model
