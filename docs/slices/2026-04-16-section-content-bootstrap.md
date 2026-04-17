# Slice: 2026-04-16 Section Content Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed content source under repository control

## Architecture Mode

Static-site builder with authored section content for non-entry hubs:

- load repository-authored markdown for section-level intro copy
- combine authored section bodies with existing deterministic hub projections
- keep section routing static and content-driven

## Discovery Scope

The current slices restore navigation, homepage framing, publication metadata,
and entry-level metadata, but `library` and `studio` still depend on hardcoded
builder copy. That is now out of step with the rest of the site, where content
and metadata increasingly come from repository-authored markdown.

This slice restores the minimum content authorship needed for section pages to
behave like real publication surfaces:

- allow `/library/` to render authored intro copy from repository content
- allow `/studio/` to render authored intro copy from repository content
- preserve the existing deterministic topic list and section-link behavior

This slice does not attempt CMS-like section management, arbitrary dynamic
sections, or redesign of the existing library and studio layouts.

## Use-Case Contract

### `LoadSectionPages`

Given a content root, load a bounded set of repository-authored markdown
documents for named section hubs such that:

- section content is explicit and versioned in the repository
- missing required section sources fail deterministically
- section authorship stays separate from standalone entry pages when helpful

### `BuildLibrarySectionPage`

Given authored section content plus the projected topic catalog, generate
deterministic static output for `/library/` such that:

- the page renders authored intro copy
- the page still lists deterministic topic links from tagged content
- the page remains compatible with static hosting

### `BuildStudioSectionPage`

Given authored section content and existing route surfaces, generate
deterministic static output for `/studio/` such that:

- the page renders authored intro copy from repository markdown
- the page still links into `/sagas/` and `/library/`
- the page remains meaningful with a small in-repo content set

## Main Business Rules

- Section-level orientation copy should be authored in repository markdown, not
  embedded as builder literals.
- Section content must stay bounded to known static routes rather than turning
  the builder into a generic section CMS.
- The library page must continue to derive topic links from tagged content,
  even when its surrounding copy becomes authored content.
- The studio page may contain curated outbound or cross-section links, but its
  primary navigation targets must remain real generated routes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for content sources
- filesystem writer for build artifacts
- environment reader for site settings

## Initial Test Plan

- unit test for deterministic loading of authored section content
- integration test asserting `/library/` renders:
  - authored intro copy
  - deterministic topic links
- integration test asserting `/studio/` renders:
  - authored intro copy
  - links to `/sagas/` and `/library/`
- integration test asserting generated HTML stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
section pages to verify:

- the library page reads like an authored section surface instead of a pure
  builder stub
- the studio page renders repository-authored section copy
- both pages still expose their existing deterministic navigation outcomes
- the pages remain fully static and traversable without an application server

## Done Criteria

- `/library/` and `/studio/` render repository-authored section copy
- section content is loaded deterministically from the repository
- existing topic and section navigation remains intact
- deterministic tests cover section-content loading and generated output
