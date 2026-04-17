# Slice: 2026-04-17 Search Navigation Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Shared-site chrome update for the new search surface:

- add one Search link to the common navigation frame
- project active-state behavior for `/search/`
- keep the slice bounded to navigation and route affordance only

## Discovery Scope

The publication now emits a dedicated `/search/` route backed by the static
`search.json` artifact, but the shared site chrome still does not expose that
route. Readers can only reach the search page if they already know the URL.

That gap is explicit in current repository artifacts:

- `src/app/application/use_cases/project_navigation_state.py` still projects
  only `Home`, `Sagas`, `Library`, `Studio`, and `About`
- `_render_navigation(...)` in `build_site.py` therefore emits no Search link
  across generated pages

This slice restores the minimum search-navigation surface needed for the
current publication:

- add one `Search` link to the shared navigation
- mark `/search/` as the active section on the search route
- keep the change bounded to navigation projection and rendering

This slice does not attempt broader information-architecture changes, shortcut
keys, persistent search state, or redesign of the site frame.

## Use-Case Contract

### `ProjectNavigationState`

Given a generated route path, compute deterministic navigation state such that:

- the shared navigation includes the Search route
- the search route can be marked active when the current path is `/search/`
- existing top-level route behavior remains unchanged for the other sections

### `RenderSharedSiteChrome`

Given shared navigation state and a generated page, render deterministic chrome
such that:

- every generated page exposes a visible Search link
- `/search/` highlights Search as the active section
- existing static links remain valid under the configured base URL

## Main Business Rules

- The Search route should be discoverable from the shared site frame, not only
  by direct URL entry.
- A page should continue to highlight at most one top-level section as active.
- Adding Search must not disturb existing route targets for Home, Sagas,
  Library, Studio, About, and RSS.
- The slice stays bounded to navigation affordance rather than changing search
  behavior itself.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared navigation-state projection
- shared HTML navigation renderer
- existing `/search/` static route

## Initial Test Plan

- unit test asserting navigation state includes Search and marks it active for
  `/search/`
- unit test asserting existing section active-state behavior remains unchanged
- integration test asserting representative generated pages expose a Search link
- integration test asserting `/search/` marks Search active in the shared frame

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
pages to verify:

- homepage and representative content routes include a Search link
- `search/index.html` highlights Search as the active section
- links remain static and traversable without an application server

## Done Criteria

- the shared site frame exposes a deterministic Search link
- `/search/` marks Search active in navigation
- existing top-level route highlighting remains correct
- deterministic tests cover navigation-state projection and generated output
