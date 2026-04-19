# Impact Analysis

## Summary

This slice adds a bounded `404.html` artifact so the static publication
exposes an explicit not-found recovery surface for GitHub Pages and other
static hosts.

Current observed contract:

- the generated build includes `404.html`
- the repository has shared chrome and reader-facing routes suitable for a
  useful static recovery page

## Impacted Areas

- static HTML generation for one additional root artifact
- shared-frame rendering for a not-found route outside the authored content
  catalog
- integration coverage for static-hosting recovery behavior

## Boundary Change

The build gains one new root HTML artifact: `404.html`. That page reuses the
existing site frame and points readers back to stable publication surfaces
without introducing runtime route handling.

## Risks

- not-found copy could drift into generic framework language instead of the
  publication voice
- scope could drift into redirects, search recovery, or analytics behavior
- recovery links could become stale if they are not derived from the same route
  assumptions as the rest of the site frame

## Follow-On Pressure

- a later slice may add richer recovery behavior such as search suggestions once
  the client-side discovery surface matures
- release review should verify that `404.html` remains aligned with the shared
  chrome and current top-level route structure
