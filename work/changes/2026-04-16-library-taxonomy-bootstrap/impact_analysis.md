# Impact Analysis

## Model Pressure

`blog-v2` can now render content and narrative hierarchy, but it still lacks a
topic-oriented navigation surface. That leaves the model biased toward saga
structure and chronology, while the old blog also treated ideas and themes as a
first-class browsing path through the library and tag pages.

## Impacted Areas

- markdown frontmatter loading for optional tag metadata
- content models for tagged pages and episodes
- taxonomy projection from tagged entries into a topic catalog
- route generation for `/library/` and `/library/<tag>/`
- integration coverage for static topic navigation

## Proposed Boundary

Keep the slice limited to the minimum taxonomy recovery:

- load optional tags from current markdown content
- build a library index page from the discovered tag set
- build tag pages from tagged standalone pages and episodes

Do not expand into full-text search, archive views, manual curation tools, or
cross-repository topic aggregation.

## Risks

- overfitting tag behavior to the old templates instead of the current content
  model
- treating tags as mandatory when they should remain optional metadata
- introducing projection rules that become unstable as content volume grows

## Why This Slice Next

This is the smallest next slice that restores a second meaningful navigation
mode for the site. It improves discoverability without adding runtime
complexity, and it builds directly on metadata already present in the old blog
source material.
