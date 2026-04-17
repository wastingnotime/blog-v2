# Impact Analysis

## Impacted Areas

- saga and arc content-loading rules
- narrative container rendering in the static-site builder
- domain models for saga and arc records
- deterministic tests for container routes

## Boundary Change

The build boundary remains static and content-driven, but saga and arc routes
stop behaving like metadata-only index pages and start rendering their authored
markdown body content.

That means the builder must now preserve and render:

- saga body markdown already present in repository content
- arc body markdown already present in repository content
- the composition order between authored content and existing navigation blocks

It should still avoid:

- turning container routes into generic standalone pages
- introducing container-specific runtime behavior
- weakening the existing deterministic arc and episode projections

## Risks

- loading container body content without rendering order discipline could make
  navigation harder to scan
- changing saga and arc record shapes could ripple through tests that only care
  about navigation unless the model boundary is kept stable
- if container copy becomes too dominant, pages may lose their role as
  navigational hubs rather than longform entries

## Follow-On Pressure

Once narrative container content is restored, the next likely pressures move
toward:

- broader migration of existing saga content from `../blog`
- richer container metadata if the authored model requires it
- release evaluation of the current static publication surface
