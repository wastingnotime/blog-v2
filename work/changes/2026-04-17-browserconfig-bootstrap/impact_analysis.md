# Impact Analysis

## Summary

The next slice should add a bounded Windows browserconfig contract so the
generated static publication completes the platform-facing metadata surface
already implied by `msapplication-TileColor`.

Current observed gap:

- generated pages now include `msapplication-TileColor`
- the shared head still omits `meta name="msapplication-config"`
- the generated root artifact set still lacks `browserconfig.xml`
- the publication already ships stable icon assets and a shared tile color, so
  the next gap is an explicit XML metadata artifact rather than a new asset set
- no handwritten browserconfig source exists in the repository, so the
  artifact should stay owned by deterministic build logic

## Impacted Areas

- shared document-head rendering in `src/app/application/use_cases/build_site.py`
- root-artifact generation in `src/app/application/use_cases/build_site.py`
- deterministic test coverage for both root artifacts and representative head
  metadata

## Boundary Change

The build gains one new root artifact: `browserconfig.xml`. The only HTML
boundary change is one additional shared head tag linking to that artifact.
No new route family, authored content source, or runtime dependency is needed.

## Risks

- scope could drift into new pinned-site assets or broader platform-specific
  behavior instead of staying bounded to the XML contract
- tests could overfit exact XML formatting rather than the selected metadata
  content
- browserconfig values could drift from the existing shared theme color and
  icon surface if they are not projected from the same identity inputs

## Follow-On Pressure

- a later slice may revisit whether richer machine-readable publication
  semantics such as JSON-LD are justified
- release review should verify that browserconfig remains aligned with the
  existing Windows tile color and published icon assets
