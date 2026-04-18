import json
from pathlib import Path
import re

from src.app.application.use_cases.load_content_catalog import load_content_catalog
from src.app.interfaces.cli.run_scenario import load_site_config
from src.app.infrastructure.builders.static_site_builder import StaticSiteBuilder
from src.app.infrastructure.content.markdown_content_loader import MarkdownContentLoader


def test_static_site_builder_generates_static_routes_from_markdown(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "dist"
    identity_assets_dir = Path(__file__).resolve().parents[2] / "assets" / "site" / "current"
    content_root = Path(__file__).resolve().parents[2] / "content"
    builder = StaticSiteBuilder(
        output_dir=output_dir,
        identity_assets_dir=identity_assets_dir,
    )
    catalog = load_content_catalog(
        loader=MarkdownContentLoader(),
        content_root=content_root,
    )

    written_paths = builder.build(load_site_config(), catalog)

    expected_paths = {
        output_dir / ".nojekyll",
        output_dir / "CNAME",
        output_dir / "404.html",
        output_dir / "index.html",
        output_dir / "opensearch.xml",
        output_dir / "archives" / "index.html",
        output_dir / "feed.xml",
        output_dir / "robots.txt",
        output_dir / "search" / "index.html",
        output_dir / "search.json",
        output_dir / "browserconfig.xml",
        output_dir / "site.webmanifest",
        output_dir / "sitemap.xml",
        output_dir / "favicon.ico",
        output_dir / "favicon-16x16.png",
        output_dir / "favicon-32x32.png",
        output_dir / "apple-touch-icon.png",
        output_dir / "social-preview.png",
        output_dir / "about" / "index.html",
        output_dir / "library" / "index.html",
        output_dir / "library" / "architecture" / "index.html",
        output_dir / "sagas" / "index.html",
        output_dir / "sagas" / "hireflow" / "index.html",
        output_dir / "sagas" / "hireflow" / "the-origin-blueprint" / "index.html",
        output_dir / "studio" / "index.html",
        output_dir
        / "sagas"
        / "hireflow"
        / "the-origin-blueprint"
        / "the-first-brick"
        / "index.html",
    }

    assert expected_paths.issubset(set(written_paths))

    nojekyll = (output_dir / ".nojekyll").read_text(encoding="utf-8")
    cname = (output_dir / "CNAME").read_text(encoding="utf-8")
    not_found_html = (output_dir / "404.html").read_text(encoding="utf-8")
    homepage_html = (output_dir / "index.html").read_text(encoding="utf-8")
    archive_html = (
        output_dir / "archives" / "index.html"
    ).read_text(encoding="utf-8")
    search_html = (
        output_dir / "search" / "index.html"
    ).read_text(encoding="utf-8")
    library_html = (output_dir / "library" / "index.html").read_text(encoding="utf-8")
    topic_html = (
        output_dir / "library" / "architecture" / "index.html"
    ).read_text(encoding="utf-8")
    sagas_index_html = (
        output_dir / "sagas" / "index.html"
    ).read_text(encoding="utf-8")
    saga_html = (
        output_dir / "sagas" / "hireflow" / "index.html"
    ).read_text(encoding="utf-8")
    arc_html = (
        output_dir / "sagas" / "hireflow" / "the-origin-blueprint" / "index.html"
    ).read_text(encoding="utf-8")
    about_html = (output_dir / "about" / "index.html").read_text(encoding="utf-8")
    feed_xml = (output_dir / "feed.xml").read_text(encoding="utf-8")
    robots_txt = (output_dir / "robots.txt").read_text(encoding="utf-8")
    opensearch_xml = (output_dir / "opensearch.xml").read_text(encoding="utf-8")
    search_json = (output_dir / "search.json").read_text(encoding="utf-8")
    browserconfig_xml = (output_dir / "browserconfig.xml").read_text(encoding="utf-8")
    webmanifest = json.loads(
        (output_dir / "site.webmanifest").read_text(encoding="utf-8")
    )
    sitemap_xml = (output_dir / "sitemap.xml").read_text(encoding="utf-8")
    studio_html = (
        output_dir / "studio" / "index.html"
    ).read_text(encoding="utf-8")
    episode_html = (
        output_dir
        / "sagas"
        / "hireflow"
        / "the-origin-blueprint"
        / "the-first-brick"
        / "index.html"
    ).read_text(encoding="utf-8")

    assert nojekyll == "\n"
    assert cname == "wastingnotime.org\n"
    assert "In Public" in homepage_html
    assert "This site tracks architecture decisions" in homepage_html
    assert "move chronologically through the archives" in homepage_html
    assert "search across the publication directly" in homepage_html
    assert 'class="active">Home</a>' in homepage_html
    assert 'href="https://wastingnotime.org/search/"' in homepage_html
    assert 'href="https://wastingnotime.org/archives/"' in homepage_html
    assert 'href="https://wastingnotime.org/about/"' in homepage_html
    assert 'href="https://wastingnotime.org/library/"' in homepage_html
    assert 'href="https://wastingnotime.org/sagas/"' in homepage_html
    assert 'href="https://wastingnotime.org/feed.xml"' in homepage_html
    assert 'rel="alternate" type="application/rss+xml" title="Wasting No Time RSS" href="https://wastingnotime.org/feed.xml"' in homepage_html
    assert (
        'rel="search" type="application/opensearchdescription+xml" '
        'title="Wasting No Time Search" href="https://wastingnotime.org/opensearch.xml"'
        in homepage_html
    )
    assert 'href="https://wastingnotime.org/favicon.ico"' in homepage_html
    assert 'href="https://wastingnotime.org/apple-touch-icon.png"' in homepage_html
    assert 'rel="manifest" href="https://wastingnotime.org/site.webmanifest"' in homepage_html
    assert (
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />'
        in homepage_html
    )
    assert '<meta name="generator" content="blog-v2 static builder" />' in homepage_html
    assert '<meta name="author" content="wastingnotime.org" />' in homepage_html
    assert '<meta name="application-name" content="Wasting No Time" />' in homepage_html
    assert '<meta name="color-scheme" content="light" />' in homepage_html
    assert (
        '<meta name="referrer" content="strict-origin-when-cross-origin" />'
        in homepage_html
    )
    assert '<meta name="format-detection" content="telephone=no" />' in homepage_html
    assert '<meta name="theme-color" content="#fffdf8" />' in homepage_html
    assert '<meta name="msapplication-TileColor" content="#fffdf8" />' in homepage_html
    assert (
        '<meta name="msapplication-config" content="https://wastingnotime.org/browserconfig.xml" />'
        in homepage_html
    )
    assert '<meta name="apple-mobile-web-app-capable" content="yes" />' in homepage_html
    assert '<meta name="apple-mobile-web-app-title" content="Wasting No Time" />' in homepage_html
    assert '<meta name="apple-mobile-web-app-status-bar-style" content="default" />' in homepage_html
    assert '<meta name="robots" content="index,follow" />' in homepage_html
    assert '<meta name="robots" content="noindex,follow" />' in not_found_html
    assert '<meta name="robots" content="index,follow" />' not in not_found_html
    assert '<meta property="og:title" content="Wasting No Time" />' in homepage_html
    assert (
        '<meta property="og:description" content="blog-v2 starts from a simpler contract: static output, GitHub Pages deployment, and no first-party /api dependency." />'
        in homepage_html
    )
    assert '<meta property="og:url" content="https://wastingnotime.org/" />' in homepage_html
    assert '<meta property="og:type" content="website" />' in homepage_html
    assert '<meta property="og:site_name" content="Wasting No Time" />' in homepage_html
    assert '<meta property="og:image" content="https://wastingnotime.org/social-preview.png" />' in homepage_html
    assert '<meta name="twitter:card" content="summary" />' in homepage_html
    assert '<meta name="twitter:title" content="Wasting No Time" />' in homepage_html
    assert (
        '<meta name="twitter:description" content="blog-v2 starts from a simpler contract: static output, GitHub Pages deployment, and no first-party /api dependency." />'
        in homepage_html
    )
    assert '<meta name="twitter:url" content="https://wastingnotime.org/" />' in homepage_html
    assert '<meta name="twitter:image" content="https://wastingnotime.org/social-preview.png" />' in homepage_html
    homepage_structured_data = _json_ld_payloads(homepage_html)
    assert homepage_structured_data == [
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Wasting No Time",
            "description": (
                "blog-v2 starts from a simpler contract: static output, GitHub "
                "Pages deployment, and no first-party /api dependency."
            ),
            "url": "https://wastingnotime.org/",
            "potentialAction": {
                "@type": "SearchAction",
                "target": "https://wastingnotime.org/search/?q={search_term_string}",
                "query-input": "required name=search_term_string",
            },
        }
    ]
    assert "(c) 2025 wastingnotime.org - published as a static site" in homepage_html
    assert "3 recent entries shown" in homepage_html
    assert "2 episodes · last release 2025-11-15 · in-progress" in homepage_html
    assert (output_dir / "sagas" / "hireflow" / "index.html").exists()
    assert "/api/event" not in homepage_html
    assert "Deployment target:" not in homepage_html
    assert "Page Not Found" in not_found_html
    assert "Try one of these instead" in not_found_html
    assert 'href="https://wastingnotime.org/"' in not_found_html
    assert 'href="https://wastingnotime.org/search/"' in not_found_html
    assert 'href="https://wastingnotime.org/archives/"' in not_found_html
    assert 'href="https://wastingnotime.org/sagas/"' in not_found_html
    assert 'href="https://wastingnotime.org/library/"' in not_found_html
    assert "/api/event" not in not_found_html
    assert _json_ld_payloads(not_found_html) == []
    assert "Chronological Archive" in archive_html
    assert 'class="active">Archives</a>' in archive_html
    assert "[episode] Second Iteration" in archive_html
    assert "[page] About" in archive_html
    assert archive_html.index("[episode] Second Iteration") < archive_html.index("[page] About")
    assert "HireFlow / The Origin Blueprint" in archive_html
    assert "/search/" in archive_html
    assert "/library/" in archive_html
    assert "/api/event" not in archive_html
    assert _json_ld_payloads(archive_html) == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Archives",
            "description": "Chronological archive of published writing and saga episodes.",
            "url": "https://wastingnotime.org/archives/",
        }
    ]
    assert "Search the publication" in search_html
    assert 'class="active">Search</a>' in search_html
    assert 'id="search-form"' in search_html
    assert 'method="get"' in search_html
    assert 'action="https://wastingnotime.org/search/"' in search_html
    assert 'type="search"' in search_html
    assert 'name="q"' in search_html
    assert "Enter a query to search the publication." in search_html
    assert "https://wastingnotime.org/search.json" in search_html
    assert "new URLSearchParams(window.location.search).get('q') ?? ''" in search_html
    assert "const normalizeSearchText = (value) => (value || '').trim().toLowerCase();" in search_html
    assert "const projectSearchUrlState = (query) => {" in search_html
    assert "const scoreSearchRecord = (record, normalizedQuery) => {" in search_html
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
    assert "nextUrl.searchParams.set('q', normalizedQuery);" in search_html
    assert "nextUrl.searchParams.delete('q');" in search_html
    assert "window.history.replaceState(null, '', nextPath);" in search_html
    assert "searchForm.addEventListener('submit', (event) => {" in search_html
    assert "searchInput.value = initialQuery;" in search_html
    assert "renderResults(searchInput.value);" in search_html
    assert "projectSearchUrlState(event.target.value);" in search_html
    assert '<meta name="robots" content="noindex,follow" />' in search_html
    assert '<meta name="robots" content="index,follow" />' not in search_html
    assert '<link rel="canonical" href="https://wastingnotime.org/search/" />' in search_html
    assert "/archives/" in search_html
    assert "/library/" in search_html
    assert "/api/event" not in search_html
    assert _json_ld_payloads(search_html) == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Search",
            "description": "Search the publication using the static search index.",
            "url": "https://wastingnotime.org/search/",
        }
    ]
    assert "<rss version=\"2.0\">" in feed_xml
    assert "<link>https://wastingnotime.org/sagas/hireflow/the-origin-blueprint/second-iteration/</link>" in feed_xml
    assert "<title>About</title>" in feed_xml
    assert "/api/event" not in feed_xml
    assert "User-agent: *" in robots_txt
    assert "Allow: /" in robots_txt
    assert "Sitemap: https://wastingnotime.org/sitemap.xml" in robots_txt
    assert "/api/event" not in robots_txt
    assert (
        '<OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">'
        in opensearch_xml
    )
    assert "<ShortName>Wasting No Time</ShortName>" in opensearch_xml
    assert (
        "<Description>blog-v2 starts from a simpler contract: static output, GitHub "
        "Pages deployment, and no first-party /api dependency.</Description>"
        in opensearch_xml
    )
    assert (
        'template="https://wastingnotime.org/search/?q={searchTerms}"'
        in opensearch_xml
    )
    assert "/api/event" not in opensearch_xml
    assert "<browserconfig>" in browserconfig_xml
    assert (
        '<square150x150logo src="https://wastingnotime.org/apple-touch-icon.png"/>'
        in browserconfig_xml
    )
    assert "<TileColor>#fffdf8</TileColor>" in browserconfig_xml
    assert webmanifest["name"] == "Wasting No Time"
    assert webmanifest["short_name"] == "Wasting No Time"
    assert webmanifest["start_url"] == "https://wastingnotime.org/"
    assert webmanifest["theme_color"] == "#fffdf8"
    assert webmanifest["background_color"] == "#f3efe5"
    assert webmanifest["icons"][0]["src"] == "https://wastingnotime.org/favicon-16x16.png"
    assert webmanifest["icons"][1]["src"] == "https://wastingnotime.org/favicon-32x32.png"
    assert webmanifest["icons"][2]["src"] == "https://wastingnotime.org/apple-touch-icon.png"
    assert "/api/event" not in json.dumps(webmanifest)
    search_index = json.loads(search_json)
    assert any(entry["title"] == "About" for entry in search_index)
    assert any(entry["title"] == "HireFlow" and entry["type"] == "saga" for entry in search_index)
    assert any(
        entry["title"] == "Second Iteration"
        and entry["url"] == "https://wastingnotime.org/sagas/hireflow/the-origin-blueprint/second-iteration/"
        for entry in search_index
    )
    assert "/api/event" not in search_json
    assert "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" in sitemap_xml
    assert "<loc>https://wastingnotime.org/</loc>" in sitemap_xml
    assert "<loc>https://wastingnotime.org/archives/</loc>" in sitemap_xml
    assert "<loc>https://wastingnotime.org/library/architecture/</loc>" in sitemap_xml
    assert "<lastmod>2025-11-15</lastmod>" in sitemap_xml
    assert "https://wastingnotime.org/search/" not in sitemap_xml
    assert "Topics" in library_html
    assert "The library is the fastest way to move by idea instead of chronology." in library_html
    assert 'class="active">Library</a>' in library_html
    assert "Other ways in" in library_html
    assert 'href="https://wastingnotime.org/archives/"' in library_html
    assert 'href="https://wastingnotime.org/search/"' in library_html
    assert "architecture" in library_html
    assert _json_ld_payloads(library_html) == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Library",
            "description": (
                "An authored index for navigating the site's ideas and implementation threads."
            ),
            "url": "https://wastingnotime.org/library/",
        }
    ]
    assert "[page] About" in topic_html
    assert "[episode] Second Iteration" in topic_html
    assert "/archives/" in topic_html
    assert "/search/" in topic_html
    assert _json_ld_payloads(topic_html) == []
    assert "Active sagas" in sagas_index_html
    assert 'class="active">Sagas</a>' in sagas_index_html
    assert "Other ways in" in sagas_index_html
    assert "start reading" in sagas_index_html
    assert "/archives/" in sagas_index_html
    assert "/search/" in sagas_index_html
    assert _json_ld_payloads(sagas_index_html) == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Sagas",
            "description": "Browse active sagas and jump into the first episode.",
            "url": "https://wastingnotime.org/sagas/",
        }
    ]
    assert "Timeline" in saga_html
    assert 'class="active">Sagas</a>' in saga_html
    assert 'href="https://wastingnotime.org/feed.xml"' in saga_html
    assert 'rel="alternate" type="application/rss+xml" title="Wasting No Time RSS" href="https://wastingnotime.org/feed.xml"' in saga_html
    assert '<meta property="og:title" content="HireFlow" />' in saga_html
    assert (
        '<meta property="og:description" content="A fictional hiring platform used as a laboratory for architecture trade-offs and emergent design." />'
        in saga_html
    )
    assert '<meta property="og:url" content="https://wastingnotime.org/sagas/hireflow/" />' in saga_html
    assert '<meta property="og:type" content="website" />' in saga_html
    assert '<meta property="og:image" content="https://wastingnotime.org/social-preview.png" />' in saga_html
    assert '<meta name="apple-mobile-web-app-title" content="Wasting No Time" />' in saga_html
    assert '<meta name="twitter:card" content="summary" />' in saga_html
    assert '<meta name="twitter:title" content="HireFlow" />' in saga_html
    assert (
        '<meta name="twitter:description" content="A fictional hiring platform used as a laboratory for architecture trade-offs and emergent design." />'
        in saga_html
    )
    assert '<meta name="twitter:url" content="https://wastingnotime.org/sagas/hireflow/" />' in saga_html
    assert '<meta name="twitter:image" content="https://wastingnotime.org/social-preview.png" />' in saga_html
    assert "(c) 2025 wastingnotime.org - published as a static site" in saga_html
    assert "The Origin Blueprint" in saga_html
    assert "HireFlow is the working saga for exploring what architecture decisions look like" in saga_html
    assert "/archives/" in saga_html
    assert "/search/" in saga_html
    assert _json_ld_payloads(saga_html) == []
    assert "Episodes" in arc_html
    assert "/archives/" in arc_html
    assert "/search/" in arc_html
    assert "[Ep 01] The First Brick" in arc_html
    assert "The opening arc defines why HireFlow exists" in arc_html
    assert _json_ld_payloads(arc_html) == []
    assert "Why this site exists" in about_html
    assert 'class="active">About</a>' in about_html
    assert 'href="https://wastingnotime.org/feed.xml"' in about_html
    assert 'rel="alternate" type="application/rss+xml" title="Wasting No Time RSS" href="https://wastingnotime.org/feed.xml"' in about_html
    assert '<meta property="og:title" content="About" />' in about_html
    assert (
        '<meta property="og:description" content="Why this site exists and how the work is published in public." />'
        in about_html
    )
    assert '<meta property="og:url" content="https://wastingnotime.org/about/" />' in about_html
    assert '<meta property="og:type" content="website" />' in about_html
    assert '<meta property="og:image" content="https://wastingnotime.org/social-preview.png" />' in about_html
    assert '<meta name="apple-mobile-web-app-title" content="Wasting No Time" />' in about_html
    assert '<meta name="twitter:card" content="summary" />' in about_html
    assert '<meta name="twitter:title" content="About" />' in about_html
    assert (
        '<meta name="twitter:description" content="Why this site exists and how the work is published in public." />'
        in about_html
    )
    assert '<meta name="twitter:url" content="https://wastingnotime.org/about/" />' in about_html
    assert '<meta name="twitter:image" content="https://wastingnotime.org/social-preview.png" />' in about_html
    about_structured_data = _json_ld_payloads(about_html)
    assert len(about_structured_data) == 1
    assert about_structured_data[0]["@context"] == "https://schema.org"
    assert about_structured_data[0]["@type"] == "Article"
    assert about_structured_data[0]["headline"] == "About"
    assert about_structured_data[0]["description"] == (
        "Why this site exists and how the work is published in public."
    )
    assert about_structured_data[0]["datePublished"] == "2025-10-25"
    assert about_structured_data[0]["url"] == "https://wastingnotime.org/about/"
    assert "(c) 2025 wastingnotime.org - published as a static site" in about_html
    assert "1 min read" in about_html
    assert "homepage, saga index, library, archive, and search surfaces" in about_html
    assert "how to reach me" not in about_html
    assert 'href="https://wastingnotime.org/archives/"' in about_html
    assert 'href="https://wastingnotime.org/search/"' in about_html
    assert 'href="https://wastingnotime.org/library/architecture/"' in about_html
    assert 'href="https://wastingnotime.org/favicon-32x32.png"' in about_html
    assert "/sagas/" in studio_html
    assert "/library/" in studio_html
    assert "/archives/" in studio_html
    assert "/search/" in studio_html
    assert "Other ways in" in studio_html
    assert "Wasting No Time is a studio for architecture" in studio_html
    assert 'class="active">Studio</a>' in studio_html
    assert _json_ld_payloads(studio_html) == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Studio",
            "description": (
                "A section surface for the work, systems, and experiments evolving in public."
            ),
            "url": "https://wastingnotime.org/studio/",
        }
    ]
    assert "HireFlow / The Origin Blueprint" in episode_html
    assert "1 min read" in episode_html
    assert 'href="https://wastingnotime.org/library/distributed-systems/"' in episode_html
    assert 'href="https://wastingnotime.org/archives/"' in episode_html
    assert 'href="https://wastingnotime.org/search/"' in episode_html
    assert "Other ways in" in episode_html
    assert 'href="https://wastingnotime.org/favicon-16x16.png"' in episode_html
    assert '<meta property="og:title" content="The First Brick" />' in episode_html
    assert (
        '<meta property="og:description" content="We explore why HireFlow exists, what it will simulate, and how the architecture will emerge through iterative design." />'
        in episode_html
    )
    assert (
        '<meta property="og:url" content="https://wastingnotime.org/sagas/hireflow/the-origin-blueprint/the-first-brick/" />'
        in episode_html
    )
    assert '<meta property="og:type" content="website" />' in episode_html
    assert '<meta property="og:image" content="https://wastingnotime.org/social-preview.png" />' in episode_html
    assert '<meta name="apple-mobile-web-app-title" content="Wasting No Time" />' in episode_html
    assert '<meta name="twitter:card" content="summary" />' in episode_html
    assert '<meta name="twitter:title" content="The First Brick" />' in episode_html
    assert (
        '<meta name="twitter:description" content="We explore why HireFlow exists, what it will simulate, and how the architecture will emerge through iterative design." />'
        in episode_html
    )
    assert (
        '<meta name="twitter:url" content="https://wastingnotime.org/sagas/hireflow/the-origin-blueprint/the-first-brick/" />'
        in episode_html
    )
    assert '<meta name="twitter:image" content="https://wastingnotime.org/social-preview.png" />' in episode_html
    episode_structured_data = _json_ld_payloads(episode_html)
    assert len(episode_structured_data) == 1
    assert episode_structured_data[0]["@context"] == "https://schema.org"
    assert episode_structured_data[0]["@type"] == "Article"
    assert episode_structured_data[0]["headline"] == "The First Brick"
    assert episode_structured_data[0]["description"] == (
        "We explore why HireFlow exists, what it will simulate, and how "
        "the architecture will emerge through iterative design."
    )
    assert episode_structured_data[0]["datePublished"] == "2025-11-14"
    assert episode_structured_data[0]["url"] == (
        "https://wastingnotime.org/sagas/hireflow/the-origin-blueprint/the-first-brick/"
    )
    assert "Ep 02 Second Iteration" in episode_html
    assert "/api/event" not in episode_html
    assert (output_dir / "favicon.ico").read_bytes() == (
        identity_assets_dir / "favicon.ico"
    ).read_bytes()
    assert (output_dir / "social-preview.png").read_bytes() == (
        identity_assets_dir / "social-preview.png"
    ).read_bytes()


def test_static_site_builder_uses_prefixed_base_url_for_search_form_action(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setenv("SITE_BASE_URL", "https://example.com/blog/")
    output_dir = tmp_path / "dist"
    identity_assets_dir = Path(__file__).resolve().parents[2] / "assets" / "site" / "current"
    content_root = Path(__file__).resolve().parents[2] / "content"
    builder = StaticSiteBuilder(
        output_dir=output_dir,
        identity_assets_dir=identity_assets_dir,
    )
    catalog = load_content_catalog(
        loader=MarkdownContentLoader(),
        content_root=content_root,
    )

    builder.build(load_site_config(), catalog)

    search_html = (
        output_dir / "search" / "index.html"
    ).read_text(encoding="utf-8")

    assert 'action="https://example.com/blog/search/"' in search_html
    assert 'action="/search/"' not in search_html
    assert '<link rel="canonical" href="https://example.com/blog/search/" />' in search_html
    assert "https://example.com/blog/search.json" in search_html


def _json_ld_payloads(html: str) -> list[dict[str, object]]:
    matches = re.findall(
        r'<script type="application/ld\+json">(.+?)</script>',
        html,
        flags=re.DOTALL,
    )
    return [json.loads(match) for match in matches]
