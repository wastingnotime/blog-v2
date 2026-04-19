# Implementation: 2026-04-18 Saga Navigation Presentation Bootstrap

Implemented the saga-navigation refinement in `build_site.py`:

- added explicit row shells for saga arc rows, saga timeline rows, and arc episode rows
- kept the existing chronology, counts, labels, routes, and discovery links unchanged
- preserved the saga and arc routes as static navigation surfaces with no new runtime dependency

Updated deterministic unit and integration tests to verify the saga-only row shells without widening into chronology or information-architecture changes.
