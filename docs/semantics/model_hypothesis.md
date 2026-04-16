# Model Hypothesis

## Context

`blog-v2` is not a generic MRL example anymore. It is the successor to the
existing `../blog` repository and inherits one concrete migration pressure:
the current production shape depends on AWS-hosted runtime infrastructure and a
first-party `/api` endpoint, while the desired `v2` shape should return to
static publishing through GitHub Pages.

## Core Concepts

- `SiteBuild`: a deterministic build that turns repository content and settings
  into static files.
- `DeploymentTarget`: the hosting contract for generated files. The current
  target hypothesis is GitHub Pages rather than AWS containers.
- `AnalyticsMode`: whether the generated site emits analytics and, if so,
  whether that integration is direct-to-provider or disabled.
- `SiteSettings`: build-time values such as title, description, and base URL.

## Likely Entities And Value Objects

- `SiteConfig`: immutable site-wide configuration for a build.
- `AnalyticsConfig`: optional configuration that must never require a
  first-party `/api` route on the deployed site.
- `BuildArtifact`: the generated file set under `dist/`.

## Major State Transitions

- repository source plus configuration -> generated static artifact
- generated static artifact -> GitHub Pages deployment
- analytics disabled -> analytics enabled through direct third-party endpoint

## Candidate Use Cases

- `BuildStaticSite`
- `RenderHomepage`
- `RenderAnalyticsSnippet`
- `DeployToGitHubPages`

## Model Constraints

- The browser-facing site must remain valid when hosted as static files only.
- The generated HTML must not assume a same-origin `/api` backend exists.
- AWS runtime concerns from `../infrastructure` are migration context, not part
  of the target runtime model for `blog-v2`.

## Open Questions

- Whether the long-term site generator remains a minimal Python builder or
  shifts to another runtime later.
- Whether analytics should stay disabled by default permanently or use direct
  Plausible integration once deployment is stable.
