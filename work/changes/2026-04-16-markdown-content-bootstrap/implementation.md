# Implementation

## Scope Applied

This implementation adds the minimum repository-authored content flow required
by `docs/slices/2026-04-16-markdown-content-bootstrap.md`:

- in-repo markdown content under `content/`
- deterministic frontmatter loading into typed content records
- homepage recent-content projection
- standalone page rendering
- saga episode rendering

## Boundary Notes

The loader intentionally supports only the bounded frontmatter shape needed by
the current slice. It validates required fields and raises deterministic errors
for malformed inputs instead of silently skipping files.

Markdown rendering is intentionally small and local. It supports the constructs
present in the committed bootstrap content and current tests without pulling in
extra runtime dependencies before the content model proves itself.
