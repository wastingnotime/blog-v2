# Slice: 2026-04-17 Archives Navigation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Shared-site chrome update for the archive surface:

- add one Archives link to the common navigation frame
- project active-state behavior for `/archives/`
- keep the slice bounded to navigation and route discoverability only

## Discovery Scope

The publication now emits a dedicated `/archives/` route for chronological
browsing, but the shared site chrome still does not expose that route. Readers
can only reach the archive page if they already know the URL or encounter one
of the limited recovery links elsewhere.

That gap is explicit in current repository artifacts:

- `dist/archives/index.html` exists as a generated publication route
- `src/app/application/use_cases/project_navigation_state.py` still projects
  `Home`, `Search`, `Sagas`, `Library`, `Studio`, and `About`, but no archive
  route
- shared navigation rendering therefore cannot make the archive page
  discoverable or mark it active

This slice restores the minimum archive-navigation surface needed for the
current publication:

- add one `Archives` link to the shared navigation
- mark `/archives/` as the active section on the archive route
- keep the change bounded to navigation projection and rendering

This slice does not attempt year-grouped archive navigation, breadcrumbs,
homepage redesign, or broader information-architecture restructuring.

## Use-Case Contract

### `ProjectNavigationState`

Given a generated route path, compute deterministic navigation state such that:

- the shared navigation includes the Archives route
- the archive route can be marked active when the current path is `/archives/`
- existing top-level route behavior remains unchanged for the other sections

### `RenderSharedSiteChrome`

Given shared navigation state and a generated page, render deterministic chrome
such that:

- every generated page exposes a visible Archives link
- `/archives/` highlights Archives as the active section
- existing static links remain valid under the configured base URL

## Main Business Rules

- The archive route should be discoverable from the shared site frame, not only
  by direct URL entry or not-found recovery links.
- A page should continue to highlight at most one top-level section as active.
- Adding Archives must not disturb existing route targets for Home, Search,
  Sagas, Library, Studio, About, and RSS.
- The slice stays bounded to navigation affordance rather than changing archive
  content itself.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared navigation-state projection
- shared HTML navigation renderer
- existing `/archives/` static route

## Initial Test Plan

- unit test asserting navigation state includes Archives and marks it active for
  `/archives/`
- unit test asserting existing section active-state behavior remains unchanged
- integration test asserting representative generated pages expose an Archives
  link
- integration test asserting `/archives/` marks Archives active in the shared
  frame

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
pages to verify:

- homepage and representative content routes include an Archives link
- `archives/index.html` highlights Archives as the active section
- links remain static and traversable without an application server

## Done Criteria

- the shared site frame exposes a deterministic Archives link
- `/archives/` marks Archives active in navigation
- existing top-level route highlighting remains correct
- deterministic tests cover navigation-state projection and generated output
