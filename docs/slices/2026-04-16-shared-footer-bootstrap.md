# Slice: 2026-04-16 Shared Footer Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Shared publication frame with deterministic footer rendering:

- restore a small footer on all generated HTML pages
- keep footer content static and compatible with GitHub Pages
- preserve the existing shared navigation and body structure

## Discovery Scope

The restored static publication now exposes authored content, section hubs,
machine-readable metadata, identity assets, search metadata, and RSS discovery
through the shared chrome. One piece of the older shared site frame is still
missing: a small footer rendered consistently across pages.

The older `../blog` output ended each page with a compact attribution footer.
That is a good next slice because it is:

- shared across all route types
- publication-facing but operationally simple
- fully static and deterministic

This slice restores the minimum shared-footer surface needed for the current
publication:

- add one shared footer to the common frame
- expose stable attribution text and deterministic year behavior
- keep the change bounded to footer rendering only

This slice does not attempt a larger footer redesign, social links, legal
pages, or expanded site-wide branding treatment.

## Use-Case Contract

### `ProjectSharedFooter`

Given site settings and deterministic build context, project footer content
such that:

- the footer text is stable across builds for the same configuration
- the footer includes a deterministic publication year
- the footer requires no runtime service or client-side computation

### `RenderSharedFooter`

Given a generated HTML document and the shared site frame, render the footer
such that:

- the footer appears consistently across homepage, section pages, pages, and
  narrative routes
- the existing navigation and active-state behavior remain unchanged
- no same-origin `/api` dependency is introduced

## Main Business Rules

- The footer is part of the shared site frame, not page-specific content.
- Footer content should remain small, deterministic, and publication-oriented.
- The slice stays bounded to rendering the shared footer rather than redesigning
  the whole page chrome.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- environment reader for site settings
- deterministic build-time year source
- HTML document renderer for generated routes

## Initial Test Plan

- unit test asserting generated HTML pages include the shared footer
- unit test asserting the footer year and attribution are deterministic
- integration test asserting homepage and representative content routes render
  the same footer
- integration test asserting navigation active state remains unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- homepage and representative content routes include the shared footer
- footer text is consistent across page types
- the footer does not alter existing route generation or machine-readable
  outputs
- the publication stays free of same-origin `/api` assumptions

## Done Criteria

- the shared site frame renders a deterministic footer across generated HTML
  pages
- footer content remains stable and publication-oriented
- deterministic tests cover footer rendering and unchanged navigation behavior
