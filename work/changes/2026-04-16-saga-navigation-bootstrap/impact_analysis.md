# Impact Analysis

## Model Pressure

The current markdown content bootstrap proves that `blog-v2` can render content
from repository-authored markdown, but it still treats saga structure too
shallowly. A saga-oriented blog needs hierarchy and movement, not only isolated
pages, otherwise the content model collapses back into a flat list with one-off
links.

## Impacted Areas

- content catalog projection from raw records into hierarchy-aware navigation
- route generation for saga and arc landing pages
- episode-page rendering for breadcrumb and adjacent navigation
- deterministic ordering rules for arc and timeline projections
- integration coverage for traversable static links

## Proposed Boundary

Keep the slice limited to structural navigation recovery:

- project existing saga, arc, and episode records into navigable pages
- compute deterministic parent and sibling navigation metadata
- render saga and arc landing pages from current in-repo content

Do not expand into taxonomy pages, search, archive views, RSS, or styling
overhaul.

## Risks

- accidentally coupling navigation ordering to incidental filesystem layout
- reintroducing route assumptions that only work behind a server
- overfitting the Python builder to the old Go template structure instead of
  the underlying narrative model

## Why This Slice Next

This is the smallest next slice that makes the current content model behave
like a saga-driven static site rather than a content loader plus a few isolated
HTML pages. It strengthens the product model directly while staying within the
GitHub Pages constraint.
