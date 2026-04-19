# Implementation

- kept the shared discovery helper in `build_site.py` as
  `_render_discovery_surface(...)`
- reused the helper across archive, search, library, saga, page, and narrative
  routes to keep discovery structure consistent
- preserved route-specific destination choices while removing repeated inline
  discovery fragments
- kept the shared-discovery integration assertions aligned with the generated
  helper output
