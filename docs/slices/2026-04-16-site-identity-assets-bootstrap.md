# Slice: 2026-04-16 Site Identity Assets Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed asset source under repository control

## Architecture Mode

Static-site builder with bounded identity-asset publication:

- publish repository-owned icon assets into the generated static output
- link generated HTML documents to those assets deterministically
- keep asset handling file-based and compatible with GitHub Pages

## Discovery Scope

The current slices restore authored content, navigation, publication metadata,
and section surfaces, but the generated site still lacks basic identity assets
such as favicons and touch icons. The old `../blog` static output shipped those
artifacts directly and linked them from every page head.

This slice restores the minimum identity-asset surface needed for the static
publication to feel complete:

- publish a bounded favicon set from repository-owned assets
- add deterministic head links for those assets on generated HTML pages
- keep asset output independent from any runtime framework or asset pipeline

This slice does not attempt a full image pipeline, social preview cards,
responsive image generation, or broader brand-system work.

## Use-Case Contract

### `PublishIdentityAssets`

Given repository-owned icon assets and the output directory, generate static
site output such that:

- the favicon files are copied into `dist/`
- copied filenames remain stable and directly addressable
- the asset publication requires no runtime processing service

### `RenderIdentityAssetLinks`

Given site settings and a generated HTML document, render deterministic head
links such that:

- each HTML page references the published favicon files
- asset paths remain valid under the configured static-site base URL
- the links are consistent across all generated HTML routes

## Main Business Rules

- Identity assets must be repository-owned and published as static files.
- Asset filenames and head links should remain deterministic across builds.
- The slice should stay bounded to a small favicon/touch-icon set rather than
  turning into a general asset pipeline.
- Generated publication metadata files such as `feed.xml` and `sitemap.xml`
  should remain unaffected except by the presence of additional static assets in
  the output directory.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for repository assets
- filesystem writer for build artifacts
- environment reader for site settings

## Initial Test Plan

- integration test asserting identity assets are copied into `dist/`
- integration test asserting generated HTML pages include favicon and touch-icon
  links in the document head
- integration test asserting asset links use static paths compatible with the
  configured base URL
- integration test asserting generated output stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- favicon files exist in `dist/`
- homepage and representative content routes link to those assets in `<head>`
- asset paths are static and valid without an application server
- the rest of the publication surface remains unchanged

## Done Criteria

- the build publishes a bounded favicon/touch-icon set into `dist/`
- generated HTML routes link to the published identity assets
- deterministic tests cover copied assets and rendered head links
