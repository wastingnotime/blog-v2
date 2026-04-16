# Impact Analysis

## Impacted Areas

- repository semantics and decisions
- deployment workflow
- initial implementation scaffold
- deterministic tests for generated output

## Non-Goals In This Slice

- full content migration from `../blog`
- parity with every page, template, and asset from the old repository
- recreation of AWS analytics ingestion in another form

## Main Boundary Changes

- deployment target moves from AWS container workflow to GitHub Pages
- analytics move from same-origin API proxy assumption to optional direct
  provider integration
- the repository starts with a static build boundary rather than an API or
  server boundary

## Risks

- the site may stay too skeletal if later slices do not follow with content and
  richer page rendering
- direct analytics integration may still require provider-specific validation
  before production use
