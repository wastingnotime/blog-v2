# Model Hypothesis

## Context

`blog-v2` is not a generic MRL example anymore. It is the successor to the
existing `../blog` repository and inherits one concrete migration pressure:
the current production shape depends on AWS-hosted runtime infrastructure and a
first-party `/api` endpoint, while the desired `v2` shape should return to
static publishing through GitHub Pages.

The migration is not only architectural. The predecessor also established a
recognizable reader-facing visual language: dark, text-first, editorial, and
minimal. The current `v2` implementation has recovered static publishing and
discovery structure, but it has not yet recovered that stylistic continuity.

## Core Concepts

- `SiteBuild`: a deterministic build that turns repository content and settings
  into static files.
- `DeploymentTarget`: the hosting contract for generated files. The current
  target hypothesis is GitHub Pages rather than AWS containers.
- `EditorialStyleSystem`: shared visual tokens and shell rules that give the
  publication a consistent reading atmosphere across homepage, indexes, and
  long-form pages.
- `AnalyticsMode`: whether the generated site emits analytics and, if so,
  whether that integration is direct-to-provider or disabled.
- `SiteSettings`: build-time values such as title, description, and base URL.

## Likely Entities And Value Objects

- `SiteConfig`: immutable site-wide configuration for a build.
- `AnalyticsConfig`: optional configuration that must never require a
  first-party `/api` route on the deployed site.
- `StyleTokens`: immutable presentation values such as surfaces, text colors,
  borders, and typography selections shared across generated pages.
- `BuildArtifact`: the generated file set under `dist/`.

## Major State Transitions

- repository source plus configuration -> generated static artifact
- generated static artifact -> GitHub Pages deployment
- extracted visual-language evidence from `../blog` -> shared style decisions
  in generated output
- analytics disabled -> analytics enabled through direct third-party endpoint

## Candidate Use Cases

- `BuildStaticSite`
- `RenderSharedSiteChrome`
- `RenderEditorialStyleTokens`
- `RenderHomepage`
- `RenderAnalyticsSnippet`
- `DeployToGitHubPages`

## Model Constraints

- The browser-facing site must remain valid when hosted as static files only.
- The generated HTML must not assume a same-origin `/api` backend exists.
- Shared styling must be deterministic at build time and must not depend on a
  runtime CSS pipeline or third-party CDN.
- AWS runtime concerns from `../infrastructure` are migration context, not part
  of the target runtime model for `blog-v2`.
- Migration success should preserve enough of the original publication's dark
  editorial identity that `v2` still reads like the same blog, not a generic
  starter site.

## Open Questions

- Whether the long-term site generator remains a minimal Python builder or
  shifts to another runtime later.
- Whether analytics should stay disabled by default permanently or use direct
  Plausible integration once deployment is stable.
- How much of the predecessor's visual language should be restored through one
  shared shell slice before page-specific layout tuning begins.
