# Slice: 2026-04-17 Archives Sitemap Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic sitemap projection for the durable archives route:

- include one bounded `/archives/` entry in generated `sitemap.xml`
- derive its `lastmod` value from the same publication chronology already
  projected for the archive page and feed
- keep the slice limited to sitemap completeness rather than broader SEO or
  crawl-policy redesign

## Discovery Scope

The publication now exposes `/archives/` as a first-class reader-facing route:

- shared navigation links to `/archives/`
- homepage and other generated routes surface archives as a complementary path
- the archive page itself renders a chronological view across published pages
  and saga episodes

One route-inventory mismatch remains visible in the current repository state:

- `project_publication_metadata(...)` emits sitemap entries for `/`,
  `/library/`, `/sagas/`, `/studio/`, content pages, sagas, arcs, episodes,
  and topic pages
- the same projection omits `/archives/` even though the route is now a stable
  publication surface rather than a transient utility page
- generated `sitemap.xml` therefore under-represents the current static route
  set

This slice restores the minimum sitemap completeness needed for the current
static publication:

- add one deterministic `/archives/` sitemap entry
- project its `lastmod` from the same content chronology already used to build
  archive ordering
- preserve the current omission of utility routes such as `/search/`, whose
  `noindex,follow` contract is already explicit

This slice does not attempt sitemap priorities, change frequencies, image
extensions, environment-specific SEO configuration, or broader route-taxonomy
changes.

## Use-Case Contract

### `ProjectPublicationMetadata`

Given the content catalog and current route inventory, project sitemap metadata
such that:

- `/archives/` appears as one deterministic sitemap entry
- its `lastmod` reflects the latest published content date represented by the
  archive surface
- existing sitemap entries for durable reading routes remain unchanged

### `BuildSitemap`

Given projected publication metadata and the static build contract, render
`sitemap.xml` such that:

- the archive route is discoverable as a durable publication page
- utility routes that should not be indexed remain outside the sitemap
- output stays fully static and compatible with GitHub Pages hosting

## Main Business Rules

- The sitemap should represent durable reader-facing publication routes, not
  only authored content leaf pages.
- `/archives/` is part of the publication’s durable route inventory and should
  therefore appear in the sitemap.
- `/archives/` `lastmod` should derive from the latest dated published content
  already visible in the archive chronology.
- Utility routes whose crawl policy is intentionally limited, such as
  `/search/`, remain out of scope for this slice.
- The sitemap must remain deterministic for the same repository state.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- sitemap metadata projection in
  `src/app/application/use_cases/project_publication_metadata.py`
- existing archive chronology inputs derived from published page and episode
  dates
- sitemap rendering in `src/app/application/use_cases/build_site.py`

## Initial Test Plan

- unit test asserting projected sitemap metadata includes `/archives/`
- unit test asserting the archive sitemap entry uses the latest published
  content date as `lastmod`
- integration test asserting generated `dist/sitemap.xml` includes
  `https://wastingnotime.org/archives/`
- integration test asserting `/search/` remains absent from the sitemap so the
  current `noindex` utility-route distinction is preserved

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- `dist/sitemap.xml` contains `https://wastingnotime.org/archives/`
- the archive sitemap entry carries the latest published content date available
  in the repository
- existing homepage, library, saga, topic, and content entries remain present
- `/search/` remains absent from the sitemap
- the output remains fully static and compatible with GitHub Pages hosting

## Done Criteria

- generated `sitemap.xml` includes one deterministic `/archives/` entry
- the archive sitemap entry’s `lastmod` stays aligned with the publication’s
  latest dated content
- utility routes such as `/search/` remain outside the sitemap
- deterministic tests cover both sitemap projection and generated output
