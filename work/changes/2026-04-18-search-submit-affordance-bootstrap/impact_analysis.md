# Impact Analysis

## Summary

The next coherent slice is to give the existing search form an explicit submit
control so the route has a clearer visible search action.

Current observed gap:

- `/search/` now has explicit input, helper, status, and results semantics
- the form still relies on Enter or live input changes as the only practical
  submission path
- the page therefore keeps a weaker visible form-action contract than the rest
  of the search surface

## Impacted Areas

- generated search-page markup in `src/app/application/use_cases/build_site.py`
- deterministic reader-facing search-form semantics on `/search/`
- unit and integration coverage for search-form markup

## Boundary Change

The build gains no new route, artifact, or backend dependency. The boundary
change is limited to form affordance inside the existing static search page:

- `/search/` stays the canonical route
- `search.json` stays the only search artifact
- page markup gains one bounded submit-control contract for the existing search
  form

## Risks

- scope could drift into broader form-layout redesign rather than staying on
  bounded submit affordance
- tests could overfit exact button text instead of the meaningful presence of an
  explicit submit control

## Follow-On Pressure

- later slices may decide whether the search form needs additional affordances
  once the current submit path is explicit
- release review should verify that the new submit control clarifies the current
  search form without changing the static-only hosting model
