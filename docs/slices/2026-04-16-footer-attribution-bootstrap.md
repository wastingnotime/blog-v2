# Slice: 2026-04-16 Footer Attribution Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Shared publication frame with deterministic footer attribution:

- restore a small footer across generated HTML pages
- keep the footer content static and build-time only
- preserve the existing shared navigation and page body contract

## Discovery Scope

The current static publication now restores authored content, section hubs,
publication metadata, search metadata, identity assets, and RSS discovery in
the shared chrome. The remaining shared-frame gap against the older
`../blog` surface is a compact footer attribution rendered at the bottom of
each page.

That footer is a good next slice because it is:

- shared across all generated routes
- publication-facing but operationally simple
- deterministic and fully static

This slice restores the minimum footer surface needed for the current
publication:

- add one shared footer to the common frame
- expose stable attribution text and deterministic year behavior
- keep the change bounded to footer rendering only

This slice does not attempt a broader footer redesign, social links, legal
pages, or expanded branding treatment.

## Use-Case Contract

### `ProjectFooterAttribution`

Given site settings and deterministic build context, project footer content
such that:

- the attribution text is stable across builds for the same configuration
- the year is deterministic rather than taken from ambient runtime time
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
- The slice stays bounded to footer rendering rather than overall frame
  redesign.
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

- the shared site frame renders deterministic footer attribution across
  generated HTML pages
- footer content remains small and publication-oriented
- deterministic tests cover footer rendering and unchanged navigation behavior
