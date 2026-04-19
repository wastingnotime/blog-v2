# Implementation: 2026-04-18 Search Noscript Recovery Bootstrap

Implemented the noscript recovery refinement in `build_site.py`:

- replaced the plain noscript paragraphs with an explicit `search-noscript-recovery` shell
- kept the client-side search behavior unchanged for script-enabled readers
- preserved the static search route while giving no-script readers stable recovery rows

Updated deterministic unit and integration tests to verify the noscript recovery shell without widening into server-side search behavior.
