# Domain Background Knowledge

## Static Site Expectations

Users expect a personal blog to load as ordinary pages and links even when no
application server is running behind the domain. GitHub Pages reinforces this
expectation because it serves static files and does not provide arbitrary
backend endpoints under the same origin.

## Analytics Expectations

Client-side analytics on static sites usually follow one of these patterns:

- disabled entirely
- direct script integration with the analytics provider
- provider-hosted proxy endpoints that are not implemented by the site itself

What does not fit GitHub Pages is an architecture that depends on the blog
origin exposing custom runtime routes like `/api/event`.

## Migration Knowledge From `../blog`

The previous repository contains two separate concerns that should not be
conflated:

- static page generation for the blog itself
- AWS-backed analytics ingestion through API Gateway, Lambda, SQS, and a
  consumer feeding Plausible

That AWS flow was a deployment choice, not a core requirement of rendering a
blog page.

The previous repository also established a recognizable visual language that is
independent from its AWS deployment shape. That style language is valid
migration evidence for `blog-v2` even when the old implementation details are
not reused directly.

## Editorial Style Knowledge From `../blog`

The predecessor's rendered site uses a dark, minimal, text-first editorial
shell rather than a bright product-marketing layout.

Observed stable signals:

- near-black page background with light zinc-gray text hierarchy
- monospaced or editorial-feeling typography rather than a default serif shell
- subdued links that brighten on hover instead of colorful accent-heavy calls
  to action
- compact uppercase section labels such as `RECENT` and `SAGAS`
- breadcrumb and metadata styling that stays quiet relative to titles
- outlined topic chips or pills rather than filled badges
- prose treatment tuned for long-form reading with restrained borders and code
  surfaces

These signals matter because readers use them to recognize continuity across
versions of a personal publication. A successor that keeps the content model
but swaps to a generic bright starter theme can feel like a different site even
when routes and copy survive intact.

## Migration Boundaries For Style Recovery

Style recovery should not be treated as a request to recreate the old stack:

- do not reintroduce Tailwind CDN or another runtime styling dependency just to
  match the old look
- do not copy old templates wholesale when the new builder already owns
  rendering
- do not let shared-style work silently expand into full content-model or
  navigation redesign

The portable insight is the visual language and reading atmosphere, not the old
templating mechanics.

## Evaluation Risks To Watch

- generated HTML accidentally containing references to `/api`
- deployment workflows drifting back toward container or AWS assumptions
- analytics configuration appearing enabled but depending on unavailable
  runtime infrastructure
- loss of deterministic builds because environment-specific behavior leaks into
  the generated output
- stylistic slices drifting into broad redesign work instead of one bounded
  shared-style recovery at a time
- restoring dark styling in isolated pages without a coherent site-wide token
  system, producing inconsistent surfaces across routes
