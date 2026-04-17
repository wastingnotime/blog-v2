# Impact Analysis

## Summary

The next slice should add a deterministic `.nojekyll` artifact so the GitHub
Pages publication contract is explicit about serving the generated output as raw
static files.

Current observed gap:

- the build already emits multiple root deployment artifacts
- the GitHub Pages workflow deploys `dist/` directly
- the generated artifact set still lacks `.nojekyll`

## Impacted Areas

- static build artifact generation in `src/app/application/use_cases/build_site.py`
- scenario output under `dist/`
- deterministic tests for deployment-oriented root artifacts

## Boundary Change

The build gains one new root artifact: `.nojekyll`. No route, HTML page, or
browser-side behavior changes are required.

## Risks

- the slice could drift into workflow redesign instead of staying bounded to
  the generated artifact set
- tests could overfit incidental file contents rather than the minimal
  publication contract
- future slices could accidentally treat Jekyll as part of the runtime model if
  this artifact is not kept inside the build boundary

## Follow-On Pressure

- a later slice may decide whether other Pages-specific publication artifacts
  belong in the generated root set
- release review should verify that GitHub Pages remains an explicit static-file
  host rather than an implicit template-processing runtime
