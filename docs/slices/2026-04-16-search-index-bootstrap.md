# Slice: 2026-04-16 Search Index Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Static publication metadata for client-side discovery:

- project a deterministic search index from the repository-authored content
- publish that index as `search.json` in the generated output
- keep the slice limited to build-time index generation, not interactive search
  UI

## Discovery Scope

The restored static publication now emits authored HTML routes, feed metadata,
sitemap metadata, and site identity assets. One publication-facing artifact
still present in the older `../blog` output is missing from `blog-v2`:
`search.json`.

That artifact is a good next slice because it is:

- static and deterministic
- derived from already-loaded repository content
- useful to a future client-side search surface without requiring any backend

This slice restores the minimum search publication surface needed for that
future work:

- generate a flat `search.json` file at build time
- include standalone pages plus narrative containers and episodes
- preserve stable search record shape and publication URLs

This slice does not attempt a search page, live filtering UI, indexing library
integration, or fuzzy-ranking behavior in the browser.

## Use-Case Contract

### `ProjectSearchIndex`

Given the content catalog and site settings, project search records such that:

- each searchable entry has a stable title, URL, and type
- summaries, tags, context, and dates are included when available
- records remain deterministic across builds for the same repository state

### `PublishSearchIndex`

Given the projected search records and output directory, generate static site
output such that:

- `search.json` is written into `dist/`
- URLs in the index are valid for the configured static-site base URL
- publication of the index requires no runtime service or backend API

## Main Business Rules

- The search index must be generated entirely from repository-owned content.
- The slice should remain bounded to a static JSON artifact rather than a full
  search experience.
- Search records should cover the publication surface readers navigate:
  standalone pages, sagas, arcs, and episodes.
- Context fields should help distinguish nested narrative entries without
  duplicating the full route structure in every field.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- content loader output for repository-authored content
- environment reader for site settings
- filesystem writer for static build artifacts

## Initial Test Plan

- unit test asserting deterministic projection of search records from pages,
  sagas, arcs, and episodes
- unit test asserting projected URLs use the configured static-site base URL
- integration test asserting `search.json` is emitted into `dist/`
- integration test asserting the search index remains free of same-origin
  `/api` assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- `search.json` exists in `dist/`
- the file contains records for standalone pages and narrative content
- URLs are static and valid without an application server
- existing HTML, feed, sitemap, and identity asset outputs remain intact

## Done Criteria

- the build emits a deterministic `search.json` artifact
- search records cover standalone pages plus saga, arc, and episode routes
- deterministic tests cover projection and emitted output
