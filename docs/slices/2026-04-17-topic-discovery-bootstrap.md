# Slice: 2026-04-17 Topic Discovery Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic topic-page discovery update for the expanded publication surface:

- revise topic pages so they point readers toward the current complementary
  discovery routes
- add bounded affordances for Search and Archives alongside the existing topic
  entry listing
- keep the slice limited to topic-page discovery copy and links

## Discovery Scope

The publication now exposes stable reader-facing discovery routes for topic
pages, archives, and search. Topic pages still reflect an earlier site shape
and behave as isolated tag listings with only a breadcrumb back to `/library/`.

That gap is visible in current repository artifacts:

- `build_topic_page(...)` renders a breadcrumb to `/library/` and an `Entries`
  list, but no complementary discovery affordance for `/archives/` or
  `/search/`
- topic pages are already a meaningful reader-facing route family under
  `/library/<tag>/`
- archives and search are now first-class routes with shared-navigation
  discoverability, but topic pages do not acknowledge them

This slice restores the minimum topic discovery surface needed for the current
publication:

- update topic pages so they link readers to `/archives/` and `/search/`
- preserve the existing breadcrumb and topic-entry list
- keep the change bounded to topic-page discovery copy and links

This slice does not attempt broader topic-page redesign, taxonomy changes, new
search behavior, or archive faceting.

## Use-Case Contract

### `BuildTopicPage`

Given the projected topic page and current reader-facing routes, generate
deterministic static output for `/library/<tag>/` such that:

- the page continues to list entries for the topic
- readers can reach search and archives directly from the topic page
- output remains fully static and compatible with GitHub Pages hosting

### `RenderTopicDiscovery`

Given a topic route and current publication surfaces, render bounded discovery
content such that:

- the page still centers topic entries as its primary job
- archives and search are visibly represented as complementary discovery paths
- the section remains publication-oriented rather than turning into generic
  navigation chrome

## Main Business Rules

- Topic-page discovery copy must stay aligned with the routes the publication
  now exposes.
- Topic discovery affordances should point to stable reader-facing routes, not
  implementation artifacts.
- The slice stays bounded to topic-page copy and linking rather than changing
  topic projection or shared navigation.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing topic-page renderer
- environment reader for site settings
- existing stable routes for `/search/`, `/archives/`, and `/library/<tag>/`

## Initial Test Plan

- unit test asserting a topic page links directly to `/archives/` and
  `/search/`
- unit test asserting the existing breadcrumb and topic-entry list remain
  present
- integration test asserting generated `dist/library/<tag>/index.html`
  exposes the new topic discovery affordances
- integration test asserting the page remains free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect a generated
topic page such as `dist/library/architecture/index.html` to verify:

- the topic page still reads like a topic hub
- the page links directly to search and archive discovery surfaces
- the existing breadcrumb and entry list remain unchanged
- the artifact remains fully static and compatible with GitHub Pages

## Done Criteria

- topic pages align with the current publication discovery surface
- `/library/<tag>/` exposes deterministic links to `/search/` and `/archives/`
- deterministic tests cover the new topic affordances and unchanged
  static-only behavior
