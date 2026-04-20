import json
from pathlib import Path
import re

from src.app.application.use_cases.legacy_arc_pages import render_legacy_arc_page
from src.app.application.use_cases.legacy_homepage_render import render_legacy_homepage
from src.app.application.use_cases.legacy_episode_pages import render_legacy_episode_page
from src.app.application.use_cases.legacy_saga_pages import render_legacy_saga_page
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
    assert cname == "blog.wastingnotime.org\n"
    assert homepage_html == render_legacy_homepage()
    assert '<meta name="robots" content="index,follow" />' not in homepage_html
    assert '<meta name="robots" content="noindex,follow" />' in not_found_html
    assert _json_ld_payloads(homepage_html) == []
    assert (output_dir / "sagas" / "hireflow" / "index.html").exists()
    assert "/api/event" not in homepage_html
    assert "Deployment target:" not in homepage_html
    assert "Page Not Found" in not_found_html
    assert "Try one of these instead" in not_found_html
    assert '<ul class="not-found-list">' in not_found_html
    assert '<div class="not-found-row">' in not_found_html
    assert '<a class="not-found-link" href="/">Return home</a>' in not_found_html
    assert '<small class="not-found-path">/</small>' in not_found_html
    assert 'href="/search/"' in not_found_html
    assert 'href="/archives/"' in not_found_html
    assert 'href="/sagas/"' in not_found_html
    assert 'href="/library/"' in not_found_html
    assert ".not-found-row {" in not_found_html
    assert "/api/event" not in not_found_html
    assert _json_ld_payloads(not_found_html) == []
    assert "Chronological Archive" in archive_html
    assert 'class="site-nav-link active" aria-current="page">ARCHIVES</a>' in archive_html
    assert '<ul class="archive-entry-list">' in archive_html
    assert '<div class="archive-entry-row">' in archive_html
    assert '<a class="archive-entry-link" href="/sagas/hireflow/the-origin-blueprint/architecture-diagram-and-narrative/">[episode] Architecture Diagram &amp; Narrative</a>' in archive_html
    assert 'class="archive-entry-meta">2025-12-29 · HireFlow / The Origin Blueprint</small>' in archive_html
    assert 'class="archive-entry-summary">We consolidate the Origin Blueprint into a coherent MVP architecture. This episode presents the system map, explains the architectural intent, and defines what ‘done’ means for Hireflow’s first milestone.</p>' in archive_html
    assert "[episode] Architecture Diagram &amp; Narrative" in archive_html
    assert "[page] About" in archive_html
    assert archive_html.index("[episode] Architecture Diagram &amp; Narrative") < archive_html.index("[page] About")
    assert "HireFlow / The Origin Blueprint" in archive_html
    assert '<ul class="discovery-list">' in archive_html
    assert '<a class="discovery-label" href="/search/">Search across the publication</a>' in archive_html
    assert '<small class="discovery-path">/search/</small>' in archive_html
    assert "/search/" in archive_html
    assert "/library/" in archive_html
    assert ".archive-entry-row {" in archive_html
    assert "/api/event" not in archive_html
    assert _json_ld_payloads(archive_html) == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Archives",
            "description": "Chronological archive of published writing and saga episodes.",
            "url": "https://blog.wastingnotime.org/archives/",
        }
    ]
    assert "Search the publication" in search_html
    assert 'class="site-nav-link active" aria-current="page">SEARCH</a>' in search_html
    assert 'id="search-form"' in search_html
    assert 'method="get"' in search_html
    assert 'action="/search/"' in search_html
    assert '<label class="search-query-label" for="search-query">Search query</label>' in search_html
    assert '<input class="search-query-input" id="search-query"' in search_html
    assert '<p id="search-helper">Type to filter the static index published with the site.</p>' in search_html
    assert 'aria-describedby="search-helper search-status"' in search_html
    assert 'aria-description="Search titles, summaries, and topics."' in search_html
    assert '<button class="search-submit-button" type="submit">Search</button>' in search_html
    assert 'type="search"' in search_html
    assert 'name="q"' in search_html
    assert "<noscript>" in search_html
    assert '<div class="search-noscript-recovery">' in search_html
    assert "Live search on this page requires JavaScript." in search_html
    assert "browse the chronology or move by topic instead." in search_html
    assert '<a class="search-noscript-recovery-link" href="/archives/">Browse the archives</a>' in search_html
    assert '<small class="search-noscript-recovery-path">/archives/</small>' in search_html
    assert 'id="search-status" role="status" aria-live="polite" aria-atomic="true"' in search_html
    assert '<h3 id="search-results-heading" class="visually-hidden">Search results</h3>' in search_html
    assert 'id="search-results" class="search-result-list" aria-labelledby="search-results-heading"' in search_html
    assert "Enter a query to search the publication." in search_html
    assert "/search.json" in search_html
    assert "new URLSearchParams(window.location.search).get('q') ?? ''" in search_html
    assert "const normalizeSearchText = (value) => (value || '').trim().toLowerCase();" in search_html
    assert "const projectSearchUrlState = (query) => {" in search_html
    assert "const scoreSearchRecord = (record, normalizedQuery) => {" in search_html
    assert "const createHighlightedFragment = (value, normalizedQuery) => {" in search_html
    assert "const searchRecovery = document.createElement('div');" in search_html
    assert "searchRecovery.className = 'search-empty-recovery';" in search_html
    assert "const createSearchRecoveryRow = (label, path) => {" in search_html
    assert "searchRecovery.className = 'search-load-recovery';" in search_html
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
    assert "message.className = 'search-empty-recovery-message';" in search_html
    assert "message.textContent = `No results for \"${query}\". Try these routes instead.`;" in search_html
    assert "searchRecovery.appendChild(createSearchRecoveryRow('the archives'," in search_html
    assert "searchRecovery.appendChild(createSearchRecoveryRow('the library'," in search_html
    assert "searchResults.appendChild(searchRecovery);" in search_html
    assert "Search index could not be loaded." in search_html
    assert "message.className = 'search-load-recovery-message';" in search_html
    assert "Search index is unavailable right now. Try these routes instead." in search_html
    assert "search-empty-recovery-row" in search_html
    assert "search-empty-recovery-link" in search_html
    assert "search-empty-recovery-path" in search_html
    assert "search-load-recovery-message" in search_html
    assert ".search-result-list {" in search_html
    assert ".search-query-label {" in search_html
    assert 'class="search-submit-button"' in search_html
    assert ".visually-hidden {" in search_html
    assert ".search-result-item {" in search_html
    assert ".search-result-header {" in search_html
    assert ".search-result-link {" in search_html
    assert ".search-result-meta {" in search_html
    assert ".search-result-summary {" in search_html
    assert ".search-result-tags {" in search_html
    assert ".search-result-tag-chip {" in search_html
    assert "padding: 0;" in search_html
    assert "border: 0;" in search_html
    assert "background: transparent;" in search_html
    assert "link.appendChild(document.createTextNode(`[${record.type}] `));" in search_html
    assert "item.className = 'search-result-item';" in search_html
    assert "header.className = 'search-result-header';" in search_html
    assert "link.className = 'search-result-link';" in search_html
    assert "meta.className = 'search-result-meta';" in search_html
    assert "summary.className = 'search-result-summary';" in search_html
    assert "tags.className = 'search-result-tags';" in search_html
    assert "link.appendChild(createHighlightedFragment(record.title, normalizedQuery));" in search_html
    assert "meta.appendChild(createHighlightedFragment(record.context, normalizedQuery));" in search_html
    assert "summary.appendChild(createHighlightedFragment(record.summary, normalizedQuery));" in search_html
    assert "if ((record.tags || []).length) {" in search_html
    assert "const chip = document.createElement('span');" in search_html
    assert "chip.className = 'search-result-tag-chip';" in search_html
    assert "chip.appendChild(document.createTextNode('#'));" in search_html
    assert "record.tags.forEach((tag) => {" in search_html
    assert "chip.appendChild(createHighlightedFragment(tag, normalizedQuery));" in search_html
    assert "tags.appendChild(chip);" in search_html
    assert "nextUrl.searchParams.set('q', normalizedQuery);" in search_html
    assert "nextUrl.searchParams.delete('q');" in search_html
    assert "window.history.replaceState(null, '', nextPath);" in search_html
    assert "projectSearchUrlState(searchInput.value);" in search_html
    assert "searchForm.addEventListener('submit', (event) => {" in search_html
    assert "searchInput.value = initialQuery;" in search_html
    assert "renderResults(searchInput.value);" in search_html
    assert "projectSearchUrlState(event.target.value);" in search_html
    assert '<meta name="robots" content="noindex,follow" />' in search_html
    assert '<meta name="robots" content="index,follow" />' not in search_html
    assert '<link rel="canonical" href="https://blog.wastingnotime.org/search/" />' in search_html
    assert "/archives/" in search_html
    assert "/library/" in search_html
    assert 'href="/archives/"' in search_html
    assert 'href="/library/"' in search_html
    assert "/api/event" not in search_html
    assert _json_ld_payloads(search_html) == [
        {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Search",
            "description": "Search the publication using the static search index.",
            "url": "https://blog.wastingnotime.org/search/",
        }
    ]
    assert "<rss version=\"2.0\">" in feed_xml
    assert "<title>wasting no time</title>" in feed_xml
    assert "<description>Latest posts and episodes from wasting no time</description>" in feed_xml
    assert "<link>https://blog.wastingnotime.org/sagas/hireflow/the-origin-blueprint/architecture-diagram-and-narrative/</link>" in feed_xml
    assert "<title>Architecture Diagram &amp; Narrative</title>" in feed_xml
    assert "/api/event" not in feed_xml
    assert "User-agent: *" in robots_txt
    assert "Allow: /" in robots_txt
    assert "Sitemap: https://blog.wastingnotime.org/sitemap.xml" in robots_txt
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
        'template="https://blog.wastingnotime.org/search/?q={searchTerms}"'
        in opensearch_xml
    )
    assert "/api/event" not in opensearch_xml
    assert "<browserconfig>" in browserconfig_xml
    assert (
        '<square150x150logo src="/apple-touch-icon.png"/>'
        in browserconfig_xml
    )
    assert "<TileColor>#000000</TileColor>" in browserconfig_xml
    assert webmanifest["name"] == "Wasting No Time"
    assert webmanifest["short_name"] == "Wasting No Time"
    assert webmanifest["start_url"] == "/"
    assert webmanifest["theme_color"] == "#000000"
    assert webmanifest["background_color"] == "#000000"
    assert webmanifest["icons"][0]["src"] == "/favicon-16x16.png"
    assert webmanifest["icons"][1]["src"] == "/favicon-32x32.png"
    assert webmanifest["icons"][2]["src"] == "/apple-touch-icon.png"
    assert "/api/event" not in json.dumps(webmanifest)
    search_index = json.loads(search_json)
    assert any(entry["title"] == "About" for entry in search_index)
    assert any(entry["title"] == "HireFlow" and entry["type"] == "saga" for entry in search_index)
    assert any(
        entry["title"] == "Architecture Diagram & Narrative"
        and entry["url"] == "/sagas/hireflow/the-origin-blueprint/architecture-diagram-and-narrative/"
        for entry in search_index
    )
    assert "/api/event" not in search_json
    assert "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" in sitemap_xml
    assert "<loc>https://blog.wastingnotime.org/</loc>" in sitemap_xml
    assert "<loc>https://blog.wastingnotime.org/archives/</loc>" in sitemap_xml
    assert "<loc>https://blog.wastingnotime.org/library/architecture/</loc>" in sitemap_xml
    assert "<lastmod>2025-11-14</lastmod>" in sitemap_xml
    assert "https://blog.wastingnotime.org/search/" not in sitemap_xml
    assert "library — an index of ideas and implementation notes" in library_html
    assert "A living index. Pick a topic and you’ll see every post, every saga episode, and every note I’ve published that touches that idea." in library_html
    assert '<a class="active" href="/library/">LIBRARY</a>' in library_html
    assert 'href="/archives/"' not in library_html
    assert 'href="/search/"' not in library_html
    assert '<ul class="grid gap-2 sm:grid-cols-2">' in library_html
    assert '<a class="topic-link block border border-zinc-800 rounded px-3 py-2 text-zinc-100 transition-colors" href="/library/architecture/">' in library_html
    assert "#architecture" in library_html
    assert _json_ld_payloads(library_html) == []
    assert '<title>architecture — library — wasting no time</title>' in topic_html
    assert '<h1 class="mt-3 text-xl tracking-tight text-zinc-300">#architecture</h1>' in topic_html
    assert '<section class="space-y-4">' in topic_html
    assert '<ul class="space-y-4">' in topic_html
    assert '<li class="border border-zinc-800 rounded p-3 hover:border-white/30 transition-colors">' in topic_html
    assert '<div class="flex flex-col gap-1">' in topic_html
    assert '<a class="text-white hover:underline" href="/sagas/hireflow/the-origin-blueprint/architecture-diagram-and-narrative/">Architecture Diagram &amp; Narrative</a>' in topic_html
    assert '<div class="text-xs text-zinc-500">2025-12-29</div>' in topic_html
    assert '<div class="text-xs text-zinc-500">HireFlow / The Origin Blueprint —</div>' in topic_html
    assert '<p class="text-sm text-zinc-400">We consolidate the Origin Blueprint into a coherent MVP architecture.' in topic_html
    assert "[page] About" not in topic_html
    assert "Entries tagged with architecture." not in topic_html
    assert "other ways in" not in topic_html
    assert '<main>' not in topic_html
    assert _json_ld_payloads(topic_html) == []
    assert "sagas — work that moves forward in public" in sagas_index_html
    assert '<p><strong>HireFlow</strong> is a hands-on laboratory where we build a hiring platform from scratch using a microservices approach.' in sagas_index_html
    assert '<li>when the database goes down</li>' in sagas_index_html
    assert '<strong>a system reveals its truth only when we build it.</strong>' in sagas_index_html
    assert 'Let’s build HireFlow together—and learn from its evolution.' in sagas_index_html
    assert '<p>This saga explores the creation of a <strong>Game Hub</strong> — a platform designed to host multiple simple games under one structure.</p>' in sagas_index_html
    assert "<h2 class=\"text-sm text-zinc-400 mb-2\">active sagas</h2>" in sagas_index_html
    assert "start reading →" in sagas_index_html
    assert saga_html == render_legacy_saga_page("hireflow")
    assert arc_html == render_legacy_arc_page("hireflow", "the-origin-blueprint")
    assert _json_ld_payloads(arc_html) == []
    assert 'The story behind <span class="text-zinc-100">wasting no time</span>' in about_html
    assert '<a class="active" href="/about/">ABOUT</a>' in about_html
    assert "Parallel sagas evolving at their own pace" in about_html
    assert "<h3 class=\"text-lg text-zinc-100 font-normal mb-1\">what this is</h3>" in about_html
    assert "<h3 class=\"text-lg text-zinc-100 font-normal mb-1\">what you’ll find here</h3>" in about_html
    assert "<h3 class=\"text-lg text-zinc-100 font-normal mb-1\">why “wasting no time”</h3>" in about_html
    assert "<h3 class=\"text-lg text-zinc-100 font-normal mb-1\">connect</h3>" in about_html
    assert 'href="/feed.xml"' in about_html
    assert '<meta property="og:title"' not in about_html
    assert '<meta name="twitter:title"' not in about_html
    assert _json_ld_payloads(about_html) == []
    assert "© 2026 wastingnotime.org — built with custom python static renderer" in about_html
    assert 'href="/favicon-32x32.png"' in about_html
    assert "studio — building systems in public" in studio_html
    assert "Parallel spaces evolving at their own pace." in studio_html
    assert "wasting no time studio" in studio_html
    assert "codingzen labs" in studio_html
    assert "experiments" in studio_html
    assert episode_html == render_legacy_episode_page(
        "sagas/hireflow/the-origin-blueprint/the-first-brick"
    )
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

    assert 'action="/blog/search/"' in search_html
    assert 'action="/search/"' not in search_html
    assert '<link rel="canonical" href="https://example.com/blog/search/" />' in search_html
    assert "/blog/search.json" in search_html


def _json_ld_payloads(html: str) -> list[dict[str, object]]:
    matches = re.findall(
        r'<script type="application/ld\+json">(.+?)</script>',
        html,
        flags=re.DOTALL,
    )
    return [json.loads(match) for match in matches]
