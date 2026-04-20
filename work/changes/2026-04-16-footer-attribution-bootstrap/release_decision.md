# Release Decision

## Decision

Accepted as the internal released version.

## Scope Reviewed

- shared footer attribution projection
- shared footer rendering across generated pages
- local-dev host normalization for footer identity

## Evidence

- `python3 -m pytest tests/unit/test_project_footer_attribution.py tests/unit/test_build_site.py tests/integration/test_run_scenario.py -q`
- `python3 -m pytest -q`
- `71 passed`

## Assessment

The footer contract is deterministic and now renders the intended brand copy:
`© 2026 wastingnotime.org — built with custom python static renderer`.

The change is bounded to footer attribution and local host normalization. It
does not introduce new routes, new runtime dependencies, or layout regressions.

## Residual Risk

- The footer year is derived from build-time attribution logic and should be
  revisited only if the publication model changes materially.
- Local development hosts are normalized to the brand name, which is intended
  for this repository but should be kept explicit if the base URL strategy
  changes later.
