# Slice: 2026-04-16 Feed Autodiscovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Machine-readable feed discovery in the shared document head:

- expose the existing `feed.xml` artifact through RSS autodiscovery metadata
- keep the metadata stable across all generated HTML pages
- preserve the current static-only publication contract

## Discovery Scope

The restored static publication now emits `feed.xml`, exposes an RSS link in
the shared chrome, and renders deterministic page metadata. One remaining
publication-facing improvement is machine-readable feed autodiscovery in the
HTML head so browsers and feed readers can discover the site feed without
parsing visible navigation.

This slice restores the minimum autodiscovery surface needed for the current
publication:

- add one `rel="alternate"` RSS feed link in the shared document head
- keep the feed URL valid under the configured static-site base URL
- render that metadata consistently across generated HTML routes

This slice does not attempt Atom feeds, per-section feeds, WebSub, or other
subscription products.

## Use-Case Contract

### `ProjectFeedAutodiscovery`

Given site settings and the existing publication metadata, project feed
autodiscovery data such that:

- the canonical target is the existing `feed.xml` artifact
- the feed title remains stable for the configured site
- the autodiscovery URL is valid for the configured static-site base URL

### `RenderFeedAutodiscovery`

Given a generated HTML document and the shared site frame, render the head
metadata such that:

- each generated HTML page includes the RSS autodiscovery link
- the visible shared navigation and active-state behavior remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- `feed.xml` remains the canonical RSS artifact.
- Feed autodiscovery must be consistent across the generated HTML surface.
- The slice stays bounded to head metadata rather than broader SEO or social
  metadata work.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- environment reader for site settings
- shared document-head renderer
- publication metadata output for the existing feed route

## Initial Test Plan

- unit test asserting generated HTML pages include an RSS autodiscovery link
- unit test asserting the autodiscovery link uses the configured static-site
  base URL and feed title
- integration test asserting homepage and representative content routes render
  the same autodiscovery metadata
- integration test asserting visible chrome behavior remains unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include RSS autodiscovery metadata
  in `<head>`
- the metadata resolves to the generated `feed.xml` artifact
- visible navigation and footer behavior remain unchanged
- the publication stays free of same-origin `/api` assumptions

## Done Criteria

- generated HTML pages expose deterministic RSS autodiscovery metadata
- the autodiscovery link points at the existing `feed.xml` output
- deterministic tests cover head metadata and unchanged visible chrome
