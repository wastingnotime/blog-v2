# Slice: 2026-04-18 Shared Editorial Shell Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Bounded shared-style recovery for the existing static publication shell:

- keep the current Python builder and static GitHub Pages deployment model
- preserve current routes, content projection, discovery surfaces, and search
  behavior
- recover one shared dark editorial shell in the existing document renderer so
  the site regains continuity with `../blog`

## Discovery Scope

The extracted migration evidence now shows a gap that is broader than one page
but narrower than a redesign:

- `blog-v2` currently renders through one shared document shell
- that shell uses a light serif presentation that does not match the
  predecessor's dark editorial identity
- the original blog's stable signals are mostly global shell concerns:
  background, text hierarchy, link treatment, navigation tone, and long-form
  reading atmosphere

This slice restores the minimum shared style needed to make `v2` feel like the
same publication again:

- introduce shared dark editorial tokens in the existing document renderer
- shift the shell typography and link treatment toward the extracted
  predecessor style
- add a subtle layered background treatment so the shell no longer reads as a
  flat monochrome canvas
- improve shared prose, metadata, navigation, and code-surface styling through
  the same renderer

This slice does not attempt homepage information-architecture parity, Tailwind
migration, asset-pipeline work, animation, new routes, or page-specific layout
redesign.

## Use-Case Contract

### `RenderSharedEditorialShell`

Given any page rendered through the shared document renderer, produce
deterministic markup such that:

- the page uses a dark editorial shell rather than the current bright serif
  shell
- shared typography, link, metadata, and border treatments remain consistent
  across routes
- the page background carries a subtle layered treatment while staying fully
  static and deterministic
- the styling remains fully static and embedded in generated HTML

### `BuildStaticSite`

Given the current content catalog and site configuration, render deterministic
site output such that:

- existing routes and page content stay intact
- the shared site shell reflects the extracted predecessor style signals
- no runtime CSS dependency or same-origin backend dependency is introduced

## Main Business Rules

- Shared site styling should preserve continuity with the predecessor's dark,
  minimal, text-first publication identity.
- The styling change should be centralized in the shared renderer rather than
  duplicated page by page.
- The background treatment should feel intentionally layered without adding a
  runtime asset dependency.
- The slice should stay bounded to visual shell recovery and must not widen
  into content-model, navigation-structure, or page-specific layout redesign.
- Static-hosting compatibility remains a hard constraint.

## Required Ports

- shared document renderer in `src/app/application/use_cases/build_site.py`
- current route and page renderers that flow through the shared shell
- existing deterministic build and scenario test paths

## Initial Test Plan

- unit test asserting generated document CSS reflects the bounded dark-shell
  token shift instead of the current light-paper shell
- unit test asserting shared navigation and content pages continue rendering
  through the same single document shell
- unit test asserting the body background includes a bounded layered
  treatment instead of a flat fill
- integration test asserting generated `dist/index.html` reflects the shared
  dark editorial shell
- integration test asserting the publication remains static-only and does not
  introduce runtime styling dependencies

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated page
artifacts to verify:

- the homepage and at least one content page share the same dark editorial
  shell
- link, metadata, and prose styling reflect the extracted predecessor signals
- the page background feels layered rather than flat while staying static-only
- existing routes and discovery surfaces remain intact
- output remains deterministic and static-only

## Done Criteria

- the shared renderer emits a dark editorial shell aligned with extracted
  predecessor style signals
- homepage and content pages visibly share the same shell treatment
- no route or behavior contracts change
- deterministic tests cover the shared-style recovery without expanding into a
  full redesign
