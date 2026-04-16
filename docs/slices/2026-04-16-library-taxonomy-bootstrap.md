# Slice: 2026-04-16 Library Taxonomy Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed content source under repository control

## Architecture Mode

Static-site builder with taxonomy-aware projections from the content catalog:

- load optional tag metadata from repository markdown frontmatter
- project a deterministic library index from the tag set present in content
- project one static page per tag with linked entries

## Discovery Scope

The current slices restore authored content, saga navigation, and episode
movement, but they still leave the site too dependent on chronology and saga
structure. The old blog exposed another important navigation mode: topic
discovery through a library index and per-tag pages.

This slice restores the minimum taxonomy surface needed to browse the site by
idea rather than only by saga or date:

- a library landing page listing available tags
- one tag page showing matching pages and episodes
- deterministic tag loading from markdown frontmatter

This slice does not attempt full search, archives, RSS, or tag curation beyond
repository-authored metadata.

## Use-Case Contract

### `BuildLibraryIndex`

Given the loaded content catalog and site settings, generate deterministic
static output under `dist/` such that:

- `/library/` lists the available tags derived from repository content
- tags are ordered deterministically
- generated links remain compatible with static hosting
- generated output contains no same-origin `/api` dependency

### `BuildTagPages`

Given tagged pages and episodes, generate one static page per tag such that:

- each tag page lists matching content entries with stable links
- entries preserve enough context to distinguish standalone pages from saga
  episodes
- empty tag pages are not emitted

### `ProjectTopicCatalog`

Given repository markdown records with optional `tags` metadata, compute a
deterministic topic catalog for:

- the library index
- per-tag entry lists
- stable ordering of tag entries by content metadata

## Main Business Rules

- Topic browsing is derived from repository-authored metadata, not a runtime
  service or search backend.
- Tags remain optional on content records, but when present they must be loaded
  deterministically.
- Tag pages must mix standalone pages and saga episodes without flattening away
  their content type.
- Library output must degrade cleanly when the tagged content set is small.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for content sources
- filesystem writer for build artifacts
- environment reader for site settings

## Initial Test Plan

- unit test for loading optional `tags` frontmatter into typed content records
- unit test for deterministic library projection from tagged content
- integration test for generating:
  - `dist/library/index.html`
  - at least one `dist/library/<tag>/index.html`
- integration test asserting generated HTML stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
site to verify:

- the library page lists available topics
- a tag page lists matching entries with working static links
- saga episodes and standalone pages can both participate in the same topic
  view
- links are static and traversable without an application server

## Done Criteria

- repository content can declare optional tags in frontmatter
- the build generates a library index and at least one tag page successfully
- tag pages show deterministic linked entries with content-type context
- deterministic tests cover taxonomy loading and generated output

