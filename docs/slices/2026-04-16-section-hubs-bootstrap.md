# Slice: 2026-04-16 Section Hubs Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed content source under repository control

## Architecture Mode

Static-site builder with section-level projections and explicit hub-page
rendering:

- project a saga directory page from the existing saga catalog
- render a static studio hub page that points readers to the main navigation
  surfaces already present in the site
- keep hub pages deterministic and independent from any runtime service

## Discovery Scope

The current slices recover content loading, narrative navigation, and topic
navigation, but readers still enter the site through isolated routes rather
than through clear section hubs. The old blog exposed section-level pages such
as `/sagas/` and `/studio/` to orient browsing.

This slice restores the minimum section-hub surface needed to make the site
feel navigable as a publication instead of a loose set of generated pages:

- a sagas index page listing active sagas with a start-reading path
- a studio page that explains the broader spaces and links into `/sagas/` and
  `/library/`

This slice does not attempt full navigation chrome, shared layout parity with
the old templates, or multi-brand external-site integration beyond simple
links.

## Use-Case Contract

### `BuildSagasIndex`

Given the loaded content catalog and saga projections, generate deterministic
static output under `dist/` such that:

- `/sagas/` lists the available sagas
- each saga entry links to the saga landing page
- where possible, the page also offers a start-reading link into the first
  available episode path
- generated output contains no same-origin `/api` dependency

### `BuildStudioHub`

Given site settings and existing route surfaces, generate deterministic static
output under `dist/` such that:

- `/studio/` explains the site’s main spaces in a stable, static form
- the page links to `/sagas/` and `/library/`
- the page remains meaningful even with a small in-repo content set

## Main Business Rules

- Section hubs are orientation pages, not arbitrary marketing copy.
- The sagas index must be derived from the existing saga catalog rather than
  manually duplicated data.
- A start-reading link should point to the earliest available episode in saga
  order when one exists.
- The studio page may contain curated static copy, but its navigation links
  must target real generated routes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for content sources
- filesystem writer for build artifacts
- environment reader for site settings

## Initial Test Plan

- unit test for deterministic saga-summary projection including start-reading
  links
- integration test for generating:
  - `dist/sagas/index.html`
  - `dist/studio/index.html`
- integration test asserting generated HTML stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect the generated
site to verify:

- the sagas page lists HireFlow and links into the saga and first episode
- the studio page links readers into `/sagas/` and `/library/`
- both pages are static and traversable without an application server

## Done Criteria

- the build generates `/sagas/index.html` and `/studio/index.html`
- the sagas hub exposes deterministic saga links and a start-reading path when
  available
- the studio hub links to existing generated section routes
- deterministic tests cover projection and generated output

