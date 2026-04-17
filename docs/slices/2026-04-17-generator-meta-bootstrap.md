# Slice: 2026-04-17 Generator Meta Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic generator metadata in the shared document head:

- add one bounded `generator` contract to generated HTML pages
- align that metadata with the repository-owned static build model
- keep the slice limited to metadata only, without changing visible chrome

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, manifest links, Open Graph metadata, Twitter Card metadata,
shared social preview image support, theme-color, Apple mobile-web-app
metadata, format-detection metadata, referrer metadata, color-scheme
metadata, application-name metadata, viewport-fit metadata, Windows tile color
metadata, and shared author metadata. The next small browser-facing head gap is
build provenance signaling: generated HTML pages still omit
`meta name="generator"` even though the site is deterministically emitted by a
repository-owned Python builder.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders the shared document
  head without `meta name="generator"`
- the publication already has a strong shared head contract, so this is now a
  small build-identity metadata gap rather than a route or content-model gap
- the GitHub Pages deployment target keeps the site static, so the next slice
  should stay bounded to one deterministic generator literal instead of broader
  provenance or deployment reporting

This slice restores the minimum explicit generator surface needed for the
current publication:

- add one shared `meta name="generator"` tag to generated HTML pages
- keep the chosen value deterministic across homepage, sections, pages, and
- narrative routes
- align the value with the repository-owned static build model

This slice does not attempt visible badges, deployment version stamps, commit
hashes, JSON-LD publisher metadata, or runtime diagnostics.

## Use-Case Contract

### `ProjectGeneratorMetadata`

Given the current static publication model, project browser generator metadata
such that:

- each generated HTML page exposes one deterministic generator value
- the value remains shared across routes in this bootstrap slice
- metadata stays aligned with the existing repository-owned build contract

### `RenderGeneratorHead`

Given a generated HTML document and the shared head renderer, render generator
metadata such that:

- each generated HTML page includes the bounded `meta name="generator"` tag
- existing viewport, author, application-name, color-scheme, referrer,
  theme-color, mobile-web-app, manifest, and social metadata remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- Generator metadata must be explicit and deterministic across the generated
  static publication.
- The slice stays bounded to shared HTML head metadata rather than visible
  authorship or deployment reporting.
- The selected value should reflect the current repository-owned static build
  model rather than ad hoc route content.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer
- existing repository-owned build identity in `build_site.py`
- deterministic head metadata test coverage for representative route families

## Initial Test Plan

- unit test asserting generated HTML pages include the bounded
  `meta name="generator"` tag
- unit test asserting representative route families render the same generator
  value
- integration test asserting homepage and representative content routes expose
  the generator metadata in `<head>`
- integration test asserting existing viewport, author, application-name,
  color-scheme, referrer, theme-color, mobile-web-app, Open Graph, Twitter
  Card, and visible chrome behavior remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include the bounded generator
  metadata in `<head>`
- the value remains stable across generated routes
- the rest of the publication surface remains unchanged

## Done Criteria

- generated HTML routes include deterministic `generator` metadata
- the selected value is enforced consistently across representative route
  families
- the slice introduces no new routes, assets, or runtime dependencies
- deterministic tests cover the shared head metadata and unchanged visible
  chrome
