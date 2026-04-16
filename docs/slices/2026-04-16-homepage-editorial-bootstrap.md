# Slice: 2026-04-16 Homepage Editorial Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed content source under repository control

## Architecture Mode

Static-site builder with homepage-specific editorial projections:

- project a bounded recent-content rail for the root route
- project active saga summaries with reading status metadata
- render the homepage as publication-oriented content instead of migration
  status copy

## Discovery Scope

The current slices restore content routes, section hubs, and shared navigation,
but the homepage still behaves like a bootstrap status page. The old `../blog`
homepage exposed the site as an editorial surface: a short publication intro,
recent writing, and active saga summaries with lightweight status context.

This slice restores the minimum homepage behavior needed for `blog-v2` to read
like a publication rather than a build artifact:

- replace deployment-focused homepage copy with editorial framing
- limit the homepage recent rail to a deterministic bounded set
- show active saga summaries with episode count and most recent release date

This slice does not attempt full visual parity with the old templates, hero
artwork, search, archives, newsletter capture, or multi-column design work.

## Use-Case Contract

### `BuildEditorialHomepage`

Given site settings, the content catalog, and saga navigation projections,
generate deterministic static output for `/` such that:

- the homepage opens with publication-oriented intro copy
- the homepage lists a bounded set of recent content entries
- the homepage lists active sagas with stable summary metadata
- generated links remain compatible with static hosting
- generated output contains no same-origin `/api` dependency

### `ProjectHomepageSurface`

Given pages, episodes, sagas, and arc views, compute deterministic homepage
sections for:

- recent content ordered by recency and bounded by an explicit limit
- saga summaries including permalink, summary, episode count, status, and last
  release date when available
- stable empty-state behavior if content remains small

## Main Business Rules

- The homepage should describe the publication, not the deployment mechanics.
- Recent-content ordering must be deterministic and repository-derived.
- The homepage should expose only a bounded recent set rather than dumping the
  full catalog onto `/`.
- Saga summaries must be derived from the existing saga and episode catalog,
  not maintained as duplicate handwritten metadata.
- Saga status context may include episode count and most recent release date
  when those values can be projected deterministically.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for content sources
- filesystem writer for build artifacts
- environment reader for site settings

## Initial Test Plan

- unit test for homepage recent-content projection with deterministic limiting
- unit test for saga-summary projection including episode count and last
  release date
- integration test asserting the generated homepage no longer renders the
  deployment-target status card
- integration test asserting the homepage includes editorial intro copy, bounded
  recent entries, and saga status summaries
- integration test asserting generated HTML stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect `dist/index.html`
to verify:

- the homepage reads like a publication landing page rather than an
  implementation status page
- recent entries are limited and linked in deterministic order
- the HireFlow saga summary exposes episode count, latest release context, and
  a route into the saga section
- the page remains fully static and traversable without an application server

## Done Criteria

- `/` presents editorial intro copy instead of deployment-status copy
- the homepage recent rail is bounded deterministically
- saga summaries include projected status metadata from real content
- deterministic tests cover homepage projection and generated output
