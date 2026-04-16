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

## Evaluation Risks To Watch

- generated HTML accidentally containing references to `/api`
- deployment workflows drifting back toward container or AWS assumptions
- analytics configuration appearing enabled but depending on unavailable
  runtime infrastructure
- loss of deterministic builds because environment-specific behavior leaks into
  the generated output
