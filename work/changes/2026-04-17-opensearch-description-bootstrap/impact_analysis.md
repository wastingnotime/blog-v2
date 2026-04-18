# Impact Analysis

## Summary

The next slice should add bounded browser-search autodiscovery so the generated
static publication exposes a machine-readable search contract beyond the
reader-facing `/search/` page and homepage `SearchAction`.

Current observed gap:

- the site now has `search.json`, `/search/`, and a stable `?q=` URL contract
- generated output still omits an OpenSearch description artifact
- shared HTML heads do not advertise browser-search autodiscovery metadata

## Impacted Areas

- root-level static artifact generation in
  `src/app/application/use_cases/build_site.py`
- shared document-head rendering in
  `src/app/application/use_cases/build_site.py`
- deterministic test coverage for representative head metadata and generated
  root artifacts

## Boundary Change

The build gains one new root-level static artifact plus one new shared head
link relation. The boundary change stays limited to browser-search discovery
metadata and does not change search results, query handling, or route
inventory.

## Risks

- scope could drift into search UX or browser-specific behavior instead of
  staying bounded to autodiscovery metadata
- tests could overfit exact XML formatting rather than the published search
  contract
- the OpenSearch template could drift from the existing `/search/?q=` behavior
  if it stops deriving from the same bounded route contract

## Follow-On Pressure

- a later slice may revisit whether any additional machine-readable search
  contracts are justified beyond OpenSearch and JSON-LD
- release review should verify that browser-search autodiscovery remains aligned
  with the same static search route the site already exposes to readers
