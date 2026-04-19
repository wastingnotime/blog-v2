# Impact Analysis

## Summary

The next coherent slice is to give the static 404 page an explicit recovery-row
presentation so `404.html` reads like an intentional recovery surface rather
than a generic unordered list.

Current observed gap:

- `404.html` already has the right route and recovery destinations
- the page still renders those destinations as a plain list
- recent navigation refinements across the publication make the 404 page the
  next obvious lagging recovery surface

## Impacted Areas

- 404-page markup in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded recovery-row treatment
- deterministic 404 assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or recovery data. The boundary change is
limited to `404.html` presentation:

- the 404 page gets one explicit recovery-row markup contract
- current labels, routes, and robots behavior remain unchanged
- other navigation surfaces remain unchanged

## Risks

- scope could drift into redirect behavior or search-product recovery instead
  of staying on presentation
- styling could accidentally affect other list surfaces if selectors are not
  kept bounded
- tests could overfit incidental HTML formatting instead of meaningful row
  behavior

## Follow-On Pressure

- later slices may decide whether search or not-found recovery needs richer
  assistance once the current recovery surface is explicit
- release review should verify that the 404 page now feels consistent with the
  rest of the refined publication without changing its recovery contract
