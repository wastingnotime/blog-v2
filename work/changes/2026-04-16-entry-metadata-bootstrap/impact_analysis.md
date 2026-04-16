# Impact Analysis

## Impacted Areas

- content-entry projection logic in the application layer
- domain view models for page and episode metadata
- static HTML rendering for standalone pages and saga episodes
- deterministic tests for content-derived metadata

## Boundary Change

The build boundary stays fully static, but content entries become richer
publication objects rather than plain markdown renderings with only date and
container context.

That means the builder must now reason about:

- how to derive a stable reading-time estimate from markdown content
- how to expose tag metadata already present in frontmatter
- how to link entry metadata back into existing topic routes without runtime
  lookups

It should still avoid:

- browser-side metadata calculation
- external reading-time services
- inventing content metadata that is not derivable from repository artifacts

## Risks

- an overly clever reading-time heuristic would add noise instead of clarity
- metadata rendering could drift between standalone pages and episodes if the
  projection contract is not shared
- tag links on entries could imply topic coverage that does not exist if the
  route mapping is not aligned with the library builder

## Follow-On Pressure

Once entry metadata is restored, the next likely pressures move toward:

- authored section intros for `library` and `studio`
- broader migration of content from `../blog`
- release evaluation of whether the static publication surface is internally
  coherent enough for acceptance
