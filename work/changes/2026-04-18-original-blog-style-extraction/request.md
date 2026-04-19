# Request

## Summary

Recover style continuity from `../blog` so `blog-v2` does not stay functionally
correct but visually generic.

The next loop should treat the predecessor's reader-facing visual language as a
real migration input:

- preserve the static GitHub Pages deployment model
- extract the dark editorial style signals already present in `../blog`
- use those signals to guide bounded shared-style restoration in `blog-v2`

## Source Evidence

- stakeholder request in this repository session noting the current lack of
  style
- `../blog/templates/base.gohtml` defines the original global dark shell,
  subdued link palette, breadcrumb treatment, topic-link treatment, and prose
  styling
- `../blog/templates/home.gohtml` defines the original homepage tone, compact
  uppercase section labels, and text-first information hierarchy
- `../blog/public/index.html` confirms those style signals are rendered in the
  generated site rather than existing only as template intent
- `src/app/application/use_cases/build_site.py` currently renders a light serif
  shell that does not match the predecessor's visual language

## Requested Outcome

Make the original blog's visual language explicit in repository artifacts so
the next refined slice can restore a bounded part of that identity without
copying the old implementation wholesale or changing the static-only runtime
model.

## Resolution

This request is satisfied by the current repository state:

- the predecessor's dark editorial signals are captured in semantic artifacts
- the shared editorial shell and homepage follow-on slices reflect those signals
- the implementation stays static-only and does not copy the old templates wholesale
