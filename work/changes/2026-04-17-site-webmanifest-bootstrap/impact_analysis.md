# Impact Analysis

## Summary

The next slice should add a bounded `site.webmanifest` artifact so the static
publication exposes a coherent browser-install metadata surface alongside the
existing identity assets and machine-readable publication files.

Current observed gap:

- favicon and touch-icon files are published, but no manifest file exists
- the generated `dist/` output still lacks a browser-facing manifest contract

## Impacted Areas

- static artifact generation for one additional root metadata file
- deterministic projection of manifest fields from site settings
- alignment between generated manifest data and the existing identity-asset set

## Boundary Change

The build gains one new root artifact: `site.webmanifest`. That file should
stay bounded to name, start URL, display mode, and icon metadata derived from
the current static publication.

## Risks

- manifest fields could drift from the published icon set if references are not
  derived from the same asset contract
- scope could drift into broader progressive-web-app behavior the site does not
  actually implement
- naming or start-url defaults could become inconsistent with existing site
  settings if not projected from the same configuration source

## Follow-On Pressure

- a later slice may revisit richer PWA behavior only if the repository
  explicitly chooses to support it
- release review should verify that `site.webmanifest`, favicon assets, and
  head metadata remain aligned as one browser-facing identity contract
