# Impact Analysis

## Summary

The next coherent slice is to give the existing search input an explicit label
and stable hook so the static search form is clearer and less dependent on
placeholder text.

Current observed gap:

- `/search/` now has a stable route, query contract, ranking, highlighting, and
  multiple recovery paths
- the search input still uses placeholder text as its only visible descriptor
- the page therefore keeps a weaker form contract than the rest of the search
  surface and lacks a stable label/input hook pair

## Impacted Areas

- generated search-page markup in `src/app/application/use_cases/build_site.py`
- deterministic reader-facing form semantics on `/search/`
- unit and integration coverage for search-form markup

## Boundary Change

The build gains no new route, artifact, or backend dependency. The boundary
change is limited to form semantics inside the existing static search page:

- `/search/` stays the canonical route
- `search.json` stays the only search artifact
- page markup gains one bounded label contract for the existing search input

## Risks

- scope could drift into broader form-layout or accessibility redesign rather
  than staying on bounded input labeling
- tests could overfit exact label prose instead of the meaningful association
  between label and input

## Follow-On Pressure

- later slices may decide whether the search page needs additional accessibility
  affordances once the current input semantics are explicit
- release review should verify that the new label clarifies the current search
  form without changing the static-only hosting model
