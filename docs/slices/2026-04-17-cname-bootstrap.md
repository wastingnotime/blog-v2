# Slice: 2026-04-17 CNAME Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- filesystem-backed publication output
- GitHub Actions deployment to GitHub Pages

## Architecture Mode

Deterministic custom-domain deployment artifact for the current static-site
output:

- emit one bounded `CNAME` artifact from build configuration
- keep the custom-domain contract aligned with the configured site base URL
- stay within the current GitHub Pages deployment model

## Discovery Scope

The repository now generates a much more complete static publication surface,
and the default site configuration still targets `https://blog.wastingnotime.org/`.
The GitHub Pages workflow deploys `dist/` directly, but the generated artifact
set still does not include a `CNAME` file.

That gap is visible in current repository artifacts:

- `load_site_config()` defaults `SITE_BASE_URL` to `https://blog.wastingnotime.org/`
- `.github/workflows/gh-pages.yml` uploads `dist/` as the Pages artifact
- the generated `dist/` includes route, metadata, and identity artifacts, but
  no root `CNAME`

This slice restores the minimum custom-domain deployment contract needed for
the current publication:

- emit a root `CNAME` artifact when the configured base URL resolves to a
  custom host
- derive the published hostname deterministically from `SiteConfig.base_url`
- keep the slice bounded to the deployment artifact rather than broadening into
  DNS automation, workflow branching, or environment-specific publishing logic

This slice does not change routing, introduce redirects, manage registrar DNS,
or redesign the GitHub Actions workflow.

## Use-Case Contract

### `BuildCustomDomainArtifact`

Given site configuration for a GitHub Pages build, generate deterministic root
output such that:

- a custom host can be published as a root `CNAME` artifact
- the artifact contains only the host name, not scheme, path, or extra markup
- the output remains valid for static-file deployment

### `BuildStaticSite`

Given the current static publication build, include the custom-domain artifact
such that:

- the generated output stays aligned with the configured base URL
- existing HTML and metadata artifacts remain unchanged
- GitHub Pages deployment can consume the output without extra manual file
  maintenance

## Main Business Rules

- The generated `CNAME` artifact must be derived from the configured site base
  URL rather than hard-coded separately.
- The artifact must contain only the host that GitHub Pages expects.
- Root-path custom-domain publication should stay deterministic across local
  scenario runs and CI builds.
- The slice stays bounded to emitting the deployment artifact, not to
  deployment orchestration beyond the existing workflow.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- environment reader for `SITE_BASE_URL`
- existing static-site build output writer
- existing `SiteConfig` projection used by the scenario CLI and workflow build

## Initial Test Plan

- unit test asserting the static build emits a root `CNAME` entry for a custom
  host base URL
- unit test asserting the artifact content is just the expected host name
- integration test asserting generated `dist/CNAME` exists in the scenario
  output and matches `blog.wastingnotime.org`
- integration test asserting the slice does not alter existing static HTML
  assumptions or introduce same-origin `/api` usage

## Scenario Definition

Run the scenario CLI with the default in-repo configuration and inspect
`dist/CNAME` to verify:

- the artifact exists at the publication root
- its content is exactly `blog.wastingnotime.org`
- the rest of the generated static artifact set remains unchanged

## Done Criteria

- the build emits a deterministic root `CNAME` artifact for the configured
  custom host
- `dist/CNAME` matches the configured default publication host
- deterministic tests cover both the artifact path and its host-only content
- GitHub Pages deployment output remains static-only and aligned with the
  configured custom domain
