# Slice: 2026-04-17 Social Preview Image Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic social-preview image publication in the shared document head:

- publish one bounded repository-owned social preview image into the generated
  static output
- expose that image through existing Open Graph and Twitter Card metadata
- keep the slice limited to one shared image contract rather than per-route
  media generation

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, Open Graph metadata, Twitter Card metadata, `CNAME`, and
`.nojekyll`. The next publication-surface gap is the image side of social link
unfurls: generated pages still expose text metadata only and no shared social
preview image.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders `og:*` and `twitter:*`
  text metadata but no `og:image` or `twitter:image` tags
- the generated root artifact set contains identity assets only, with no
  bounded social preview image file
- the earlier Open Graph and Twitter Card slices both explicitly stayed out of
  image generation and richer media treatment

This slice restores the minimum social-preview image surface needed for the
current publication:

- publish one bounded repository-owned preview image into `dist/`
- add deterministic `og:image` and `twitter:image` metadata that resolve to the
  published asset
- keep rendering consistent across homepage, sections, pages, and narrative
  routes

This slice does not attempt per-route artwork, generated preview cards, account
handles, or richer media policy.

## Use-Case Contract

### `PublishSocialPreviewAsset`

Given a repository-owned social preview image and the output directory,
generate static-site output such that:

- the preview image is copied into `dist/` with a stable filename
- copied filenames remain deterministic and directly addressable
- publication requires no runtime processing service

### `RenderSocialPreviewMetadata`

Given site settings and a generated HTML document, render head metadata such
that:

- `og:image` and `twitter:image` both resolve to the published preview asset
- the preview asset URL remains valid under the configured static-site base URL
- existing title, description, and canonical metadata remain unchanged

## Main Business Rules

- Social preview images must be repository-owned and published as static files.
- The slice stays bounded to one shared preview image rather than per-route
  image generation.
- `og:image` and `twitter:image` should resolve to the same deterministic asset
  in this bootstrap slice.
- Metadata should remain consistent across all generated HTML routes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- filesystem reader for repository-owned assets
- filesystem writer for build artifacts
- environment reader for site settings
- shared document-head renderer

## Initial Test Plan

- integration test asserting the preview image is copied into `dist/`
- unit test asserting representative HTML routes include `og:image` and
  `twitter:image`
- unit test asserting image URLs use the configured static-site base URL
- integration test asserting existing Open Graph and Twitter text metadata
  remain unchanged
- integration test asserting generated output stays free of same-origin `/api`
  assumptions

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- the preview image exists in `dist/`
- homepage and representative content routes include `og:image` and
  `twitter:image` in `<head>`
- image URLs are static and valid without an application server
- the rest of the publication surface remains unchanged

## Done Criteria

- the build publishes one bounded social preview image into `dist/`
- generated HTML routes include deterministic `og:image` and `twitter:image`
  metadata
- the image URL derives from existing site settings and the published asset
- deterministic tests cover copied asset publication and head metadata
