# Impact Analysis

## Summary

The next coherent slice is to give topic pages an explicit entry-row
presentation so tagged collections read like editorial navigation surfaces
instead of generic list output.

Current observed gap:

- `/library/` now presents topics as chips
- `/library/<tag>/` still renders tagged entries as plain list rows
- topic pages therefore lag behind the rest of the publication's recent
  presentation refinements

## Impacted Areas

- topic-page markup in `src/app/application/use_cases/build_site.py`
- shared embedded CSS for the bounded topic-entry row treatment
- deterministic topic-page assertions in unit and integration tests

## Boundary Change

The build gains no new route, runtime, or topic data. The boundary change is
limited to topic-page entry presentation:

- topic pages get one explicit entry-row markup contract
- topic-entry ordering, context, and destination routes remain unchanged
- library-index chips and other list surfaces remain unchanged

## Risks

- scope could drift into topic-page intro changes or taxonomy redesign instead
  of staying on entry-row presentation
- styling could accidentally affect non-topic entry rows if selectors are not
  kept bounded
- tests could overfit incidental HTML formatting instead of meaningful row
  behavior

## Follow-On Pressure

- later slices may decide whether archives or section hubs need similarly
  compact row treatment
- release review should verify that topic pages now feel consistent with the
  refined library surface without changing topic behavior
