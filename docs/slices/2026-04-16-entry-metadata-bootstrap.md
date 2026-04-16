# Slice: 2026-04-16 Entry Metadata Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed content source under repository control

## Architecture Mode

Static-site builder with reader-facing metadata projections for content entries:

- project display metadata for standalone pages and saga episodes
- derive lightweight reading-time estimates from repository-authored markdown
- render tag context directly on entry pages without runtime lookups

## Discovery Scope

The current slices restore routes, navigation, homepage framing, and machine-
readable publication metadata, but individual content pages still expose only
minimal metadata. The old `../blog` post surface carried more reader-oriented
context: publication date, reading time, and tags on the entry itself.

This slice restores the minimum entry-level metadata needed to make pages and
episodes read like publication artifacts instead of raw markdown renderings:

- show tag metadata directly on standalone pages and episode pages
- derive and display a deterministic reading-time estimate
- keep metadata rendering consistent with the existing static route model

This slice does not attempt author bios, comments, reactions, series-wide
recommendations, or visual redesign beyond the metadata strip itself.

## Use-Case Contract

### `ProjectEntryMetadata`

Given a page or episode record and its markdown body, compute deterministic
display metadata for:

- publication date
- optional tags already authored in frontmatter
- derived reading-time estimate based on repository text content

### `RenderEntryMetadata`

Given projected entry metadata and site settings, generate deterministic static
HTML for page and episode routes such that:

- metadata appears near the top of the entry page
- tags link back to existing library topic routes when applicable
- rendered metadata requires no runtime service or content lookup
- generated output remains compatible with GitHub Pages hosting

## Main Business Rules

- Reading time must be derived deterministically from repository-authored
  content, not external services or browser runtime code.
- Tags shown on entry pages must come from existing frontmatter and link to real
  generated `/library/<tag>/` routes.
- Metadata rendering should degrade cleanly when a page or episode has no tags.
- Episode pages must preserve existing narrative context while adding entry
  metadata rather than replacing it.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for content sources
- filesystem writer for build artifacts
- environment reader for site settings

## Initial Test Plan

- unit test for deterministic reading-time projection from markdown body
- unit test for entry metadata projection with and without tags
- integration test asserting page and episode routes render:
  - reading-time metadata
  - tag links to `/library/<tag>/`
- integration test asserting generated HTML stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
entry pages to verify:

- standalone pages show publication date, reading time, and tags when present
- episode pages show reading time and tag links alongside existing saga context
- tag links point to real library topic pages
- entry pages remain fully static and traversable without an application server

## Done Criteria

- page and episode routes expose reader-facing metadata near the top of the
  content
- reading time is derived deterministically from repository-authored markdown
- tag metadata links back into existing library routes
- deterministic tests cover metadata projection and generated output
