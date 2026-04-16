# Impact Analysis

## Model Pressure

`blog-v2` now has meaningful content routes, hierarchy, and taxonomy, but it
still lacks the section-level entry points that make those routes legible as a
publication. Without section hubs, the site remains navigable only if the user
already knows specific content URLs or starts from the homepage.

## Impacted Areas

- projection of saga summaries and first-entry links from existing saga data
- route generation for `/sagas/` and `/studio/`
- integration coverage for section-level navigation surfaces
- homepage or section cross-link consistency where relevant

## Proposed Boundary

Keep the slice limited to top-level orientation pages:

- build a sagas index from existing saga and episode projections
- build a studio hub with static explanatory copy and links into generated
  sections

Do not expand into a full shared navigation shell, visual redesign, or dynamic
site map generation.

## Risks

- duplicating saga metadata manually instead of deriving it from the content
  catalog
- allowing hub pages to become copy-heavy placeholders with weak navigation
  value
- expanding the slice into global layout work instead of keeping it page-bounded

## Why This Slice Next

This is the smallest next slice that improves orientation at the site level.
It makes the recovered content surfaces easier to enter and browse without
adding runtime complexity or broad presentation refactors.
