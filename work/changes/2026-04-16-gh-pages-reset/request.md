# Request

## Summary

Turn this repository into `blog-v2`, the successor to `../blog`, with one
major change in deployment shape:

- remove the call to `/api`
- return the site to `gh-pages` deployment
- stop targeting the AWS environment as the primary runtime

## Source Evidence

- stakeholder request in this repository session
- `../blog/templates/base.gohtml` currently posts analytics to
  `https://blog.wastingnotime.org/api/event`
- `../blog/.github/workflows/docker-blog.yml` deploys the blog image into AWS
- `../blog/.github/workflows/docker-analytics-api.yml` deploys the analytics API
- `../blog/internal/analytics/docs/event-contract.md` documents the AWS-backed
  analytics ingestion path
- `../infrastructure/terraform/environments/production/swarm/stacks/blog.yml`
  shows the current container deployment shape

## Requested Outcome

Bootstrap `blog-v2` around static generation and GitHub Pages deployment, with
no same-origin API requirement in generated site output.

## Resolution

This request is satisfied by the current repository state:

- static generation is implemented in the Python builder
- generated output has no same-origin `/api` dependency
- GitHub Pages-oriented deployment artifacts are present
