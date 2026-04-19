# Impact Analysis

## Summary

The next coherent slice is to make breadcrumb treatment consistent across arc,
topic, and episode routes by moving the remaining plain breadcrumb links onto
the shared breadcrumb presentation contract.

Current observed gap:

- episode pages already use explicit breadcrumb hooks
- arc and topic pages still render breadcrumbs as plain inline links
- the publication therefore presents route navigation inconsistently across
  otherwise similar reading surfaces

## Impacted Areas

- generated arc-page markup in `src/app/application/use_cases/build_site.py`
- generated topic-page markup in `src/app/application/use_cases/build_site.py`
- deterministic arc and topic assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or breadcrumb destination. The boundary
change is limited to breadcrumb presentation on arc and topic routes:

- breadcrumb links get the shared explicit crumb hooks
- current breadcrumb destinations and labels remain unchanged
- discovery surfaces and page content remain unchanged

## Risks

- scope could drift into changing breadcrumb depth instead of staying on
  presentation
- tests could overfit exact inline markup instead of meaningful breadcrumb
  contracts
- arc and topic routes could diverge if the shared breadcrumb treatment is not
  applied consistently

## Follow-On Pressure

- later slices may decide whether saga index or other route-local metadata needs
  richer navigation framing after breadcrumb treatment is consistent
- release review should verify that breadcrumb handling now feels uniform across
  the publication
