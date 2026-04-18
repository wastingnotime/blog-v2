# Impact Analysis

## Summary

The next coherent slice is to recover the original publication's shared visual
language through the existing document renderer rather than continuing to add
features on top of a generic shell.

Current observed gap:

- `blog-v2` now has working static routes, discovery surfaces, and search
  affordances
- the shared renderer still emits a light serif shell that breaks continuity
  with `../blog`
- the predecessor's strongest stable style signals are shared-shell concerns,
  so the next slice should land at that boundary rather than page by page

## Impacted Areas

- shared page-shell markup and embedded CSS in
  `src/app/application/use_cases/build_site.py`
- homepage and content-page visual continuity through the existing shared
  renderer
- deterministic unit and integration coverage for generated page shell output

## Boundary Change

The build gains no new route, backend, or asset pipeline. The boundary change
is limited to site-wide styling emitted from the existing renderer:

- shared CSS tokens move from a light-paper shell to a dark editorial shell
- typography, links, metadata, borders, and prose surfaces shift at the shared
  renderer level
- all existing page routes continue to render through the same static builder

## Risks

- scope could drift into homepage layout redesign or navigation restructuring
  instead of staying on the shared shell
- the implementation could overfit to old template mechanics rather than
  extracting portable style signals
- tests could become brittle if they assert too much exact CSS instead of the
  meaningful shell contract

## Follow-On Pressure

- later slices may restore homepage-specific tone and section presentation once
  the shared shell is back in place
- release review should verify that the recovered shell feels continuous with
  `../blog` without reintroducing runtime styling dependencies
