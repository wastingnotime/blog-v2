# Implementation

- kept the shared head renderer in `src/app/application/use_cases/build_site.py`
  route-aware through `project_route_robots_policy(...)`
- preserved `index,follow` for normal publication routes and
  `noindex,follow` for `404.html`
- kept the 404 recovery page on the same shared chrome and static hosting
  path as the rest of the publication
- retained the route-specific assertions already present in the site build
  tests and the scenario integration tests
