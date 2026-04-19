# Implementation: 2026-04-17 Search Navigation Bootstrap

## Summary

The shared navigation renderer now emits a stable `site-nav-link` class for
every top-level link and adds `aria-current="page"` to the active route.

## Validation

- updated unit assertions for the shared navigation contract
- updated integration assertions for generated pages and active-state behavior
