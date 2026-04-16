# Slice: 2026-04-16 Markdown Content Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed content source under repository control

## Architecture Mode

Static-site builder with explicit content-loading and projection steps:

- load markdown source files plus YAML frontmatter
- map source documents into typed content records
- project those records into static routes and homepage summaries

## Discovery Scope

This slice restores the smallest real blog surface from `../blog` that proves
the repository can behave like a static content site instead of a placeholder:

- one homepage driven by content
- one standalone page
- one saga episode route

This slice does not attempt full parity with the old repository.

## Use-Case Contract

### `BuildStaticSiteFromMarkdown`

Given repository-authored markdown files and site settings, generate
deterministic static output under `dist/` such that:

- the homepage includes a recent-content list derived from markdown sources
- a standalone page route renders markdown body content
- a saga episode route renders markdown body content and metadata
- generated links remain compatible with static hosting
- generated output contains no same-origin `/api` dependency

### `LoadContentCatalog`

Given a content root, load a bounded set of markdown documents with frontmatter
into typed records for:

- page
- saga
- episode

The loader should reject or surface invalid inputs deterministically rather than
silently skipping malformed content.

## Main Business Rules

- Content is authored in repository markdown files, not fetched from a runtime
  service.
- Homepage ordering should be deterministic and based on content metadata.
- Standalone pages and saga episodes must have stable static permalinks.
- The slice should preserve the distinction between generic pages and saga
  narrative entries.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for content sources
- filesystem writer for build artifacts
- environment reader for site settings

## Proposed Source Shape

The build should target a source layout close to the existing blog language,
while still allowing future simplification if needed:

```text
content/
  pages/
    about.md
  sagas/
    hireflow/
      index.md
      the-origin-blueprint/
        the-first-brick.md
```

## Initial Test Plan

- unit test for markdown frontmatter parsing into typed content records
- unit test for homepage projection ordering from content metadata
- integration test for generating:
  - `dist/index.html`
  - `dist/about/index.html`
  - `dist/sagas/hireflow/the-origin-blueprint/the-first-brick/index.html`
- integration test asserting generated HTML stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against a small in-repo content set and inspect the
generated site to verify:

- homepage shows recent content entries
- about page renders markdown body
- episode page renders markdown body and metadata
- links are static and traversable without an application server

## Done Criteria

- repository contains a bounded markdown content set used by the builder
- the builder loads frontmatter plus markdown body deterministically
- homepage output reflects recent content instead of only placeholder text
- one standalone page and one episode route are generated successfully
- tests cover content loading and output generation
