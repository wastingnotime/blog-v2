# Implementation

- kept Open Graph rendering inside `_render_open_graph_metadata(...)` in
  `src/app/application/use_cases/build_site.py`
- continued deriving `og:title`, `og:description`, `og:type`, `og:url`,
  `og:site_name`, and `og:image` from existing page metadata and site settings
- preserved the bounded `website` type across homepage, section, page, saga,
  arc, and episode routes
- kept the behavior covered by the document-head assertions in
  `tests/unit/test_build_site.py` and
  `tests/integration/test_run_scenario.py`
