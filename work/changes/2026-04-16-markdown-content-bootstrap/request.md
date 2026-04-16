# Request

## Summary

After the gh-pages reset bootstrap, `blog-v2` still lacks the core behavior of a
blog: loading authored content from the repository and rendering more than a
placeholder homepage.

The next slice should restore a minimal static-content flow from `../blog`
without reintroducing AWS or `/api` assumptions.

## Source Evidence

- `../blog/content/about/index.md` shows a content page backed by markdown
  frontmatter.
- `../blog/content/sagas/hireflow/index.md` shows a saga index backed by
  markdown frontmatter.
- `../blog/content/sagas/hireflow/the-origin-blueprint/the-first-brick.md`
  shows an episode backed by markdown frontmatter and body content.
- `../blog/templates/home.gohtml` shows the homepage surfacing recent posts and
  sagas rather than only a static hero section.
- `../blog/internal/site/page.go` and `../blog/internal/site/loader.go` show
  the old repository's minimum content-loading model.

## Requested Outcome

Define one bounded slice that introduces repository-authored markdown content
and renders a small but real static site surface:

- homepage with recent content
- one standalone page
- one saga/episode path

All of that must remain compatible with pure static GitHub Pages hosting.
