# Impact Analysis

## Summary

This slice adds a bounded `robots.txt` artifact so the static publication
exposes an explicit crawler-policy contract alongside the existing feed,
sitemap, search index, RSS autodiscovery, and Open Graph metadata.

Current observed contract:

- publication metadata includes `robots.txt`
- the generated artifact set carries a root crawler-policy file

## Impacted Areas

- static artifact generation in the site builder
- deterministic projection of crawler-policy lines from site settings
- integration coverage for one additional non-HTML publication artifact

## Boundary Change

The build does not gain new HTML routes. Instead, it includes one
machine-readable root artifact: `robots.txt`. That file stays bounded to a
single public-site policy plus a sitemap declaration derived from the
configured base URL.

## Risks

- the policy could accidentally become environment-specific if it depends on
  ad hoc local rules instead of site configuration
- scope could drift into broader SEO strategy, route-level exclusions, or
  provider-specific crawler tuning
- the sitemap reference could drift from the generated `sitemap.xml` contract if
  it is not derived from the same base-URL inputs

## Follow-On Pressure

- a later slice may need route-specific exclusions if the site gains private or
  duplicated surfaces
- release review should verify that `robots.txt`, `sitemap.xml`, and canonical
  URLs remain aligned as one publication-discovery contract
