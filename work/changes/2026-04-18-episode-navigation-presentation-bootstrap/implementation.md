# Implementation: 2026-04-18 Episode Navigation Presentation Bootstrap

Implemented the episode-local navigation refinement in `build_site.py`:

- added an explicit `episode-breadcrumbs` presentation hook to episode breadcrumb markup
- added an explicit `episode-adjacent-nav` presentation hook to the previous/next episode nav
- kept the existing breadcrumb destinations, episode numbering, and adjacent-episode logic unchanged
- preserved static-site compatibility and the current discovery surfaces

Updated deterministic unit and integration tests to verify the new episode-only navigation shells.
