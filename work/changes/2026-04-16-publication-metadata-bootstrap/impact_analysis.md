# Impact Analysis

## Impacted Areas

- publication-metadata projection logic in the application layer
- static-site builder outputs beyond HTML pages
- domain view models for feed and sitemap entries
- deterministic integration coverage for non-HTML artifacts

## Boundary Change

The build boundary remains static-first, but it expands from human-facing HTML
pages into machine-readable publication artifacts.

That means the builder must now reason about:

- which content belongs in a syndication feed
- which generated routes belong in a sitemap
- how to derive stable absolute URLs and `lastmod` values from repository
  metadata

It should still avoid:

- runtime route discovery
- filesystem timestamp dependence
- manual duplicate manifests that drift from generated pages

## Risks

- projecting feed and sitemap entries from slightly different route rules could
  create subtle drift between human-facing pages and metadata artifacts
- including too many structural routes in the feed could weaken the publication
  signal and make the slice less coherent
- invalid XML generation would be easy to miss if tests only assert fragments
  rather than full artifact shape

## Follow-On Pressure

Once publication metadata exists, the likely next pressures move toward:

- richer content metadata such as reading time or author information
- broader content migration from `../blog`
- release-oriented evaluation of whether the static publication surface is now
  internally complete enough for acceptance
