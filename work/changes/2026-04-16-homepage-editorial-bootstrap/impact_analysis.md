# Impact Analysis

## Impacted Areas

- homepage-specific projection logic in the application layer
- domain view models for homepage and saga-summary rendering
- static-site HTML generation for the root route
- deterministic test coverage for homepage output

## Boundary Change

The build boundary stays static-first, but the root route stops being treated as
a migration status artifact and starts being treated as an editorial projection
of the content catalog.

That means the homepage should depend on:

- existing content metadata
- saga navigation projections already available in the build
- stable limits and ordering rules

It should not depend on:

- runtime APIs
- handwritten duplicated saga metrics
- visual-theme parity work from the old repository

## Risks

- introducing too much homepage curation in one slice could blur the boundary
  between deterministic projection and bespoke editorial tooling
- deriving saga status incorrectly could duplicate or conflict with existing
  saga navigation projections if responsibilities are not kept clear
- replacing bootstrap copy without an explicit editorial framing could make the
  homepage feel emptier rather than clearer

## Follow-On Pressure

Once the homepage becomes editorial, the next likely pressures move toward:

- richer standalone content surfaces for `library` and `studio`
- clearer site-wide presentation polish
- additional publication metadata such as timestamps, canonical labels, or
  future feed/archive slices
