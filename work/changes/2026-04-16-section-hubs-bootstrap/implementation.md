# Implementation

## Scope Applied

This slice restores the minimum section-level orientation pages:

- `/sagas/` is now generated from the existing saga and episode projections
- each saga summary can link to a deterministic start-reading episode path
- `/studio/` is now generated as a static hub that links into `/sagas/` and
  `/library/`

## Boundary Notes

The sagas hub derives its entries from the existing content projections rather
than carrying duplicated page data. The studio hub remains intentionally simple
and static so the slice stays page-bounded instead of expanding into a full
shared layout or navigation-shell rewrite.
