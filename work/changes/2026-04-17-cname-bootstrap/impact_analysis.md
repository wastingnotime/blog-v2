# Impact Analysis

## Summary

The next slice should add a deterministic `CNAME` artifact so the generated
GitHub Pages output matches the repository's configured custom-domain target.

Current observed gap:

- the build defaults to `https://wastingnotime.org/`
- the GitHub Pages workflow publishes `dist/` directly
- the generated artifact set still lacks a root `CNAME`

## Impacted Areas

- static build artifact generation in `src/app/application/use_cases/build_site.py`
- scenario and integration output under `dist/`
- deterministic tests for deployment-oriented root artifacts

## Boundary Change

The build gains one new root artifact: `CNAME`. No route, HTML page, or browser
behavior changes are required.

## Risks

- deriving the host incorrectly from `SITE_BASE_URL` could emit an invalid
  artifact
- scope could drift into broader deployment automation instead of staying
  bounded to the build output
- tests could accidentally lock in path or scheme formatting rather than the
  host-only contract GitHub Pages expects

## Follow-On Pressure

- a later slice may decide how non-custom-domain or preview environments should
  suppress or vary the `CNAME` artifact
- release review should verify that the deployment artifact remains aligned with
  the configured base URL whenever publication settings change
