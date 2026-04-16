# Impact Analysis

## Model Pressure

`blog-v2` now contains meaningful content and section routes, but the generated
pages still look and behave like disconnected documents. The old blog’s shared
base template provided a stable orientation layer that tied those routes into a
single publication.

## Impacted Areas

- shared HTML composition inside the static builder
- route-to-section projection for active navigation state
- integration coverage across representative page types
- cross-page consistency for top-level links

## Proposed Boundary

Keep the slice limited to shared chrome:

- add one reusable site frame around generated pages
- compute active top-level navigation state from route paths
- apply that frame across homepage, content pages, saga pages, topic pages, and
  section hubs

Do not expand into a full visual redesign, favicon/static asset pipeline, or
  external-brand integration.

## Risks

- coupling navigation state to brittle string matching across routes
- turning a bounded chrome slice into a broad styling rewrite
- accidentally breaking static-link assumptions while introducing shared layout

## Why This Slice Next

This is the smallest next slice that improves whole-site coherence without
changing the core content model. It turns the recovered routes into a navigable
publication surface rather than a set of independent pages.
