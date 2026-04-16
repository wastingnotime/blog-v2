# Slice: 2026-04-16 Shared Site Chrome Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed content source under repository control

## Architecture Mode

Static-site builder with a shared layout frame for generated routes:

- render a consistent navigation shell around page bodies
- project route-aware navigation links into every generated page
- keep layout composition deterministic and independent from any runtime
  framework

## Discovery Scope

The current slices restore content, hierarchy, taxonomy, and section hubs, but
the site still behaves like a collection of isolated generated documents. The
old blog used a shared base template to provide orientation, repeated section
links, and a more coherent reading surface.

This slice restores the minimum shared chrome needed to make `blog-v2` feel
like one publication:

- a consistent top-level navigation frame across generated pages
- links for the main site surfaces: home, sagas, library, studio, about
- route-aware active-state rendering when a page belongs to one of those
  surfaces

This slice does not attempt full visual parity with the old Tailwind-based
theme, asset-pipeline work, or analytics/layout integration beyond the shared
HTML frame.

## Use-Case Contract

### `RenderSharedSiteChrome`

Given site settings, route metadata, and a page body, generate deterministic
static HTML such that:

- every generated page renders inside a shared site frame
- the frame links to the main generated sections
- the current section is visually distinguishable in the navigation
- generated output contains no same-origin `/api` dependency

### `ProjectNavigationState`

Given a generated route path, compute deterministic navigation state for:

- the active top-level section
- section link targets for the shared frame
- stable labeling of the main surfaces

## Main Business Rules

- Shared chrome must be derived from generated route structure, not handwritten
  per-page fragments.
- Navigation labels and targets should stay consistent across all page types.
- A page should highlight at most one top-level section as active.
- The shared frame must not introduce runtime dependencies or route assumptions
  incompatible with GitHub Pages.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for content sources
- filesystem writer for build artifacts
- environment reader for site settings

## Initial Test Plan

- unit test for deterministic active-section projection from route paths
- integration test asserting generated pages include shared navigation links
- integration test asserting the expected page marks the current section active
- integration test asserting generated HTML stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
pages to verify:

- homepage, saga, library, studio, and about pages share one navigation frame
- the current section is highlighted consistently on representative routes
- navigation links are static and traversable without an application server

## Done Criteria

- generated pages share a consistent navigation shell
- the main site sections are linked from every generated page
- representative routes expose the correct active top-level section
- deterministic tests cover navigation-state projection and generated output

