# Impact Analysis

## Model Pressure

The current slice proves deployment shape but not the product model. Until the
repository can ingest authored content and emit meaningful routes, `blog-v2`
cannot validate whether the chosen Python static-site path fits the actual blog
domain.

## Impacted Areas

- content source layout under repository control
- markdown frontmatter parsing
- permalink and route generation
- homepage projection rules for recent content
- deterministic builder tests

## Proposed Boundary

Keep the slice limited to the minimum content surface needed to recover the blog
model:

- markdown-backed source files
- homepage projection of recent posts
- one standalone page route
- one saga episode route

Do not yet migrate all old sections, tags, arc navigation, RSS, or asset
pipelines.

## Risks

- overfitting the Python builder to old Go structures too early
- inventing too much taxonomy before the first real content slice proves useful
- coupling route generation to assumptions that break when content migration
  expands

## Why This Slice Next

This slice is the first one that exercises the actual product model while still
honoring the static GitHub Pages constraint. It is a stronger test of the
chosen direction than adding more deployment or styling work.
