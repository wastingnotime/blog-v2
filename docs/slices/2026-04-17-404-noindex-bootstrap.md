# Slice: 2026-04-17 404 Noindex Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic route-specific crawl metadata for the static publication:

- keep shared robots metadata for normal reader-facing routes
- project one bounded `noindex,follow` contract onto the generated `404.html`
  page
- keep the slice limited to metadata semantics rather than broader hosting or
  redirect behavior

## Discovery Scope

The restored static publication now emits `robots.txt`, canonical URLs,
browserconfig metadata, manifest metadata, social metadata, and a generated
`404.html` recovery page. One publication-semantics mismatch is still visible:
the shared document renderer currently applies the same
`<meta name="robots" content="index,follow" />` tag to every generated page,
including `404.html`.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` hardcodes one shared
  `index,follow` robots tag inside `_render_document(...)`
- `build_not_found_page(...)` reuses that shared renderer, so the not-found
  route inherits the same indexable robots contract as real publication pages
- the earlier `robots.txt` slice deliberately stayed bounded to one root
  crawler-policy artifact and did not address route-specific indexing metadata
- existing tests assert the shared robots tag on representative routes, but the
  repository has no bounded distinction yet between reader-facing content pages
  and the not-found recovery surface

This slice restores the minimum route-specific crawl semantics needed for the
current static publication:

- keep `index,follow` as the default for the public reading surface
- render `noindex,follow` for `404.html`
- preserve the existing shared site frame and recovery content without changing
  the route structure

This slice does not attempt HTTP status simulation beyond static hosting,
environment-specific crawl policy, route-classification beyond the 404 page, or
broader SEO strategy work.

## Use-Case Contract

### `ProjectRouteRobotsPolicy`

Given the generated route kind, project robots metadata such that:

- normal public publication routes keep the current `index,follow` contract
- the generated not-found route uses `noindex,follow`
- the same repository state yields the same robots directives for the same
  route kind

### `RenderNotFoundRobotsMetadata`

Given the generated `404.html` document and the shared renderer, render
metadata such that:

- the not-found page includes one explicit `noindex,follow` robots tag
- homepage, archive, search, saga, topic, and content routes remain unchanged
- the slice stays bounded to document-head metadata only

## Main Business Rules

- The static publication should invite indexing of real reader-facing routes but
  not of the generated not-found recovery page.
- Route-specific robots metadata must be deterministic and derived by the build,
  not maintained as a handwritten post-processing step.
- The 404 page should remain discoverable to readers through links and static
  hosting behavior while still opting out of indexing.
- The slice stays bounded to one route-specific metadata distinction rather than
  expanding into general SEO policy configuration.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer in `build_site.py`
- route-specific metadata projection for generated pages
- existing `404.html` generation path

## Initial Test Plan

- unit test asserting representative public routes still render
  `index,follow`
- unit test asserting `404.html` renders `noindex,follow`
- integration test asserting scenario output preserves route-specific robots
  metadata for homepage and `404.html`
- integration test asserting the publication remains free of same-origin `/api`
  assumptions and unchanged outside the bounded robots distinction

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- `dist/404.html` exists and includes
  `<meta name="robots" content="noindex,follow" />`
- representative reader-facing routes such as homepage and archives still
  include `<meta name="robots" content="index,follow" />`
- no other document-head metadata regresses as part of the route-specific
  robots change

## Done Criteria

- the build projects deterministic route-specific robots metadata
- `404.html` renders `noindex,follow`
- representative public routes remain `index,follow`
- deterministic tests cover the bounded distinction without changing the rest
  of the static publication contract
