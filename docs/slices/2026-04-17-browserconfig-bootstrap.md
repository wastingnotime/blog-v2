# Slice: 2026-04-17 Browserconfig Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic Windows browserconfig metadata for the static publication:

- add one bounded `browserconfig.xml` artifact to the generated root output
- link that artifact from the shared document head through one deterministic
  `msapplication-config` tag
- keep the slice limited to metadata and existing identity assets only

## Discovery Scope

The restored static publication now includes canonical URLs, RSS discovery,
identity assets, manifest links, Open Graph metadata, Twitter Card metadata,
shared social preview image support, theme-color, Apple mobile-web-app
metadata, format-detection metadata, referrer metadata, color-scheme
metadata, application-name metadata, viewport-fit metadata, Windows tile color
metadata, shared author metadata, generator metadata, and shared robots
metadata. The next small platform-facing gap is the browserconfig contract:
generated output still lacks `browserconfig.xml`, and generated HTML pages omit
`meta name="msapplication-config"`.

Current repository evidence confirms that gap:

- `src/app/application/use_cases/build_site.py` renders
  `msapplication-TileColor` in the shared head but no `msapplication-config`
  tag
- the generated root artifact set already includes the favicon and touch-icon
  assets needed for a bounded Windows configuration surface
- the earlier tile-color slice explicitly avoided browserconfig XML, which
  leaves a clear next bounded follow-on rather than a broad new direction
- the current repository contains no `browserconfig.xml` source artifact, so
  the contract still belongs in deterministic build output rather than
  handwritten publication files

This slice restores the minimum explicit browserconfig surface needed for the
current publication:

- emit one deterministic `browserconfig.xml` root artifact during the build
- link that artifact from generated HTML pages with one shared
  `msapplication-config` tag
- reuse the existing tile color and published identity assets instead of
  adding new artwork

This slice does not attempt pinned-site-specific artwork, alternate tile sizes,
route-specific configuration, or broader Windows platform behavior.

## Use-Case Contract

### `ProjectBrowserconfigMetadata`

Given site settings, the current shared tile color, and existing identity
assets, project browserconfig metadata such that:

- the build emits one deterministic `browserconfig.xml` artifact
- the shared head exposes one deterministic `msapplication-config` link
- the browserconfig contents remain aligned with the existing tile color and
  icon surface

### `RenderBrowserconfigHeadAndArtifact`

Given a generated HTML document and the browserconfig renderer, render metadata
such that:

- each generated HTML page includes the bounded `msapplication-config` tag
- `browserconfig.xml` is emitted at the publication root
- existing viewport, author, application-name, color-scheme, referrer,
  theme-color, tile color, mobile-web-app, manifest, and social metadata
  remain unchanged

## Main Business Rules

- Browserconfig metadata must be explicit and deterministic across the
  generated static publication.
- The slice stays bounded to one root XML artifact plus one shared head tag.
- The selected tile color and icons should derive from the existing shared
  publication identity, not new platform-specific assets.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- shared document-head renderer
- root-artifact generation in `build_site.py`
- existing shared theme color and current identity assets

## Initial Test Plan

- unit test asserting the build emits a deterministic `browserconfig.xml`
  artifact
- unit test asserting representative generated HTML routes include the bounded
  `msapplication-config` tag
- integration test asserting scenario output contains `browserconfig.xml`
- integration test asserting homepage and representative content routes link to
  the browserconfig artifact while existing metadata remains unchanged

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- `dist/browserconfig.xml` exists with deterministic tile color and icon
  references
- homepage and representative content routes include the bounded
  `msapplication-config` tag in `<head>`
- the rest of the publication surface remains unchanged

## Done Criteria

- the build emits a deterministic `browserconfig.xml` root artifact
- generated HTML routes include the shared `msapplication-config` tag
- browserconfig content reuses the existing shared tile color and identity
  assets
- deterministic tests cover the new artifact and unchanged shared-head
  behavior
