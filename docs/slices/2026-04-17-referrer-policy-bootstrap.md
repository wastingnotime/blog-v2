# Slice: 2026-04-17 Referrer Policy Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic referrer metadata in the shared document head:

- add one bounded referrer-policy contract to generated HTML pages
- keep the policy aligned with the current static publication model
- keep the slice limited to metadata only, without runtime security machinery

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, manifest links, Open Graph metadata, Twitter Card metadata,
shared social preview image support, theme-color, Apple mobile-web-app
metadata, and format-detection metadata. The next small browser-facing head
gap is referrer handling: generated HTML pages still omit any explicit
`referrer` policy.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders the shared document
  head without a `meta name="referrer"` tag
- the publication now has a substantial deterministic head contract, so this
  is a metadata gap rather than a missing route or asset
- the GitHub Pages deployment target keeps the site static, so the next slice
  should stay bounded to one explicit browser-facing policy literal rather than
  broader header or CDN behavior

This slice restores the minimum explicit referrer surface needed for the
current publication:

- add one shared `meta name="referrer"` tag to generated HTML pages
- keep the chosen literal deterministic across homepage, sections, pages, and
  narrative routes
- align the policy with the current static publication model without assuming
  server-controlled response headers

This slice does not attempt CSP, permissions policy, HTTP response header
management, analytics policy redesign, or per-route referrer behavior.

## Use-Case Contract

### `ProjectReferrerPolicyMetadata`

Given site settings and the current static publication model, project browser
referrer metadata such that:

- each generated HTML page exposes one deterministic referrer policy
- the chosen policy remains bounded to one literal for this bootstrap slice
- metadata remains stable across generated routes

### `RenderReferrerPolicyHead`

Given a generated HTML document and the shared head renderer, render referrer
metadata such that:

- each generated HTML page includes the bounded `meta name="referrer"` tag
- existing theme-color, mobile-web-app, manifest, and social metadata remain
  unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- Referrer metadata must be explicit and deterministic across the generated
  static publication.
- The slice stays bounded to shared HTML head metadata rather than broader
  transport or hosting policy machinery.
- The selected referrer value should remain one deterministic literal in this
  bootstrap slice.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer
- existing site settings in `SiteConfig`
- deterministic head metadata test coverage for representative route families

## Initial Test Plan

- unit test asserting generated HTML pages include the bounded
  `meta name="referrer"` tag
- unit test asserting representative route families render the same referrer
  policy value
- integration test asserting homepage and representative content routes expose
  the referrer metadata in `<head>`
- integration test asserting existing theme-color, mobile-web-app, Open Graph,
  Twitter Card, and visible chrome behavior remain unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include the bounded referrer
  metadata in `<head>`
- the chosen referrer value remains stable across generated routes
- the rest of the publication surface remains unchanged

## Done Criteria

- generated HTML routes include deterministic referrer metadata
- the selected referrer value is enforced consistently across representative
  route families
- the slice introduces no new routes, assets, or runtime dependencies
- deterministic tests cover the shared head metadata and unchanged visible
  chrome
