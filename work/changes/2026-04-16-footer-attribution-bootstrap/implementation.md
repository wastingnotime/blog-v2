# Implementation

## Summary

Implemented deterministic shared footer attribution by projecting footer copy
from site settings and repository content dates, then rendering that footer
across generated HTML pages.

## Main Changes

- added `project_footer_attribution` to compute:
  - a deterministic publication year from the latest repository content date
  - the site name from the configured base URL
  - stable attribution copy for the shared frame
- extended the content model with `FooterAttribution`
- updated `build_site.py` to render the shared footer on homepage, section
  pages, standalone pages, and narrative routes
- added unit and integration coverage for:
  - deterministic footer attribution projection
  - shared footer rendering across representative routes
  - unchanged shared navigation behavior

## Validation

- `PYTHONPATH=. python3 -m pytest`
- `PYTHONPATH=. python3 -m src.app.interfaces.cli.run_scenario`
