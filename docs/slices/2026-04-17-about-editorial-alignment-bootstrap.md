# Slice: 2026-04-17 About Editorial Alignment Bootstrap

## Selected Pack

- `python_ddd_monolith`

## Runtime Targets

- Python build runtime
- static browser runtime
- filesystem-backed publication output

## Architecture Mode

Deterministic editorial alignment for the published About surface:

- correct the authored About page so it matches what the static site actually
  offers today
- keep the slice bounded to repository-owned content rather than shared chrome
  redesign or new contact infrastructure
- preserve the existing markdown-to-static-publication pipeline

## Discovery Scope

The generated site now exposes a substantial static publication surface:
homepage, section hubs, sagas, archives, search, RSS, sitemap, `robots.txt`,
identity assets, and a webmanifest. One content-level mismatch is still visible
in the current build: the About page summary promises "how to reach me," but
the authored page body and the generated site expose no actual contact method.

That gap is visible in current repository artifacts:

- `content/pages/about.md` declares a summary that promises personal
  reachability
- the same file's body contains only site purpose and publishing intent
- the generated `/about/` page, search index, and Open Graph metadata therefore
  repeat an unsupported claim

This slice corrects that mismatch in the narrowest possible way:

- revise the About page summary so it reflects the current publication truth
- revise the About page body so it describes the site's purpose and current
  reading surfaces without implying an unavailable contact channel
- let the existing builder propagate that corrected editorial state through the
  generated site

This slice does not attempt a contact form, social-link chrome, email
configuration, GitHub profile discovery, or any broader About-page redesign.

## Use-Case Contract

### `AuthorAboutPageContent`

Given the repository-owned About markdown entry, author content such that:

- the summary and body accurately describe the current static publication
- the text does not promise personal contact methods that the site does not
  publish
- the same repository state yields the same rendered About page and derived
  metadata

### `PublishAboutEditorialState`

Given the existing markdown-content pipeline, publish the revised About entry
such that:

- `/about/` renders the corrected editorial copy
- derived metadata surfaces such as search and Open Graph reflect the same
  corrected summary
- no new runtime dependency or configuration surface is introduced

## Main Business Rules

- Repository-authored public copy must not promise capabilities the current
  publication does not actually expose.
- The About page remains ordinary authored content, not a special runtime-owned
  feature.
- Existing markdown rendering, metadata projection, and static hosting
  contracts remain unchanged.
- GitHub Pages compatibility remains a hard constraint.

## Required Ports

- repository-owned markdown content
- existing markdown content loader
- existing static HTML and metadata renderers

## Initial Test Plan

- unit test asserting the in-repo About content loads with the corrected
  summary
- unit test asserting generated `/about/` HTML reflects the revised editorial
  copy
- integration test asserting scenario output no longer includes the unsupported
  reachability claim in `/about/`
- integration test asserting derived About metadata surfaces stay aligned with
  the revised copy

## Scenario Definition

Run the scenario CLI against the in-repo content set and inspect generated
artifacts to verify:

- `/about/` presents corrected purpose-oriented copy
- the page does not promise unsupported personal reachability
- search and Open Graph surfaces reflect the same revised summary
- the publication remains fully static and deterministic

## Done Criteria

- repository-owned About copy aligns with the current published site reality
- generated `/about/` output and derived metadata surfaces share the corrected
  editorial state
- deterministic tests cover the content correction and unchanged static-site
  behavior
