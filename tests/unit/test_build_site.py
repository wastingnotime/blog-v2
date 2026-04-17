import json

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

    assert "[episode] Second Iteration" in html
    assert "[episode] The First Brick" in html
    assert "[page] Notes" in html
    assert "[page] About" not in html


def test_build_static_site_renders_arc_page_and_episode_navigation() -> None:
    pages = build_static_site(_site_config(), _catalog())

    arc_html = pages["sagas/hireflow/the-origin-blueprint/index.html"]
    first_episode_html = pages[
        "sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"
    ]
    second_episode_html = pages[
        "sagas/hireflow/the-origin-blueprint/second-iteration/index.html"
    ]

    assert "[Ep 01] The First Brick" in arc_html
    assert "[Ep 02] Second Iteration" in arc_html
    assert "Arc body." in arc_html
    assert "/archives/" in arc_html
    assert "/search/" in arc_html
    assert "HireFlow</a> /" in first_episode_html
    assert "1 min read" in first_episode_html
    assert 'href="https://example.com/library/architecture/"' in first_episode_html
    assert 'href="https://example.com/archives/"' in first_episode_html
    assert 'href="https://example.com/search/"' in first_episode_html
    assert "Ep 02 Second Iteration" in first_episode_html
    assert "Ep 01 The First Brick" in second_episode_html


def test_build_static_site_generates_library_and_topic_pages() -> None:
    pages = build_static_site(_site_config(), _catalog())

    archive_html = pages["archives/index.html"]
    search_html = pages["search/index.html"]
    library_html = pages["library/index.html"]
    topic_html = pages["library/architecture/index.html"]

    assert "Chronological Archive" in archive_html
    assert "[episode] Second Iteration" in archive_html
    assert "[page] About" in archive_html
    assert archive_html.index("[episode] Second Iteration") < archive_html.index("[page] About")
    assert "HireFlow / The Origin Blueprint" in archive_html
    assert "/search/" in archive_html
    assert "/library/" in archive_html
    assert "Search the publication" in search_html
    assert 'type="search"' in search_html
    assert "Enter a query to search the publication." in search_html
    assert "https://example.com/search.json" in search_html
    assert "/archives/" in search_html
    assert "/library/" in search_html
    assert "Topics" in library_html
    assert "The library is the fastest way to move by idea instead of chronology." in library_html
    assert "Other ways in" in library_html
    assert 'href="https://example.com/archives/"' in library_html
    assert 'href="https://example.com/search/"' in library_html
    assert "architecture" in library_html
    assert "[page] About" in topic_html
    assert "[episode] Second Iteration" in topic_html
    assert "HireFlow / The Origin Blueprint" in topic_html
    assert "/archives/" in topic_html
    assert "/search/" in topic_html


def test_build_static_site_generates_section_hub_pages() -> None:
    pages = build_static_site(_site_config(), _catalog())

    sagas_html = pages["sagas/index.html"]
    studio_html = pages["studio/index.html"]

    assert "Active sagas" in sagas_html
    assert "Other ways in" in sagas_html
    assert "HireFlow" in sagas_html
    assert "start reading" in sagas_html
    assert "/archives/" in sagas_html
    assert "/search/" in sagas_html
    assert "/library/" in studio_html
    assert "/sagas/" in studio_html
    assert "/archives/" in studio_html
    assert "/search/" in studio_html
    assert "Other ways in" in studio_html
    assert "Wasting No Time is a studio for architecture" in studio_html


def test_build_static_site_generates_feed_and_sitemap() -> None:
    pages = build_static_site(_site_config(), _catalog())

    nojekyll = pages[".nojekyll"]
    cname = pages["CNAME"]
    not_found_html = pages["404.html"]
    feed_xml = pages["feed.xml"]
    robots_txt = pages["robots.txt"]
    webmanifest = json.loads(pages["site.webmanifest"])
    browserconfig_xml = pages["browserconfig.xml"]
    sitemap_xml = pages["sitemap.xml"]

    assert nojekyll == "\n"
    assert cname == "example.com\n"
    assert "Page Not Found" in not_found_html
    assert "Try one of these instead" in not_found_html
    assert 'href="https://example.com/"' in not_found_html
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
    assert webmanifest["name"] == "Example"
    assert webmanifest["short_name"] == "Example"
    assert webmanifest["start_url"] == "https://example.com/"
    assert webmanifest["display"] == "standalone"
    assert webmanifest["theme_color"] == "#fffdf8"
    assert webmanifest["background_color"] == "#f3efe5"
    assert webmanifest["icons"][0]["src"] == "https://example.com/favicon-16x16.png"
    assert webmanifest["icons"][1]["src"] == "https://example.com/favicon-32x32.png"
    assert webmanifest["icons"][2]["src"] == "https://example.com/apple-touch-icon.png"
    assert "<browserconfig>" in browserconfig_xml
    assert '<square150x150logo src="https://example.com/apple-touch-icon.png"/>' in browserconfig_xml
    assert "<TileColor>#fffdf8</TileColor>" in browserconfig_xml
    assert "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" in sitemap_xml
    assert "<loc>https://example.com/library/</loc>" in sitemap_xml
    assert "<loc>https://example.com/sagas/hireflow/</loc>" in sitemap_xml
    assert "<lastmod>2026-04-13</lastmod>" in sitemap_xml


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
    assert "(c) 2026 example.com - published as a static site" in home_html
    assert "(c) 2026 example.com - published as a static site" in about_html
    assert "(c) 2026 example.com - published as a static site" in saga_html


def test_build_static_site_renders_editorial_homepage_instead_of_status_card() -> None:
    html = build_static_site(_site_config(), _catalog())["index.html"]

    assert "In Public" in html
    assert "This site tracks architecture decisions" in html
    assert "move chronologically through the archives" in html
    assert "search across the publication directly" in html
    assert 'href="https://example.com/search/"' in html
    assert 'href="https://example.com/archives/"' in html
    assert "Active Sagas" in html
    assert "2 episodes · last release 2026-04-13 · in-progress" in html
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
    studio_discovery = _discovery_section(pages["studio/index.html"])
    episode_discovery = _discovery_section(
        pages["sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"]
    )

    assert 'href="https://example.com/search/"' in archive_discovery
    assert 'href="https://example.com/library/"' in archive_discovery
    assert 'href="https://example.com/archives/"' not in archive_discovery
    assert 'href="https://example.com/archives/"' in search_discovery
    assert 'href="https://example.com/library/"' in search_discovery
    assert 'href="https://example.com/search/"' not in search_discovery
    assert 'href="https://example.com/archives/"' in library_discovery
    assert 'href="https://example.com/search/"' in library_discovery
    assert 'href="https://example.com/library/"' not in library_discovery
    assert 'href="https://example.com/sagas/"' in studio_discovery
    assert 'href="https://example.com/library/"' in studio_discovery
    assert 'href="https://example.com/archives/"' in studio_discovery
    assert 'href="https://example.com/search/"' in studio_discovery
    assert 'href="https://example.com/studio/"' not in studio_discovery
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
        assert '<meta name="theme-color" content="#fffdf8" />' in html


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
        assert '<meta name="color-scheme" content="light" />' in html


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
        assert '<meta name="msapplication-TileColor" content="#fffdf8" />' in html


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
            '<meta name="apple-mobile-web-app-status-bar-style" content="default" />'
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


def _site_config() -> SiteConfig:
    return SiteConfig(
        title="Example",
        description="Static site",
        base_url="https://example.com/",
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
