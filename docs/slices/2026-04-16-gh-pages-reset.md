# Slice: 2026-04-16 Gh Pages Reset

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- GitHub Actions deployment to GitHub Pages

## Architecture Mode

Static-site builder with explicit configuration objects and a thin CLI entry
point.

## Discovery Scope

This slice covers only the first bootstrap needed to make `blog-v2` target the
desired runtime shape. It does not migrate all old content or templates.

## Use-Case Contract

### `BuildStaticSite`

Given site configuration and optional analytics settings, generate deterministic
static output under `dist/` such that:

- the homepage renders from local code only
- the output contains no same-origin `/api` reference
- analytics are absent by default
- when analytics are enabled, the output uses a direct external provider
  script, not a first-party API proxy

### `DeployToGitHubPages`

Given a successful build on `main`, publish the generated `dist/` directory to
GitHub Pages.

## Main Business Rules

- GitHub Pages compatibility is the primary deployment constraint.
- The generated output must remain functional as static files only.
- Analytics must never require the blog origin to implement `/api`.

## Required Ports

- filesystem writer for build artifacts
- environment reader for build-time settings

## Initial Test Plan

- unit test for analytics-disabled rendering
- unit test for direct analytics rendering
- integration test for writing `dist/index.html`

## Scenario Definition

Run the scenario CLI locally and inspect `dist/index.html` to verify that the
site builds without AWS or API dependencies.

## Done Criteria

- repository artifacts describe the migration target clearly
- `python -m src.app.interfaces.cli.run_scenario` generates `dist/index.html`
- generated HTML has no same-origin `/api` dependency
- GitHub Pages workflow is present
- tests pass
