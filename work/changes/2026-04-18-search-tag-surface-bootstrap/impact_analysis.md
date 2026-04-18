# Impact Analysis

## Summary

The next coherent slice is to surface tags inside the existing static search
results so tag-based matches are visible rather than implicit.

Current observed gap:

- `/search/` now ranks and highlights matches across title, context, summary,
  and tags
- tags still do not render in the result surface
- a tag-only match can therefore influence search behavior without any visible
  explanation for the reader

## Impacted Areas

- generated search-page script in `src/app/application/use_cases/build_site.py`
- deterministic reader-facing result rendering on `/search/`
- unit and integration coverage for search-result tag presentation

## Boundary Change

The build gains no new route, artifact, or backend dependency. The boundary
change is limited to result-context rendering inside the existing static search
page:

- `/search/` stays the canonical route
- `search.json` stays the only search artifact
- client-side rendering gains one bounded contract for surfacing existing record
  tags as secondary result context

## Risks

- scope could drift into clickable tag navigation, taxonomy redesign, or search
  faceting rather than staying on bounded tag presentation
- result cards could become visually noisy if the slice does not keep tags
  clearly secondary to title and summary content
- tests could overfit exact markup details instead of meaningful tag-surface
  behavior

## Follow-On Pressure

- later slices may decide whether tags from search results should become
  clickable discovery affordances once simple surfacing is in place
- release review should verify that tag visibility improves result legibility
  without changing the current static-only hosting model
