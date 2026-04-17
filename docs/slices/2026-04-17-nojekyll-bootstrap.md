# Slice: 2026-04-17 NoJekyll Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- filesystem-backed publication output
- GitHub Actions deployment to GitHub Pages

## Architecture Mode

Deterministic GitHub Pages publication-contract hardening for the current static
build:

- emit one bounded `.nojekyll` artifact at the publication root
- make the Pages deployment explicitly publish generated files as-is
- stay within the current static build and deployment model

## Discovery Scope

The repository now generates a substantial root artifact set for GitHub Pages:
HTML routes, metadata artifacts, identity assets, and a custom-domain `CNAME`.
The deployment workflow uploads `dist/` directly, but the generated output
still does not include a `.nojekyll` file.

That gap is visible in current repository artifacts:

- `.github/workflows/gh-pages.yml` deploys `dist/` directly to GitHub Pages
- the build already owns root deployment artifacts such as `CNAME`,
  `robots.txt`, `site.webmanifest`, and `sitemap.xml`
- the generated `dist/` root still lacks `.nojekyll`, leaving Pages free to
  apply Jekyll processing to a site that is intended to be published as raw
  generated static output

This slice restores the minimum Pages publication guardrail needed for the
current deployment contract:

- emit a root `.nojekyll` artifact as part of the static build
- keep the artifact deterministic and content-light
- keep the slice bounded to publication output rather than branching the
  workflow or introducing Jekyll-specific content features

This slice does not redesign deployment workflow steps, add new routes, or
introduce template processing.

## Use-Case Contract

### `BuildPagesPublicationArtifacts`

Given the current GitHub Pages build target, generate deterministic root output
such that:

- the publication artifact set explicitly opts out of Jekyll processing
- the build remains static-file-only
- the output can still be inspected and reproduced locally

### `BuildStaticSite`

Given the current site configuration and content set, include the `.nojekyll`
artifact such that:

- existing HTML, XML, JSON, and identity artifacts remain unchanged
- deployment output stays aligned with the repository's explicit static-site
  contract
- GitHub Pages can publish the generated artifact set without treating Jekyll
  as part of the runtime model

## Main Business Rules

- The generated publication artifact set should explicitly express when GitHub
  Pages must publish files as raw static output.
- The `.nojekyll` artifact must be emitted by the build rather than maintained
  manually outside the generated output.
- The slice stays bounded to one deployment artifact, not broader workflow or
  hosting changes.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- existing static-site build output writer
- existing GitHub Pages deployment workflow
- current root-artifact generation path in `build_site.py`

## Initial Test Plan

- unit test asserting the static build emits a root `.nojekyll` artifact
- unit test asserting the artifact content stays deterministic and minimal
- integration test asserting generated `dist/.nojekyll` exists in scenario
  output
- integration test asserting the slice does not alter existing static HTML
  assumptions or introduce same-origin `/api` usage

## Scenario Definition

Run the scenario CLI with the default in-repo configuration and inspect
`dist/.nojekyll` to verify:

- the artifact exists at the publication root
- it contains the bounded expected content
- the rest of the generated static artifact set remains unchanged

## Done Criteria

- the build emits a deterministic root `.nojekyll` artifact
- `dist/.nojekyll` is present in local scenario output
- deterministic tests cover both artifact path and minimal content
- GitHub Pages deployment output remains explicit about its static-only
  publication contract
