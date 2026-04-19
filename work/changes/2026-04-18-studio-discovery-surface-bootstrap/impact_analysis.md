# Impact Analysis

## Summary

The next coherent slice is to give the studio page an explicit discovery-row
presentation so `/studio/` reads like a publication-facing hub rather than a
generic fallback block.

Current observed gap:

- `/studio/` already exposes the right route and authored intro copy
- the page already points to sagas, library, archives, and search
- the current page still relies on the shared generic discovery block with no
  studio-specific presentation contract

## Impacted Areas

- studio-page markup in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded studio-row treatment
- deterministic studio assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or destination data. The boundary
change is limited to `/studio/` discovery presentation:

- the studio page gets one explicit studio-row shell contract
- current destination labels and routes remain unchanged
- shared discovery surfaces on other pages remain unchanged

## Risks

- scope could drift into redesigning the generic discovery component instead of
  staying on the studio page
- styling could accidentally affect non-studio surfaces if selectors are not
  kept bounded
- tests could overfit incidental HTML formatting instead of meaningful row
  behavior

## Follow-On Pressure

- later slices may decide whether the shared discovery surface itself should be
  redesigned once enough page-specific evidence exists
- release review should verify that the studio page now feels intentional
  without changing its content or links
