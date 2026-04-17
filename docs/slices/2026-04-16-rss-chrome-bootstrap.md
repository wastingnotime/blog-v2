# Slice: 2026-04-16 RSS Chrome Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Shared publication chrome with explicit feed discovery:

- expose the existing `feed.xml` artifact through the shared site navigation
- keep the link stable across all generated HTML pages
- preserve the current static-only deployment contract

## Discovery Scope

The restored static publication already emits `feed.xml`, but the current site
frame does not surface that feed anywhere in the shared chrome. The older
`../blog` output linked RSS directly from its top-level navigation on every
page, which made the feed discoverable without requiring users to guess the
artifact path.

This slice restores the minimum subscription-discovery surface needed for the
current publication:

- add one shared RSS link to the common site frame
- keep the link deterministic across homepage, section pages, pages, and saga
  routes
- ensure the link resolves correctly under the configured static-site base URL

This slice does not attempt newsletter signup, a dedicated subscriptions page,
alternate feed formats, or a larger footer redesign.

## Use-Case Contract

### `ProjectSharedFeedLink`

Given site settings and the shared navigation state, project a feed link such
that:

- the link targets the existing `feed.xml` artifact
- the URL is valid for the configured static-site base URL
- the link appears consistently across all generated HTML routes

### `RenderSharedFeedChrome`

Given a generated HTML document and the shared site frame, render the chrome
such that:

- the RSS link is visible in the shared navigation or equivalent common frame
- existing active-state behavior for Home, Sagas, Library, Studio, and About
  remains deterministic
- no same-origin `/api` dependency is introduced

## Main Business Rules

- The existing `feed.xml` output remains the canonical RSS artifact.
- Feed discovery should be consistent across the generated HTML surface.
- The slice stays bounded to shared chrome rendering, not subscription product
  design.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- environment reader for site settings
- shared navigation projection
- HTML document renderer for generated routes

## Initial Test Plan

- unit test asserting generated HTML pages include an RSS link to `feed.xml`
- unit test asserting the shared feed link uses the configured static-site base
  URL
- integration test asserting homepage and representative content routes expose
  the feed link in the generated chrome
- integration test asserting the chrome change does not alter existing active
  section behavior

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content pages include a visible RSS link
- the link resolves to the generated `feed.xml` artifact
- active navigation state remains unchanged for the existing sections
- the publication stays free of same-origin `/api` assumptions

## Done Criteria

- the shared site frame exposes `feed.xml` through a deterministic RSS link
- generated HTML routes render that link consistently
- deterministic tests cover the feed link and unchanged active navigation state
