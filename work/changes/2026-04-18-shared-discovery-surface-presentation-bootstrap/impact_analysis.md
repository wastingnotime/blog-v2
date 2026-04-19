# Impact Analysis

## Summary

The next coherent slice is to give the shared discovery helper an explicit row
presentation so pages that still use `Other ways in` read like the rest of the
refined publication surfaces.

Current observed gap:

- most major publication surfaces now have explicit presentation treatment
- the shared helper still renders destinations as plain paragraph lines
- the helper is now the main remaining generic surface that looks weaker than
  the rest of the publication

## Impacted Areas

- shared discovery helper markup in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded discovery-row treatment
- deterministic assertions for pages that use the shared helper

## Boundary Change

The build gains no new route, runtime, or destination data. The boundary
change is limited to the shared helper:

- the shared helper gets one explicit row-based markup contract
- existing labels, routes, and route-specific destination choices remain
  unchanged
- the studio-specific discovery surface remains unchanged

## Risks

- scope could drift into redesigning page-specific destinations instead of
  staying on shared helper presentation
- styling could accidentally affect studio or non-discovery surfaces if
  selectors are not kept bounded
- tests could overfit incidental HTML formatting instead of meaningful row
  behavior

## Follow-On Pressure

- later slices may decide whether any remaining individual pages need bespoke
  discovery surfaces instead of the shared helper
- release review should verify that the publication now has a coherent
  navigation language across both shared and page-specific surfaces
