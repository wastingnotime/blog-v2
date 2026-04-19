import json
import re

from src.app.application.use_cases.build_site import build_static_site
from src.app.domain.models.content import (
    Arc,
    ContentCatalog,
    Episode,
    Page,
    Saga,
    SectionPage,
)
from src.app.domain.models.site_config import AnalyticsConfig, SiteConfig


def test_build_static_site_omits_same_origin_api_when_analytics_disabled() -> None:
    html = build_static_site(_site_config(), _catalog())["index.html"]

    assert "/api/event" not in html
    assert 'src="https://plausible.io/js/script.js"' not in html


def test_build_static_site_renders_direct_plausible_configuration() -> None:
    config = SiteConfig(
        title="Example",
        description="Static site",
        base_url="https://example.com/",
        analytics=AnalyticsConfig(
            provider="plausible",
            domain="example.com",
            script_url="https://plausible.example.com/js/script.js",
            api_host="https://plausible.example.com",
        ),
    )

    html = build_static_site(config, _catalog())["index.html"]

    assert 'src="https://plausible.example.com/js/script.js"' in html
    assert 'data-api="https://plausible.example.com/api/event"' in html
    assert 'data-domain="example.com"' in html
    assert "https://example.com/api/event" not in html


def test_build_static_site_orders_recent_content_by_date_desc() -> None:
    html = build_static_site(_site_config(), _catalog())["index.html"]

    assert html.index("[episode] Second Iteration") < html.index("[page] About")


def test_build_static_site_limits_homepage_recent_entries() -> None:
    html = build_static_site(_site_config(), _catalog_with_extra_page())["index.html"]

    assert "Architecture, focus, and growth in public." in html
    assert "Experiments in architecture, focus, and growth, built in public one saga at a time." in html
    assert "This site tracks architecture decisions" not in html
    assert '<ul class="homepage-list">' in html
    assert 'class="homepage-link"' in html
    assert 'class="homepage-meta">2026-04-13 · HireFlow / The Origin Blueprint</small>' in html
    assert 'class="homepage-summary">Follow-up work.</p>' in html
    assert "[episode] Second Iteration" in html
    assert "[episode] The First Brick" in html
    assert "[page] Notes" in html
    assert "[page] About" not in html


def test_build_static_site_renders_arc_page_and_episode_navigation() -> None:
    pages = build_static_site(_site_config(), _catalog())

    saga_html = pages["sagas/hireflow/index.html"]
    arc_html = pages["sagas/hireflow/the-origin-blueprint/index.html"]
    first_episode_html = pages[
        "sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"
    ]
    second_episode_html = pages[
        "sagas/hireflow/the-origin-blueprint/second-iteration/index.html"
    ]

    assert '<ul class="saga-arc-list">' in saga_html
    assert '<a class="saga-arc-link" href="https://example.com/sagas/hireflow/the-origin-blueprint/">The Origin Blueprint</a>' in saga_html
    assert 'class="saga-arc-meta">2 episodes · last 2026-04-13</small>' in saga_html
    assert '<ul class="saga-timeline-list">' in saga_html
    assert '<a class="saga-timeline-link" href="https://example.com/sagas/hireflow/the-origin-blueprint/the-first-brick/">[Ep 01] The First Brick</a>' in saga_html
    assert 'class="saga-timeline-meta">The Origin Blueprint · 2026-04-12</small>' in saga_html
    assert "[Ep 01] The First Brick" in arc_html
    assert "[Ep 02] Second Iteration" in arc_html
    assert '<ul class="arc-episode-list">' in arc_html
    assert '<a class="breadcrumb-link" href="https://example.com/sagas/hireflow/">' in arc_html
    assert '<a class="arc-episode-link" href="https://example.com/sagas/hireflow/the-origin-blueprint/the-first-brick/">[Ep 01] The First Brick</a>' in arc_html
    assert 'class="arc-episode-meta">2026-04-12</small>' in arc_html
    assert "Arc body." in arc_html
    assert "/archives/" in arc_html
    assert "/search/" in arc_html
    assert "1 min read" in first_episode_html
    assert 'href="https://example.com/library/architecture/"' in first_episode_html
    assert 'href="https://example.com/archives/"' in first_episode_html
    assert 'href="https://example.com/search/"' in first_episode_html
    assert '<a class="breadcrumb-link" href="https://example.com/sagas/hireflow/">' in first_episode_html
    assert '<span class="breadcrumb-separator">/</span>' in first_episode_html
    assert '<a class="breadcrumb-link" href="https://example.com/sagas/hireflow/the-origin-blueprint/">' in first_episode_html
    assert 'class="adjacent-nav-link next" href="https://example.com/sagas/hireflow/the-origin-blueprint/second-iteration/"' in first_episode_html
    assert "Ep 02 Second Iteration" in first_episode_html
    assert 'class="adjacent-nav-link previous" href="https://example.com/sagas/hireflow/the-origin-blueprint/the-first-brick/"' in second_episode_html
    assert "Ep 01 The First Brick" in second_episode_html
    assert ".breadcrumb-link {" in first_episode_html
    assert ".breadcrumb-separator {" in first_episode_html
    assert ".adjacent-nav-link {" in first_episode_html
    assert ".adjacent-nav-link.next {" in first_episode_html
    assert ".saga-arc-list {" in saga_html
    assert ".saga-arc-link {" in saga_html
    assert ".saga-arc-meta {" in saga_html
    assert ".saga-timeline-list {" in saga_html
    assert ".saga-timeline-link {" in saga_html
    assert ".saga-timeline-meta {" in saga_html
    assert ".arc-episode-list {" in arc_html
    assert ".arc-episode-link {" in arc_html
    assert ".arc-episode-meta {" in arc_html


def test_build_static_site_generates_library_and_topic_pages() -> None:
    pages = build_static_site(_site_config(), _catalog())

    archive_html = pages["archives/index.html"]
    search_html = pages["search/index.html"]
    library_html = pages["library/index.html"]
    topic_html = pages["library/architecture/index.html"]

    assert "Chronological Archive" in archive_html
    assert '<ul class="archive-entry-list">' in archive_html
    assert '<a class="archive-entry-link" href="https://example.com/sagas/hireflow/the-origin-blueprint/second-iteration/">[episode] Second Iteration</a>' in archive_html
    assert 'class="archive-entry-meta">2026-04-13 · HireFlow / The Origin Blueprint</small>' in archive_html
    assert 'class="archive-entry-summary">Follow-up work.</p>' in archive_html
    assert "[episode] Second Iteration" in archive_html
    assert "[page] About" in archive_html
    assert archive_html.index("[episode] Second Iteration") < archive_html.index("[page] About")
    assert "HireFlow / The Origin Blueprint" in archive_html
    assert "/search/" in archive_html
    assert "/library/" in archive_html
    assert "Search the publication" in search_html
    assert 'id="search-form"' in search_html
    assert 'method="get"' in search_html
    assert 'action="https://example.com/search/"' in search_html
    assert '<label for="search-query">Search query</label>' in search_html
    assert '<p id="search-helper">Type to filter the static index published with the site.</p>' in search_html
    assert 'aria-describedby="search-helper search-status"' in search_html
    assert '<button type="submit">Search</button>' in search_html
    assert 'type="search"' in search_html
    assert 'name="q"' in search_html
    assert "<noscript>" in search_html
    assert "Live search on this page requires JavaScript." in search_html
    assert "browse the chronology or move by topic instead." in search_html
    assert 'id="search-status" aria-live="polite" aria-atomic="true"' in search_html
    assert 'id="search-results" class="search-result-list" aria-label="Search results"' in search_html
    assert "Enter a query to search the publication." in search_html
    assert "https://example.com/search.json" in search_html
    assert "new URLSearchParams(window.location.search).get('q') ?? ''" in search_html
    assert "const normalizeSearchText = (value) => (value || '').trim().toLowerCase();" in search_html
    assert "const projectSearchUrlState = (query) => {" in search_html
    assert "const scoreSearchRecord = (record, normalizedQuery) => {" in search_html
    assert "const createHighlightedFragment = (value, normalizedQuery) => {" in search_html
    assert "const searchRecovery = document.createElement('p');" in search_html
    assert "const fragment = document.createDocumentFragment();" in search_html
    assert "const mark = document.createElement('mark');" in search_html
    assert "mark.textContent = sourceText.slice(matchIndex, matchIndex + normalizedQuery.length);" in search_html
    assert "if (normalizedTitle === normalizedQuery) {" in search_html
    assert "if (normalizedTitle.startsWith(normalizedQuery)) {" in search_html
    assert "if (normalizedTitle.includes(normalizedQuery)) {" in search_html
    assert "if (normalizedContext === normalizedQuery) {" in search_html
    assert "if (normalizedSummary.includes(normalizedQuery)) {" in search_html
    assert "if (normalizedTags.some((tag) => tag === normalizedQuery)) {" in search_html
    assert "return Number.POSITIVE_INFINITY;" in search_html
    assert ".filter(({ score }) => Number.isFinite(score))" in search_html
    assert ".sort((left, right) => {" in search_html
    assert "return left.score - right.score;" in search_html
    assert "const titleComparison = normalizeSearchText(left.record.title)" in search_html
    assert "return (left.record.url || '').localeCompare(right.record.url || '');" in search_html
    assert "searchRecovery.replaceChildren();" in search_html
    assert "if (!matches.length) {" in search_html
    assert "searchRecovery.appendChild(document.createTextNode('Try '));" in search_html
    assert "archivesLink.textContent = 'the archives';" in search_html
    assert "libraryLink.textContent = 'the library';" in search_html
    assert "searchResults.appendChild(searchRecovery);" in search_html
    assert "Search index could not be loaded." in search_html
    assert "while search is unavailable." in search_html
    assert "link.appendChild(document.createTextNode(`[${record.type}] `));" in search_html
    assert "item.className = 'search-result-item';" in search_html
    assert "link.className = 'search-result-link';" in search_html
    assert "meta.className = 'search-result-meta';" in search_html
    assert "summary.className = 'search-result-summary';" in search_html
    assert "tags.className = 'search-result-tags';" in search_html
    assert "link.appendChild(createHighlightedFragment(record.title, normalizedQuery));" in search_html
    assert "meta.appendChild(createHighlightedFragment(record.context, normalizedQuery));" in search_html
    assert "summary.appendChild(createHighlightedFragment(record.summary, normalizedQuery));" in search_html
    assert "if ((record.tags || []).length) {" in search_html
    assert ".search-result-list {" in search_html
    assert ".search-result-link {" in search_html
    assert ".search-result-meta {" in search_html
    assert ".search-result-summary {" in search_html
    assert ".search-result-tags {" in search_html
    assert "tags.appendChild(document.createTextNode('Tags: '));" in search_html
    assert "record.tags.forEach((tag, index) => {" in search_html
    assert "tags.appendChild(createHighlightedFragment(tag, normalizedQuery));" in search_html
    assert "nextUrl.searchParams.set('q', normalizedQuery);" in search_html
    assert "nextUrl.searchParams.delete('q');" in search_html
    assert "window.history.replaceState(null, '', nextPath);" in search_html
    assert "searchForm.addEventListener('submit', (event) => {" in search_html
    assert "searchInput.value = initialQuery;" in search_html
    assert "renderResults(searchInput.value);" in search_html
    assert "projectSearchUrlState(event.target.value);" in search_html
    assert '<meta name="robots" content="noindex,follow" />' in search_html
    assert '<meta name="robots" content="index,follow" />' not in search_html
    assert '<link rel="canonical" href="https://example.com/search/" />' in search_html
    assert "/archives/" in search_html
    assert "/library/" in search_html
    assert 'href="https://example.com/archives/"' in search_html
    assert 'href="https://example.com/library/"' in search_html
    assert "Topics" in library_html
    assert "The library is the fastest way to move by idea instead of chronology." in library_html
    assert "Other ways in" in library_html
    assert 'href="https://example.com/archives/"' in library_html
    assert 'href="https://example.com/search/"' in library_html
    assert '<ul class="library-topic-list">' in library_html
    assert '<a class="topic-link" href="https://example.com/library/architecture/">#architecture</a>' in library_html
    assert '<a class="breadcrumb-link" href="https://example.com/library/">' in topic_html
    assert '<ul class="topic-entry-list">' in topic_html
    assert '<a class="topic-entry-link" href="https://example.com/about/">[page] About</a>' in topic_html
    assert 'class="topic-entry-meta">2026-04-10</small>' in topic_html
    assert '<a class="topic-entry-link" href="https://example.com/sagas/hireflow/the-origin-blueprint/second-iteration/">[episode] Second Iteration</a>' in topic_html
    assert 'class="topic-entry-meta">2026-04-13 · HireFlow / The Origin Blueprint</small>' in topic_html
    assert 'class="topic-entry-summary">Follow-up work.</p>' in topic_html
    assert "[page] About" in topic_html
    assert "[episode] Second Iteration" in topic_html
    assert "HireFlow / The Origin Blueprint" in topic_html
    assert "/archives/" in topic_html
    assert "/search/" in topic_html


def test_build_static_site_refines_homepage_editorial_surface() -> None:
    html = build_static_site(_site_config(), _catalog())["index.html"]

    assert "Architecture, focus, and growth in public." in html
    assert "Experiments in architecture, focus, and growth, built in public one saga at a time." in html
    assert "This site tracks architecture decisions" not in html
    assert (
        '<p class="homepage-paths"><a href="https://example.com/search/">Search</a> / '
        '<a href="https://example.com/archives/">Archives</a> / '
        '<a href="https://example.com/library/">Library</a></p>'
    ) in html
    assert '<h2 class="section-label">RECENT</h2>' in html
    assert '<h2 class="section-label">SAGAS</h2>' in html
    assert '<h2 class="section-label">LIBRARY</h2>' in html
    assert 'class="homepage-meta">2026-04-13 · HireFlow / The Origin Blueprint</small>' in html
    assert 'class="homepage-saga-row">' in html
    assert 'class="homepage-saga-status">2 episodes - last release 2026-04-13 - in-progress</small>' in html
    assert "<h2>In Public</h2>" not in html
    assert "<h2>Active Sagas</h2>" not in html


def test_build_static_site_uses_base_url_for_search_form_action() -> None:
    pages = build_static_site(_site_config(base_url="https://example.com/blog/"), _catalog())

    search_html = pages["search/index.html"]

    assert 'action="https://example.com/blog/search/"' in search_html
    assert 'action="/search/"' not in search_html
    assert "https://example.com/blog/search.json" in search_html
    assert '<link rel="canonical" href="https://example.com/blog/search/" />' in search_html


def test_build_static_site_generates_section_hub_pages() -> None:
    pages = build_static_site(_site_config(), _catalog())

    sagas_html = pages["sagas/index.html"]
    studio_html = pages["studio/index.html"]

    assert "Active sagas" in sagas_html
    assert "Other ways in" in sagas_html
    assert '<ul class="saga-index-list">' in sagas_html
    assert '<a class="saga-index-link" href="https://example.com/sagas/hireflow/">HireFlow</a>' in sagas_html
    assert 'class="saga-index-summary">Architecture in public.</p>' in sagas_html
    assert '<small class="saga-index-start"><a href="https://example.com/sagas/hireflow/the-origin-blueprint/the-first-brick/">start reading</a></small>' in sagas_html
    assert "/archives/" in sagas_html
    assert "/search/" in sagas_html
    assert "/library/" in studio_html
    assert "/sagas/" in studio_html
    assert "/archives/" in studio_html
    assert "/search/" in studio_html
    assert "<h2>In the studio</h2>" in studio_html
    assert '<ul class="studio-discovery-list">' in studio_html
    assert '<a class="studio-discovery-label" href="https://example.com/sagas/">See active sagas</a>' in studio_html
    assert '<small class="studio-discovery-path">/sagas/</small>' in studio_html
    assert "Other ways in" not in studio_html
    assert "Wasting No Time is a studio for architecture" in studio_html


def test_build_static_site_generates_feed_and_sitemap() -> None:
    pages = build_static_site(_site_config(), _catalog())

    nojekyll = pages[".nojekyll"]
    cname = pages["CNAME"]
    not_found_html = pages["404.html"]
    feed_xml = pages["feed.xml"]
    robots_txt = pages["robots.txt"]
    opensearch_xml = pages["opensearch.xml"]
    webmanifest = json.loads(pages["site.webmanifest"])
    browserconfig_xml = pages["browserconfig.xml"]
    sitemap_xml = pages["sitemap.xml"]

    assert nojekyll == "\n"
    assert cname == "example.com\n"
    assert "Page Not Found" in not_found_html
    assert "Try one of these instead" in not_found_html
    assert '<ul class="not-found-list">' in not_found_html
    assert '<a class="not-found-link" href="https://example.com/">Return home</a>' in not_found_html
    assert '<small class="not-found-path">/</small>' in not_found_html
    assert 'href="https://example.com/search/"' in not_found_html
    assert 'href="https://example.com/archives/"' in not_found_html
    assert 'href="https://example.com/sagas/"' in not_found_html
    assert 'href="https://example.com/library/"' in not_found_html
    assert "<rss version=\"2.0\">" in feed_xml
    assert "<title>Second Iteration</title>" in feed_xml
    assert "<link>https://example.com/sagas/hireflow/the-origin-blueprint/second-iteration/</link>" in feed_xml
    assert "Fri, 11 Apr 2026" not in feed_xml
    assert "User-agent: *" in robots_txt
    assert "Allow: /" in robots_txt
    assert "Sitemap: https://example.com/sitemap.xml" in robots_txt
    assert '<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">' in opensearch_xml
    assert "<ShortName>Example</ShortName>" in opensearch_xml
    assert "<Description>Static site</Description>" in opensearch_xml
    assert 'template="https://example.com/search/?q={searchTerms}"' in opensearch_xml
    assert webmanifest["name"] == "Example"
    assert webmanifest["short_name"] == "Example"
    assert webmanifest["start_url"] == "https://example.com/"
    assert webmanifest["display"] == "standalone"
    assert webmanifest["theme_color"] == "#0b0b0b"
    assert webmanifest["background_color"] == "#000000"
    assert webmanifest["icons"][0]["src"] == "https://example.com/favicon-16x16.png"
    assert webmanifest["icons"][1]["src"] == "https://example.com/favicon-32x32.png"
    assert webmanifest["icons"][2]["src"] == "https://example.com/apple-touch-icon.png"
    assert "<browserconfig>" in browserconfig_xml
    assert '<square150x150logo src="https://example.com/apple-touch-icon.png"/>' in browserconfig_xml
    assert "<TileColor>#0b0b0b</TileColor>" in browserconfig_xml
    assert "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" in sitemap_xml
    assert "<loc>https://example.com/archives/</loc>" in sitemap_xml
    assert "<loc>https://example.com/library/</loc>" in sitemap_xml
    assert "<loc>https://example.com/sagas/hireflow/</loc>" in sitemap_xml
    assert "<lastmod>2026-04-13</lastmod>" in sitemap_xml
    assert "https://example.com/search/" not in sitemap_xml


def test_build_static_site_adds_shared_navigation_and_active_section() -> None:
    pages = build_static_site(_site_config(), _catalog())

    home_html = pages["index.html"]
    search_html = pages["search/index.html"]
    archive_html = pages["archives/index.html"]
    about_html = pages["about/index.html"]
    saga_html = pages["sagas/hireflow/index.html"]

    assert ">Home</a>" in home_html
    assert 'class="active">Home</a>' in home_html
    assert 'href="https://example.com/search/"' in home_html
    assert 'href="https://example.com/archives/"' in home_html
    assert 'class="active">Search</a>' in search_html
    assert 'class="active">Archives</a>' in archive_html
    assert 'class="active">About</a>' in about_html
    assert 'class="active">Sagas</a>' in saga_html
    assert 'href="https://example.com/library/"' in saga_html
    assert 'href="https://example.com/feed.xml"' in home_html
    assert 'href="https://example.com/feed.xml"' in about_html
    assert 'href="https://example.com/feed.xml"' in saga_html
    assert 'rel="alternate" type="application/rss+xml" title="Example RSS" href="https://example.com/feed.xml"' in home_html
    assert 'rel="alternate" type="application/rss+xml" title="Example RSS" href="https://example.com/feed.xml"' in about_html
    assert 'rel="alternate" type="application/rss+xml" title="Example RSS" href="https://example.com/feed.xml"' in saga_html
    assert 'rel="search" type="application/opensearchdescription+xml" title="Example Search" href="https://example.com/opensearch.xml"' in home_html
    assert 'rel="search" type="application/opensearchdescription+xml" title="Example Search" href="https://example.com/opensearch.xml"' in about_html
    assert 'rel="search" type="application/opensearchdescription+xml" title="Example Search" href="https://example.com/opensearch.xml"' in saga_html
    assert "(c) 2026 example.com - published as a static site" in home_html
    assert "(c) 2026 example.com - published as a static site" in about_html
    assert "(c) 2026 example.com - published as a static site" in saga_html


def test_build_static_site_renders_editorial_homepage_instead_of_status_card() -> None:
    html = build_static_site(_site_config(), _catalog())["index.html"]

    assert "Architecture, focus, and growth in public." in html
    assert "Experiments in architecture, focus, and growth, built in public one saga at a time." in html
    assert "This site tracks architecture decisions" not in html
    assert '<p class="homepage-intro">Experiments in architecture, focus, and growth, built in public one saga at a time.</p>' in html
    assert 'href="https://example.com/search/"' in html
    assert 'href="https://example.com/archives/"' in html
    assert '<h2 class="section-label">RECENT</h2>' in html
    assert '<h2 class="section-label">SAGAS</h2>' in html
    assert '<h2 class="section-label">LIBRARY</h2>' in html
    assert '<a class="homepage-link" href="https://example.com/sagas/hireflow/">HireFlow</a>' in html
    assert "2 episodes - last release 2026-04-13 - in-progress" in html
    assert "Deployment target:" not in html


def test_build_static_site_renders_entry_metadata_for_pages() -> None:
    html = build_static_site(_site_config(), _catalog())["about/index.html"]

    assert "1 min read" in html
    assert 'href="https://example.com/library/architecture/"' in html
    assert 'href="https://example.com/archives/"' in html
    assert 'href="https://example.com/search/"' in html
    assert "#architecture" in html
    assert "homepage, saga index, library, archive, and search surfaces" in html


def test_build_static_site_renders_narrative_container_body_content() -> None:
    pages = build_static_site(_site_config(), _catalog())

    saga_html = pages["sagas/hireflow/index.html"]
    arc_html = pages["sagas/hireflow/the-origin-blueprint/index.html"]

    assert "Saga body." in saga_html
    assert "Other ways in" in saga_html
    assert "/archives/" in saga_html
    assert "/search/" in saga_html
    assert "Arc body." in arc_html


def test_build_static_site_uses_shared_discovery_surface_with_route_specific_links() -> None:
    pages = build_static_site(_site_config(), _catalog())

    archive_discovery = _discovery_section(pages["archives/index.html"])
    search_discovery = _discovery_section(pages["search/index.html"])
    library_discovery = _discovery_section(pages["library/index.html"])
    episode_discovery = _discovery_section(
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"]
    )

    assert '<ul class="discovery-list">' in archive_discovery
    assert 'class="discovery-label"' in archive_discovery
    assert 'class="discovery-path">/search/</small>' in archive_discovery
    assert 'href="https://example.com/search/"' in archive_discovery
    assert 'href="https://example.com/library/"' in archive_discovery
    assert 'href="https://example.com/archives/"' not in archive_discovery
    assert '<ul class="discovery-list">' in search_discovery
    assert 'href="https://example.com/archives/"' in search_discovery
    assert 'href="https://example.com/library/"' in search_discovery
    assert 'href="https://example.com/search/"' not in search_discovery
    assert '<ul class="discovery-list">' in library_discovery
    assert 'href="https://example.com/archives/"' in library_discovery
    assert 'href="https://example.com/search/"' in library_discovery
    assert 'href="https://example.com/library/"' not in library_discovery
    assert '<ul class="discovery-list">' in episode_discovery
    assert 'href="https://example.com/archives/"' in episode_discovery
    assert 'href="https://example.com/search/"' in episode_discovery


def test_build_static_site_renders_identity_asset_links_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    homepage_html = pages["index.html"]
    episode_html = pages[
        "sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"
    ]

    assert 'rel="icon" href="https://example.com/favicon.ico"' in homepage_html
    assert (
        'rel="icon" type="image/png" sizes="16x16" '
        'href="https://example.com/favicon-16x16.png"'
    ) in homepage_html
    assert (
        'rel="icon" type="image/png" sizes="32x32" '
        'href="https://example.com/favicon-32x32.png"'
    ) in homepage_html
    assert (
        'rel="apple-touch-icon" type="image/png" '
        'href="https://example.com/apple-touch-icon.png"'
    ) in homepage_html
    assert 'rel="manifest" href="https://example.com/site.webmanifest"' in homepage_html
    assert 'href="https://example.com/apple-touch-icon.png"' in episode_html


def test_build_static_site_renders_open_graph_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    homepage_html = pages["index.html"]
    about_html = pages["about/index.html"]
    saga_html = pages["sagas/hireflow/index.html"]
    episode_html = pages[
        "sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"
    ]

    assert '<meta property="og:title" content="Example" />' in homepage_html
    assert '<meta property="og:description" content="Static site" />' in homepage_html
    assert '<meta property="og:url" content="https://example.com/" />' in homepage_html
    assert '<meta property="og:site_name" content="Example" />' in homepage_html
    assert '<meta property="og:image" content="https://example.com/social-preview.png" />' in homepage_html

    assert '<meta property="og:title" content="About" />' in about_html
    assert (
        '<meta property="og:description" content="Why this site exists and how the work is published in public." />'
        in about_html
    )
    assert '<meta property="og:url" content="https://example.com/about/" />' in about_html
    assert '<meta property="og:image" content="https://example.com/social-preview.png" />' in about_html

    assert '<meta property="og:title" content="HireFlow" />' in saga_html
    assert '<meta property="og:description" content="Architecture in public." />' in saga_html
    assert '<meta property="og:url" content="https://example.com/sagas/hireflow/" />' in saga_html
    assert '<meta property="og:image" content="https://example.com/social-preview.png" />' in saga_html

    assert '<meta property="og:title" content="The First Brick" />' in episode_html
    assert (
        '<meta property="og:description" content="Recent work." />'
        in episode_html
    )
    assert (
        '<meta property="og:url" content="https://example.com/sagas/hireflow/the-origin-blueprint/the-first-brick/" />'
        in episode_html
    )
    assert '<meta property="og:image" content="https://example.com/social-preview.png" />' in episode_html


def test_build_static_site_renders_twitter_card_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    homepage_html = pages["index.html"]
    about_html = pages["about/index.html"]
    saga_html = pages["sagas/hireflow/index.html"]
    episode_html = pages[
        "sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"
    ]

    assert '<meta name="twitter:card" content="summary" />' in homepage_html
    assert '<meta name="twitter:title" content="Example" />' in homepage_html
    assert '<meta name="twitter:description" content="Static site" />' in homepage_html
    assert '<meta name="twitter:url" content="https://example.com/" />' in homepage_html
    assert '<meta name="twitter:image" content="https://example.com/social-preview.png" />' in homepage_html

    assert '<meta name="twitter:title" content="About" />' in about_html
    assert (
        '<meta name="twitter:description" content="Why this site exists and how the work is published in public." />'
        in about_html
    )
    assert '<meta name="twitter:url" content="https://example.com/about/" />' in about_html
    assert '<meta name="twitter:image" content="https://example.com/social-preview.png" />' in about_html

    assert '<meta name="twitter:title" content="HireFlow" />' in saga_html
    assert '<meta name="twitter:description" content="Architecture in public." />' in saga_html
    assert '<meta name="twitter:url" content="https://example.com/sagas/hireflow/" />' in saga_html
    assert '<meta name="twitter:image" content="https://example.com/social-preview.png" />' in saga_html

    assert '<meta name="twitter:title" content="The First Brick" />' in episode_html
    assert (
        '<meta name="twitter:description" content="Recent work." />'
        in episode_html
    )
    assert (
        '<meta name="twitter:url" content="https://example.com/sagas/hireflow/the-origin-blueprint/the-first-brick/" />'
        in episode_html
    )
    assert '<meta name="twitter:image" content="https://example.com/social-preview.png" />' in episode_html


def test_build_static_site_renders_theme_color_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta name="theme-color" content="#0b0b0b" />' in html


def test_build_static_site_renders_format_detection_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta name="format-detection" content="telephone=no" />' in html


def test_build_static_site_renders_referrer_policy_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert (
            '<meta name="referrer" content="strict-origin-when-cross-origin" />'
            in html
        )


def test_build_static_site_renders_color_scheme_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta name="color-scheme" content="dark" />' in html


def test_build_static_site_renders_shared_editorial_shell_tokens() -> None:
    pages = build_static_site(_site_config(), _catalog())

    homepage_html = pages["index.html"]
    about_html = pages["about/index.html"]

    for html in (homepage_html, about_html):
        assert "color-scheme: dark;" in html
        assert "--bg: #000000;" in html
        assert "--surface: #0b0b0b;" in html
        assert "--text-400: #a1a1aa;" in html
        assert 'font-family: ui-monospace, "SFMono-Regular", Menlo, Monaco, Consolas,' in html
        assert "background: var(--bg);" in html
        assert ".site-nav a.active::after {" in html
        assert 'content: "•";' in html
        assert "article pre {" in html
        assert "article code {" in html
        assert 'font-family: Georgia, "Times New Roman", serif;' not in html


def test_build_static_site_renders_application_name_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta name="application-name" content="Example" />' in html


def test_build_static_site_renders_viewport_fit_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert (
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />'
            in html
        )


def test_build_static_site_renders_msapplication_tile_color_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta name="msapplication-TileColor" content="#0b0b0b" />' in html


def test_build_static_site_renders_msapplication_config_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert (
            '<meta name="msapplication-config" content="https://example.com/browserconfig.xml" />'
            in html
        )


def test_build_static_site_renders_author_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta name="author" content="example.com" />' in html


def test_build_static_site_renders_generator_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta name="generator" content="blog-v2 static builder" />' in html


def test_build_static_site_renders_robots_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta name="robots" content="index,follow" />' in html


def test_build_static_site_renders_noindex_robots_metadata_for_not_found_page() -> None:
    pages = build_static_site(_site_config(), _catalog())

    not_found_html = pages["404.html"]

    assert '<meta name="robots" content="noindex,follow" />' in not_found_html
    assert '<meta name="robots" content="index,follow" />' not in not_found_html


def test_build_static_site_renders_mobile_web_app_metadata_in_document_head() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta name="apple-mobile-web-app-capable" content="yes" />' in html
        assert '<meta name="apple-mobile-web-app-title" content="Example" />' in html
        assert (
            '<meta name="apple-mobile-web-app-status-bar-style" content="black" />'
            in html
        )


def test_build_static_site_keeps_twitter_card_type_bounded_to_summary() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta name="twitter:card" content="summary" />' in html


def test_build_static_site_keeps_open_graph_type_bounded_to_website() -> None:
    pages = build_static_site(_site_config(), _catalog())

    route_html = (
        pages["index.html"],
        pages["library/index.html"],
        pages["about/index.html"],
        pages["sagas/hireflow/index.html"],
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"],
    )

    for html in route_html:
        assert '<meta property="og:type" content="website" />' in html


def test_build_static_site_renders_bounded_json_ld_structured_data() -> None:
    pages = build_static_site(_site_config(), _catalog())

    homepage_payloads = _json_ld_payloads(pages["index.html"])
    archives_payloads = _json_ld_payloads(pages["archives/index.html"])
    search_payloads = _json_ld_payloads(pages["search/index.html"])
    library_payloads = _json_ld_payloads(pages["library/index.html"])
    sagas_payloads = _json_ld_payloads(pages["sagas/index.html"])
    studio_payloads = _json_ld_payloads(pages["studio/index.html"])
    about_payloads = _json_ld_payloads(pages["about/index.html"])
    episode_payloads = _json_ld_payloads(
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"]
    )

    assert len(homepage_payloads) == 1
    assert homepage_payloads[0] == {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Example",
        "description": "Static site",
        "url": "https://example.com/",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://example.com/search/?q={search_term_string}",
            "query-input": "required name=search_term_string",
        },
    }

    assert archives_payloads == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Archives",
            "description": "Chronological archive of published writing and saga episodes.",
            "url": "https://example.com/archives/",
        }
    ]
    assert search_payloads == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Search",
            "description": "Search the publication using the static search index.",
            "url": "https://example.com/search/",
        }
    ]
    assert library_payloads == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Library",
            "description": "A section for navigating the site's ideas.",
            "url": "https://example.com/library/",
        }
    ]
    assert sagas_payloads == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Sagas",
            "description": "Browse active sagas and jump into the first episode.",
            "url": "https://example.com/sagas/",
        }
    ]
    assert studio_payloads == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Studio",
            "description": "A section surface for work in public.",
            "url": "https://example.com/studio/",
        }
    ]

    assert len(about_payloads) == 1
    assert about_payloads[0]["@context"] == "https://schema.org"
    assert about_payloads[0]["@type"] == "Article"
    assert about_payloads[0]["headline"] == "About"
    assert about_payloads[0]["description"] == (
        "Why this site exists and how the work is published in public."
    )
    assert about_payloads[0]["datePublished"] == "2026-04-10"
    assert about_payloads[0]["url"] == "https://example.com/about/"
    assert about_payloads[0]["mainEntityOfPage"] == {
        "@type": "WebPage",
        "@id": "https://example.com/about/",
    }
    assert about_payloads[0]["author"] == {
        "@type": "Person",
        "name": "example.com",
    }
    assert about_payloads[0]["publisher"] == {
        "@type": "Organization",
        "name": "Example",
        "url": "https://example.com/",
    }

    assert len(episode_payloads) == 1
    assert episode_payloads[0]["@context"] == "https://schema.org"
    assert episode_payloads[0]["@type"] == "Article"
    assert episode_payloads[0]["headline"] == "The First Brick"
    assert episode_payloads[0]["description"] == "Recent work."
    assert episode_payloads[0]["datePublished"] == "2026-04-12"
    assert episode_payloads[0]["url"] == (
        "https://example.com/sagas/hireflow/the-origin-blueprint/the-first-brick/"
    )


def test_build_static_site_omits_json_ld_for_structural_and_recovery_routes() -> None:
    pages = build_static_site(_site_config(), _catalog())

    assert _json_ld_payloads(pages["404.html"]) == []
    assert _json_ld_payloads(pages["library/architecture/index.html"]) == []
    assert _json_ld_payloads(pages["sagas/hireflow/index.html"]) == []
    assert _json_ld_payloads(pages["sagas/hireflow/the-origin-blueprint/index.html"]) == []


def test_build_static_site_generates_search_index() -> None:
    pages = build_static_site(_site_config(), _catalog())

    search_index = json.loads(pages["search.json"])

    assert search_index[0]["title"] == "Second Iteration"
    assert search_index[0]["url"] == (
        "https://example.com/sagas/hireflow/the-origin-blueprint/second-iteration/"
    )
    assert any(entry["type"] == "saga" and entry["title"] == "HireFlow" for entry in search_index)
    assert any(
        entry["type"] == "arc"
        and entry["context"] == "HireFlow"
        for entry in search_index
    )
    assert any(
        entry["type"] == "page"
        and entry["url"] == "https://example.com/about/"
        for entry in search_index
    )

def _discovery_section(html: str) -> str:
    marker = "          <h2>Other ways in</h2>"
    start = html.index(marker)
    return html[start : html.index("        </section>", start)]


def _json_ld_payloads(html: str) -> list[dict[str, object]]:
    matches = re.findall(
        r'<script type="application/ld\+json">(.+?)</script>',
        html,
        flags=re.DOTALL,
    )
    return [json.loads(match) for match in matches]


def _site_config(*, base_url: str = "https://example.com/") -> SiteConfig:
    return SiteConfig(
        title="Example",
        description="Static site",
        base_url=base_url,
    )


def _catalog() -> ContentCatalog:
    return ContentCatalog(
        pages=(
            Page(
                title="About",
                slug="about",
                summary="Why this site exists and how the work is published in public.",
                date="2026-04-10",
                body_markdown=(
                    "Wasting No Time is a place to make architecture and software "
                    "thinking visible.\n\n"
                    "The goal is simple: publish work that stays concrete, "
                    "testable, and useful.\n\n"
                    "The site currently organizes that work through the homepage, "
                    "saga index, library, archive, and search surfaces so readers "
                    "can move by chronology, topic, or longer narrative thread."
                ),
                tags=("architecture",),
            ),
        ),
        section_pages=(
            SectionPage(
                title="Library",
                slug="library",
                summary="A section for navigating the site's ideas.",
                body_markdown=(
                    "The library is the fastest way to move by idea instead of chronology."
                ),
            ),
            SectionPage(
                title="Studio",
                slug="studio",
                summary="A section surface for work in public.",
                body_markdown=(
                    "Wasting No Time is a studio for architecture, systems thinking, and deliberate experiments."
                ),
            ),
        ),
        sagas=(
            Saga(
                title="HireFlow",
                slug="hireflow",
                summary="Architecture in public.",
                date="2026-04-11",
                status="in-progress",
                body_markdown="Saga body.",
            ),
        ),
        arcs=(
            Arc(
                title="The Origin Blueprint",
                slug="the-origin-blueprint",
                summary="How the saga starts.",
                date="2026-04-11",
                saga_slug="hireflow",
                saga_title="HireFlow",
                body_markdown="Arc body.",
            ),
        ),
        episodes=(
            Episode(
                title="The First Brick",
                slug="the-first-brick",
                summary="Recent work.",
                date="2026-04-12",
                saga_slug="hireflow",
                saga_title="HireFlow",
                arc_slug="the-origin-blueprint",
                arc_title="The Origin Blueprint",
                number=1,
                body_markdown="Episode body.",
                tags=("architecture", "writing"),
            ),
            Episode(
                title="Second Iteration",
                slug="second-iteration",
                summary="Follow-up work.",
                date="2026-04-13",
                saga_slug="hireflow",
                saga_title="HireFlow",
                arc_slug="the-origin-blueprint",
                arc_title="The Origin Blueprint",
                number=2,
                body_markdown="More episode body.",
                tags=("architecture",),
            ),
        ),
    )


def _catalog_with_extra_page() -> ContentCatalog:
    base_catalog = _catalog()
    return ContentCatalog(
        pages=base_catalog.pages
        + (
            Page(
                title="Notes",
                slug="notes",
                summary="Newest standalone page.",
                date="2026-04-14",
                body_markdown="Notes body.",
                tags=("writing",),
            ),
        ),
        section_pages=base_catalog.section_pages,
        sagas=base_catalog.sagas,
        arcs=base_catalog.arcs,
        episodes=base_catalog.episodes,
    )
