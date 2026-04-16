# Implementation

## Scope Applied

This slice restores the minimum taxonomy surface for `blog-v2`:

- pages and episodes can declare optional `tags` in frontmatter
- the build projects a library index from discovered tags
- the build projects one static page per tag with mixed page and episode
  entries

## Boundary Notes

Tags remain optional metadata. The loader validates them only when present, and
the taxonomy projection stays separate from narrative navigation so the two
navigation modes remain inspectable and independently testable.

The in-repo content set now carries a small deterministic tag surface so
library pages can be exercised end to end without expanding into search or
manual taxonomy management.
