# Impact Analysis

## Summary

The next slice should restore a static search index artifact so the generated
publication regains the `search.json` surface present in the older site without
introducing any runtime search backend or browser-side search UI.

## Impacted Areas

- publication metadata generation beyond `feed.xml` and `sitemap.xml`
- content projection for pages, sagas, arcs, and episodes
- static build output at the top level of `dist/`
- integration coverage for emitted non-HTML artifacts

## Boundary Change

The build boundary expands from HTML and XML publication artifacts to one
additional JSON artifact derived from the same repository-authored catalog and
site settings.

## Risks

- record shape drift from the older `search.json` surface could make future
  client-side search harder to reintroduce
- inconsistent URL derivation between HTML, sitemap, feed, and search index
- accidental scope drift from static artifact generation into interactive search
  behavior

## Follow-On Pressure

- a later slice may add a search page or lightweight client-side filtering
- search ranking or excerpt generation may need a separate slice once real
  search behavior exists
- release review should compare the new search artifact against the prior site
  surface once it is built
