# Impact Analysis

## Impacted Areas

- content-loading rules for section-level sources
- static rendering for `library` and `studio`
- repository content structure for authored section copy
- deterministic integration coverage for section pages

## Boundary Change

The build boundary remains static and file-based, but section hubs stop being
defined exclusively by builder literals and start depending on repository-
authored markdown content.

That means the builder must now reason about:

- where section-level authored content lives
- how that content composes with existing deterministic projections
- how to keep section surfaces authored without turning every route into a
  generic page

It should still avoid:

- runtime-managed content
- open-ended section registration
- duplicating the same content both in markdown and in builder code

## Risks

- introducing a vague section-content abstraction could blur the distinction
  between standalone entries and named section hubs
- migrating copy into authored content without clear loading rules could make
  missing-section failures ambiguous
- hardcoded fallback copy and authored copy could drift if both are kept alive

## Follow-On Pressure

Once section content becomes authored, the next likely pressures move toward:

- broader migration of content from `../blog`
- richer authored metadata such as custom section summaries or labels
- release evaluation of the current static publication surface
