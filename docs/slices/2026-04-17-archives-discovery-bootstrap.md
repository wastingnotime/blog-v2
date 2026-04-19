# Slice: 2026-04-17 Archives Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic archive-hub discovery update for the expanded publication surface:

- revise the archive page so it points readers toward the current complementary
  discovery routes
- add bounded affordances for Search and Library alongside the existing
  chronological listing
- keep the slice limited to archive-page discovery copy, links, and a stable
  shell hook

## Discovery Scope

The publication now exposes stable reader-facing discovery routes for archives,
search, and library. The archive page still reflects its initial bootstrap
shape and behaves as a pure chronological listing surface.

That gap is visible in current repository artifacts:

- `build_archive_page(...)` renders only the chronological archive list
- `/archives/` is now a meaningful reader-facing route rather than a hidden
  utility surface
- search and library are stable routes with shared-navigation discoverability,
  but the archive page does not acknowledge them as alternate reading paths

This slice restores the minimum archive discovery surface needed for the
current publication:

- update the archive page so it links readers to `/search/` and `/library/`
- preserve the existing chronological listing and ordering
- expose the complementary discovery block through a stable page-shell class
- keep the change bounded to archive-page discovery copy and links

This slice does not attempt pagination, year-grouping, archive faceting, or
broader archive redesign.

## Use-Case Contract

### `BuildArchivePage`

Given site settings and the archive index, generate deterministic static output
for `/archives/` such that:

- the page continues to list entries chronologically
- readers can reach search and library directly from the archive page
- output remains fully static and compatible with GitHub Pages hosting

### `RenderArchiveDiscovery`

Given the archive route and current publication surfaces, render bounded
discovery content such that:

- the page still centers chronology as its primary job
- search and library are visibly represented as complementary discovery paths
- the section remains publication-oriented rather than turning into generic
  navigation chrome
- the discovery block uses a stable shell hook

## Main Business Rules

- Archive-page discovery copy must stay aligned with the routes the publication
  now exposes.
- Archive discovery affordances should point to stable reader-facing routes,
  not implementation artifacts.
- The slice stays bounded to archive-page copy and linking rather than changing
  archive projection or shared navigation.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing archive-page renderer
- environment reader for site settings
- existing stable routes for `/search/`, `/library/`, and `/archives/`

## Initial Test Plan

- unit test asserting the archive page links directly to `/search/` and
  `/library/`
- unit test asserting the existing chronological list remains present
- integration test asserting generated `dist/archives/index.html` exposes the
  new archive discovery affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect
`dist/archives/index.html` to verify:

- the archive page still reads like a chronology hub
- the page links directly to search and library discovery surfaces
- the existing chronological list remains unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- the archive page aligns with the current publication discovery surface
- `/archives/` exposes deterministic links to `/search/` and `/library/`
- deterministic tests cover the new archive affordances and unchanged
  static-only behavior
