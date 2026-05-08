from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from email.utils import format_datetime
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from src.app.domain.models.content import (
    ArchiveEntry,
    ArchiveIndex,
    ArcView,
    ContentCatalog,
    EntryMetadata,
    Episode,
    FeedEntry,
    FooterAttribution,
    HomepageSagaSummary,
    HomepageSurface,
    LibraryCatalog,
    Page,
    PublicationMetadata,
    RecentContent,
    SagasIndex,
    SagaView,
    SearchEntry,
    SearchIndex,
    SectionPage,
    SitemapEntry,
    TopicEntry,
    TopicPage,
)
from src.app.domain.models.site_config import AnalyticsConfig, SiteConfig
from src.app.application.use_cases.project_narrative_navigation import (
    project_arc_views,
    project_saga_views,
)
from src.app.application.use_cases.project_navigation_state import (
    NavigationLink,
    project_navigation_state,
)
from src.app.application.use_cases.project_homepage_surface import (
    project_homepage_surface,
)
from src.app.application.use_cases.project_entry_metadata import (
    project_episode_metadata,
    project_page_metadata,
)
from src.app.application.use_cases.project_footer_attribution import (
    project_footer_attribution,
)
from src.app.application.use_cases.project_publication_metadata import (
    project_publication_metadata,
)
from src.app.application.use_cases.project_archive_index import project_archive_index
from src.app.application.use_cases.project_search_index import project_search_index
from src.app.application.use_cases.project_topic_catalog import project_topic_catalog
from src.app.application.use_cases.project_route_robots_policy import (
    project_route_robots_policy,
)
from src.app.application.use_cases.project_section_hubs import project_sagas_index
from src.app.application.use_cases.legacy_episode_pages import render_legacy_episode_page
from src.app.application.use_cases.legacy_sagas_render import (
    render_legacy_sagas_page as render_legacy_sagas_page_snapshot,
)

IDENTITY_ASSET_LINKS: tuple[tuple[str, str, str | None], ...] = (
    ("icon", "/favicon.ico", None),
    ("icon", "/favicon-16x16.png", "16x16"),
    ("icon", "/favicon-32x32.png", "32x32"),
    ("apple-touch-icon", "/apple-touch-icon.png", None),
)
THEME_COLOR = "#000000"
BACKGROUND_COLOR = "#000000"


def build_static_site(config: SiteConfig, catalog: ContentCatalog) -> dict[str, str]:
    arc_views = project_arc_views(catalog)
    footer_attribution = project_footer_attribution(config, catalog)
    saga_views = project_saga_views(catalog, arc_views)
    homepage_surface = project_homepage_surface(catalog, saga_views, arc_views)
    topic_catalog = project_topic_catalog(catalog)
    publication_metadata = project_publication_metadata(
        catalog,
        saga_views,
        arc_views,
        topic_catalog.pages,
    )
    archive_index = project_archive_index(catalog)
    search_index = project_search_index(config, catalog)
    sagas_index = project_sagas_index(saga_views, arc_views)
    section_pages = {page.slug: page for page in catalog.section_pages}
    pages = {
        ".nojekyll": build_nojekyll(),
        "CNAME": build_cname(config),
        "404.html": build_not_found_page(config, footer_attribution),
        "browserconfig.xml": build_browserconfig(config),
        "index.html": build_homepage(
            config,
            catalog,
            homepage_surface,
            footer_attribution,
        ),
        "opensearch.xml": build_opensearch_description(config),
        "archives/index.html": build_archive_page(
            config,
            archive_index,
            footer_attribution,
        ),
        "search/index.html": build_search_page(config, footer_attribution),
        "library/index.html": build_library_page(
            config,
            topic_catalog,
            section_pages["library"],
            footer_attribution,
        ),
        "sagas/index.html": build_sagas_index_page(config, sagas_index, footer_attribution),
        "studio/index.html": build_studio_page(config, section_pages["studio"], footer_attribution),
        "feed.xml": build_feed(config, publication_metadata),
        "robots.txt": build_robots_txt(config),
        "search.json": build_search_index(search_index),
        "site.webmanifest": build_site_webmanifest(config),
        "sitemap.xml": build_sitemap(config, publication_metadata),
    }

    for page in catalog.pages:
        pages[f"{page.slug}/index.html"] = build_content_page(
            config,
            page,
            footer_attribution,
        )

    for saga in catalog.sagas:
        pages[f"sagas/{saga.slug}/index.html"] = build_saga_page(
            config,
            saga_views[saga.slug],
            footer_attribution,
        )

    for arc in catalog.arcs:
        pages[f"sagas/{arc.saga_slug}/{arc.slug}/index.html"] = build_arc_page(
            config,
            arc_views[(arc.saga_slug, arc.slug)],
            footer_attribution,
        )

    for episode in catalog.episodes:
        pages[episode.permalink.strip("/") + "/index.html"] = build_episode_page(
            config,
            episode,
            arc_views[(episode.saga_slug, episode.arc_slug)],
            footer_attribution,
        )

    for topic_page in topic_catalog.pages:
        pages[f"library/{topic_page.tag}/index.html"] = build_topic_page(
            config,
            topic_page,
            footer_attribution,
        )

    return pages


def build_feed(config: SiteConfig, publication_metadata: PublicationMetadata) -> str:
    feed_title = config.title
    feed_description = config.description
    if config.title == "Wasting No Time":
        feed_title = "wasting no time"
        feed_description = "Latest posts and episodes from wasting no time"
    items_markup = "\n".join(
        _render_feed_item(entry, base_url=config.base_url)
        for entry in publication_metadata.feed_entries
    )
    last_build_date = _format_rfc2822(
        publication_metadata.feed_entries[0].date
        if publication_metadata.feed_entries
        else None
    )
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<rss version=\"2.0\">\n"
        "  <channel>\n"
        f"    <title>{html.escape(feed_title)}</title>\n"
        f"    <link>{html.escape(_absolute_url(config.base_url, '/'))}</link>\n"
        f"    <description>{html.escape(feed_description)}</description>\n"
        f"    <lastBuildDate>{html.escape(last_build_date)}</lastBuildDate>\n"
        f"{items_markup}\n"
        "  </channel>\n"
        "</rss>\n"
    )


def build_sitemap(config: SiteConfig, publication_metadata: PublicationMetadata) -> str:
    entries_markup = "\n".join(
        _render_sitemap_entry(entry, base_url=config.base_url)
        for entry in publication_metadata.sitemap_entries
    )
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
        f"{entries_markup}\n"
        "</urlset>\n"
    )


def build_search_index(search_index: SearchIndex) -> str:
    records = [_serialize_search_entry(entry) for entry in search_index.entries]
    return json.dumps(records, ensure_ascii=True) + "\n"


def build_robots_txt(config: SiteConfig) -> str:
    sitemap_url = _absolute_url(config.base_url, "/sitemap.xml")
    return (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {sitemap_url}\n"
    )


def build_cname(config: SiteConfig) -> str:
    return f"{_site_host(config.base_url)}\n"


def build_nojekyll() -> str:
    return "\n"


def build_opensearch_description(config: SiteConfig) -> str:
    search_template = _absolute_url(config.base_url, "/search/?q={searchTerms}")
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<OpenSearchDescription xmlns=\"http://a9.com/-/spec/opensearch/1.1/\">\n"
        f"  <ShortName>{html.escape(config.title)}</ShortName>\n"
        f"  <Description>{html.escape(config.description)}</Description>\n"
        "  <InputEncoding>UTF-8</InputEncoding>\n"
        f"  <Url type=\"text/html\" template=\"{html.escape(search_template)}\"/>\n"
        "</OpenSearchDescription>\n"
    )


def build_site_webmanifest(config: SiteConfig) -> str:
    manifest = {
        "name": config.title,
        "short_name": config.title,
        "start_url": _site_path(config.base_url, "/"),
        "display": "standalone",
        "theme_color": THEME_COLOR,
        "background_color": BACKGROUND_COLOR,
        "icons": [
            {
                "src": _site_path(config.base_url, "/favicon-16x16.png"),
                "sizes": "16x16",
                "type": "image/png",
            },
            {
                "src": _site_path(config.base_url, "/favicon-32x32.png"),
                "sizes": "32x32",
                "type": "image/png",
            },
            {
                "src": _site_path(config.base_url, "/apple-touch-icon.png"),
                "sizes": "180x180",
                "type": "image/png",
            },
        ],
    }
    return json.dumps(manifest, ensure_ascii=True, indent=2) + "\n"


def build_browserconfig(config: SiteConfig) -> str:
    square_logo_url = _site_path(config.base_url, "/apple-touch-icon.png")
    return (
        "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
        "<browserconfig>\n"
        "  <msapplication>\n"
        "    <tile>\n"
        f"      <square150x150logo src=\"{html.escape(square_logo_url)}\"/>\n"
        f"      <TileColor>{html.escape(THEME_COLOR)}</TileColor>\n"
        "    </tile>\n"
        "  </msapplication>\n"
        "</browserconfig>\n"
    )


def build_homepage(
    config: SiteConfig,
    catalog: ContentCatalog,
    homepage_surface: HomepageSurface,
    footer_attribution: FooterAttribution,
) -> str:
    if config.title == "Wasting No Time":
        return _render_legacy_homepage(
            config=config,
            homepage_surface=homepage_surface,
            footer_attribution=footer_attribution,
        )

    recent_items = homepage_surface.recent_entries
    recent_markup = "\n".join(
        _render_recent_item(item, base_url=config.base_url) for item in recent_items
    )
    saga_markup = "\n".join(
        _render_homepage_saga_summary(summary, base_url=config.base_url)
        for summary in homepage_surface.saga_summaries
    )
    return _render_document(
        config=config,
        title=config.title,
        description=config.description,
        canonical_path="/",
        eyebrow="Home",
        heading=config.title,
        summary="Experiments in architecture, focus, and growth — built in public, one saga at a time.",
        metadata="",
        footer_attribution=footer_attribution,
        structured_data_payload=_project_website_structured_data(
            site_title=config.title,
            site_description=config.description,
            base_url=config.base_url,
        ),
        body_html=(
            "        <section>\n"
            "          <h2 class=\"section-label\">RECENT</h2>\n"
            "          <ul class=\"homepage-list\">\n"
            f"{recent_markup}\n"
            "          </ul>\n"
            "        </section>\n"
            "        <section>\n"
            "          <h2 class=\"section-label\">SAGAS</h2>\n"
            "          <ul class=\"homepage-list\">\n"
            f"{saga_markup}\n"
            "          </ul>\n"
            "        </section>\n"
        ),
    )


def _render_legacy_homepage(
    *,
    config: SiteConfig,
    homepage_surface: HomepageSurface,
    footer_attribution: FooterAttribution,
) -> str:
    recent_markup = "\n".join(
        _render_legacy_homepage_recent_item(item, base_url=config.base_url)
        for item in homepage_surface.recent_entries
    )
    saga_markup = "\n".join(
        _render_legacy_homepage_saga_summary(summary, base_url=config.base_url)
        for summary in homepage_surface.saga_summaries
    )
    title = "wasting no time — architecture, focus, and growth in public"
    summary = (
        "Experiments in architecture, focus, and growth — built in public, "
        "one saga at a time."
    )
    section_html = (
        "    <main>\n"
        "        <section>\n"
        "            <h2 class=\"text-sm text-zinc-400 mb-2\">RECENT</h2>\n"
        "            <ul class=\"space-y-3\">\n"
        f"{recent_markup}\n"
        "            </ul>\n"
        "        </section>\n"
        "\n"
        "        <section class=\"mt-6\">\n"
        "            <h2 class=\"text-sm text-zinc-400 mb-2\">SAGAS</h2>\n"
        "            <ul class=\"space-y-1\">\n"
        f"{saga_markup}\n"
        "            </ul>\n"
        "        </section>\n"
        "    </main>\n"
    )
    rendered = _render_legacy_blog_page(
        title=title,
        h1_html=html.escape(title),
        intro_html=html.escape(summary),
        section_html=section_html,
        active_section="home",
        footer_attribution=footer_attribution,
    )
    return _inject_legacy_homepage_metadata(
        rendered,
        config=config,
        title=title,
        description=summary,
    )


def _inject_legacy_homepage_metadata(
    rendered: str,
    *,
    config: SiteConfig,
    title: str,
    description: str,
) -> str:
    canonical_path = "/"
    canonical_url = _absolute_url(config.base_url, canonical_path)
    feed_url = _site_path(config.base_url, "/feed.xml")
    manifest_url = _site_path(config.base_url, "/site.webmanifest")
    browserconfig_url = _site_path(config.base_url, "/browserconfig.xml")
    opensearch_url = _site_path(config.base_url, "/opensearch.xml")
    social_preview_url = _site_path(config.base_url, "/social-preview.png")
    metadata = "\n".join(
        (
            f'    <meta name="robots" content="{html.escape(project_route_robots_policy(canonical_path))}" />',
            f'    <meta name="description" content="{html.escape(description)}" />',
            f'    <meta name="generator" content="blog-v2 static builder" />',
            f'    <meta name="author" content="{html.escape(_site_host(config.base_url))}" />',
            f'    <meta name="application-name" content="{html.escape(config.title)}" />',
            '    <meta name="color-scheme" content="dark" />',
            '    <meta name="referrer" content="strict-origin-when-cross-origin" />',
            '    <meta name="format-detection" content="telephone=no" />',
            f'    <meta name="theme-color" content="{THEME_COLOR}" />',
            f'    <meta name="msapplication-TileColor" content="{THEME_COLOR}" />',
            f'    <meta name="msapplication-config" content="{html.escape(browserconfig_url)}" />',
            '    <meta name="apple-mobile-web-app-capable" content="yes" />',
            f'    <meta name="apple-mobile-web-app-title" content="{html.escape(config.title)}" />',
            '    <meta name="apple-mobile-web-app-status-bar-style" content="black" />',
            f'    <link rel="canonical" href="{html.escape(canonical_url)}" />',
            _render_open_graph_metadata(
                site_title=config.title,
                title=title,
                description=description,
                canonical_url=canonical_url,
                social_preview_url=social_preview_url,
            ),
            _render_twitter_card_metadata(
                title=title,
                description=description,
                canonical_url=canonical_url,
                social_preview_url=social_preview_url,
            ),
            _render_structured_data_script(
                _project_website_structured_data(
                    site_title=config.title,
                    site_description=config.description,
                    base_url=config.base_url,
                )
            ),
            f'    <link rel="alternate" type="application/rss+xml" title="{html.escape(config.title)} RSS" href="{html.escape(feed_url)}" />',
            f'    <link rel="search" type="application/opensearchdescription+xml" title="{html.escape(config.title)} Search" href="{html.escape(opensearch_url)}" />',
            f'    <link rel="manifest" href="{html.escape(manifest_url)}" />',
        )
    )
    title_markup = f"    <title>{html.escape(title)}</title>\n"
    return rendered.replace(title_markup, f"{title_markup}{metadata}\n", 1)


def _render_legacy_homepage_recent_item(
    item: RecentContent,
    *,
    base_url: str,
) -> str:
    context = ""
    if item.saga_title:
        context = f" · {item.saga_title}"
        if item.arc_title:
            context += f" / {item.arc_title}"

    return (
        "                <li>\n"
        f'                    <a href="{_site_path(base_url, item.permalink)}">\n'
        f"                        [{html.escape(item.kind.capitalize())}] {html.escape(item.title)}\n"
        "                    </a>\n"
        "                    <span class=\"block text-zinc-500 text-xs mt-0.5\">\n"
        f"                        {html.escape(item.date)}{html.escape(context)}\n"
        "                    </span>\n"
        "                    <p class=\"text-sm text-zinc-400 leading-relaxed mt-1\">\n"
        f"                        {html.escape(item.summary)}\n"
        "                    </p>\n"
        "                </li>"
    )


def _render_legacy_homepage_saga_summary(
    summary: HomepageSagaSummary,
    *,
    base_url: str,
) -> str:
    episode_label = "episode" if summary.episode_count == 1 else "episodes"
    status_parts = [f"{summary.episode_count} {episode_label}"]
    if summary.last_release_date:
        status_parts.append(f"last release {summary.last_release_date}")
    status_parts.append(summary.status)
    return (
        "                <li>\n"
        f'                    <a href="{_site_path(base_url, summary.permalink)}">{html.escape(summary.title)}</a>\n'
        "                    <span class=\"homepage-saga-status text-zinc-500 text-xs\">\n"
        f"                        — {html.escape('; '.join(status_parts))}\n"
        "                    </span>\n"
        "                </li>"
    )




def build_not_found_page(
    config: SiteConfig,
    footer_attribution: FooterAttribution,
) -> str:
    recovery_rows = "\n".join(
        (
            "            <li>\n"
            '              <div class="not-found-row">\n'
                f'                <a class="not-found-link" href="{_site_path(config.base_url, path)}">{html.escape(label)}</a>\n'
            f'                <small class="not-found-path">{html.escape(path)}</small>\n'
            "              </div>\n"
            "            </li>"
        )
        for label, path in (
            ("Return home", "/"),
            ("Search the publication", "/search/"),
            ("Browse the archives", "/archives/"),
            ("Browse sagas", "/sagas/"),
            ("Browse the library", "/library/"),
        )
    )
    return _render_document(
        config=config,
        title="Not Found",
        description="The requested page could not be found on this static site.",
        canonical_path="/404.html",
        eyebrow="404",
        heading="Page Not Found",
        summary="The route you asked for is not part of the current publication.",
        metadata="Static recovery page",
        robots_content="noindex,follow",
        footer_attribution=footer_attribution,
        body_html=(
            "        <section>\n"
            "          <h2>Try one of these instead</h2>\n"
            "          <p>The page you requested does not exist here, or it may have moved during the rebuild.</p>\n"
            "          <ul class=\"not-found-list\">\n"
            f"{recovery_rows}\n"
            "          </ul>\n"
            "        </section>"
        ),
    )


def build_archive_page(
    config: SiteConfig,
    archive_index: ArchiveIndex,
    footer_attribution: FooterAttribution,
) -> str:
    archive_markup = "\n".join(
        _render_archive_entry(entry, base_url=config.base_url)
        for entry in archive_index.entries
    )
    return _render_document(
        config=config,
        title="Archives",
        description="Chronological archive of published writing and saga episodes.",
        canonical_path="/archives/",
        eyebrow="Archives",
        heading="Archives",
        summary="Browse the publication chronologically from newest to oldest.",
        metadata=f"{len(archive_index.entries)} published entries",
        footer_attribution=footer_attribution,
        structured_data_payload=_project_webpage_structured_data(
            title="Archives",
            description="Chronological archive of published writing and saga episodes.",
            canonical_url=_absolute_url(config.base_url, "/archives/"),
        ),
        body_html="\n".join(
            [
                (
                    "        <section>\n"
                    "          <h2>Chronological Archive</h2>\n"
                    "          <ul class=\"archive-entry-list\">\n"
                    f"{archive_markup}\n"
                    "          </ul>\n"
                    "        </section>"
                ),
                _render_discovery_surface(
                    config.base_url,
                    (
                        ("Search across the publication", "/search/"),
                        ("Move by topic instead", "/library/"),
                    ),
                ),
            ]
        ),
    )


def build_search_page(
    config: SiteConfig,
    footer_attribution: FooterAttribution,
) -> str:
    search_index_url = _site_path(config.base_url, "/search.json")
    search_action_url = _site_path(config.base_url, "/search/")
    return _render_document(
        config=config,
        title="Search",
        description="Search the publication using the static search index.",
        canonical_path="/search/",
        eyebrow="Search",
        heading="Search",
        summary="Use the static index to find pages, sagas, arcs, and episodes.",
        metadata="client-side search",
        footer_attribution=footer_attribution,
        structured_data_payload=_project_webpage_structured_data(
            title="Search",
            description="Search the publication using the static search index.",
            canonical_url=_absolute_url(config.base_url, "/search/"),
        ),
        body_html=(
            "        <section>\n"
            "          <h2>Search the publication</h2>\n"
            '          <p id="search-helper">Type to filter the static index published with the site.</p>\n'
            f'          <form id="search-form" method="get" action="{search_action_url}">\n'
            '            <label class="search-query-label" for="search-query">Search query</label>\n'
            '            <input class="search-query-input" id="search-query" name="q" type="search" placeholder="Search titles, summaries, and topics" autocomplete="off" aria-describedby="search-helper search-status" aria-description="Search titles, summaries, and topics." />\n'
            '            <button class="search-submit-button" type="submit">Search</button>\n'
            "          </form>\n"
            "          <noscript>\n"
            "            <div class=\"search-noscript-recovery\">\n"
            "              <p class=\"search-noscript-recovery-message\">Live search on this page requires JavaScript. If it is unavailable, browse the chronology or move by topic instead.</p>\n"
            "              <div class=\"search-noscript-recovery-row\">\n"
            f'                <a class="search-noscript-recovery-link" href="{_site_path(config.base_url, "/archives/")}">Browse the archives</a>\n'
            f'                <small class="search-noscript-recovery-path">/archives/</small>\n'
            "              </div>\n"
            "              <div class=\"search-noscript-recovery-row\">\n"
            f'                <a class="search-noscript-recovery-link" href="{_site_path(config.base_url, "/library/")}">Explore the library</a>\n'
            f'                <small class="search-noscript-recovery-path">/library/</small>\n'
            "              </div>\n"
            "            </div>\n"
            "          </noscript>\n"
            '          <p id="search-status" role="status" aria-live="polite" aria-atomic="true">Enter a query to search the publication.</p>\n'
            '          <h3 id="search-results-heading" class="visually-hidden">Search results</h3>\n'
            '          <ul id="search-results" class="search-result-list" aria-labelledby="search-results-heading"></ul>\n'
            "        </section>\n"
        f"{_render_discovery_surface(config.base_url, (('Browse the chronology', '/archives/'), ('Move by topic instead', '/library/')))}\n"
            "        <script>\n"
            f"          const searchIndexUrl = {json.dumps(search_index_url)};\n"
            "          const searchForm = document.getElementById('search-form');\n"
            "          const searchInput = document.getElementById('search-query');\n"
            "          const searchStatus = document.getElementById('search-status');\n"
            "          const searchResults = document.getElementById('search-results');\n"
            "          const searchRecovery = document.createElement('div');\n"
            "          searchRecovery.className = 'search-empty-recovery';\n"
            "          const initialQuery = new URLSearchParams(window.location.search).get('q') ?? '';\n"
            "          let searchRecords = [];\n"
            "          const normalizeSearchText = (value) => (value || '').trim().toLowerCase();\n"
            "          const createSearchRecoveryRow = (label, path) => {\n"
            "            const row = document.createElement('div');\n"
            "            row.className = 'search-empty-recovery-row';\n"
            "            const link = document.createElement('a');\n"
            "            link.className = 'search-empty-recovery-link';\n"
            "            link.href = path;\n"
            "            link.textContent = label;\n"
            "            const meta = document.createElement('small');\n"
            "            meta.className = 'search-empty-recovery-path';\n"
            "            meta.textContent = new URL(path).pathname;\n"
            "            row.appendChild(link);\n"
            "            row.appendChild(meta);\n"
            "            return row;\n"
            "          };\n"
            "          const projectSearchUrlState = (query) => {\n"
            "            const nextUrl = new URL(window.location.href);\n"
            "            const normalizedQuery = query.trim();\n"
            "            if (normalizedQuery) {\n"
            "              nextUrl.searchParams.set('q', normalizedQuery);\n"
            "            } else {\n"
            "              nextUrl.searchParams.delete('q');\n"
            "            }\n"
            "            const nextPath = nextUrl.search ? `${nextUrl.pathname}${nextUrl.search}` : nextUrl.pathname;\n"
            "            window.history.replaceState(null, '', nextPath);\n"
            "          };\n"
            "          const scoreSearchRecord = (record, normalizedQuery) => {\n"
            "            const normalizedTitle = normalizeSearchText(record.title);\n"
            "            if (normalizedTitle === normalizedQuery) {\n"
            "              return 0;\n"
            "            }\n"
            "            if (normalizedTitle.startsWith(normalizedQuery)) {\n"
            "              return 1;\n"
            "            }\n"
            "            if (normalizedTitle.includes(normalizedQuery)) {\n"
            "              return 2;\n"
            "            }\n"
            "            const normalizedContext = normalizeSearchText(record.context);\n"
            "            if (normalizedContext === normalizedQuery) {\n"
            "              return 3;\n"
            "            }\n"
            "            if (normalizedContext.includes(normalizedQuery)) {\n"
            "              return 4;\n"
            "            }\n"
            "            const normalizedSummary = normalizeSearchText(record.summary);\n"
            "            if (normalizedSummary.includes(normalizedQuery)) {\n"
            "              return 5;\n"
            "            }\n"
            "            const normalizedTags = (record.tags || []).map((tag) => normalizeSearchText(tag));\n"
            "            if (normalizedTags.some((tag) => tag === normalizedQuery)) {\n"
            "              return 6;\n"
            "            }\n"
            "            if (normalizedTags.some((tag) => tag.includes(normalizedQuery))) {\n"
            "              return 7;\n"
            "            }\n"
            "            return Number.POSITIVE_INFINITY;\n"
            "          };\n"
            "          const createHighlightedFragment = (value, normalizedQuery) => {\n"
            "            const fragment = document.createDocumentFragment();\n"
            "            const sourceText = value || '';\n"
            "            if (!normalizedQuery) {\n"
            "              fragment.appendChild(document.createTextNode(sourceText));\n"
            "              return fragment;\n"
            "            }\n"
            "            const normalizedSource = normalizeSearchText(sourceText);\n"
            "            if (!normalizedSource.includes(normalizedQuery)) {\n"
            "              fragment.appendChild(document.createTextNode(sourceText));\n"
            "              return fragment;\n"
            "            }\n"
            "            let startIndex = 0;\n"
            "            let matchIndex = normalizedSource.indexOf(normalizedQuery, startIndex);\n"
            "            while (matchIndex !== -1) {\n"
            "              if (matchIndex > startIndex) {\n"
            "                fragment.appendChild(document.createTextNode(sourceText.slice(startIndex, matchIndex)));\n"
            "              }\n"
            "              const mark = document.createElement('mark');\n"
            "              mark.textContent = sourceText.slice(matchIndex, matchIndex + normalizedQuery.length);\n"
            "              fragment.appendChild(mark);\n"
            "              startIndex = matchIndex + normalizedQuery.length;\n"
            "              matchIndex = normalizedSource.indexOf(normalizedQuery, startIndex);\n"
            "            }\n"
            "            if (startIndex < sourceText.length) {\n"
            "              fragment.appendChild(document.createTextNode(sourceText.slice(startIndex)));\n"
            "            }\n"
            "            return fragment;\n"
            "          };\n"
            "          const renderResults = (query) => {\n"
            "            const normalizedQuery = normalizeSearchText(query);\n"
            "            searchResults.innerHTML = '';\n"
            "            searchRecovery.replaceChildren();\n"
            "            if (!normalizedQuery) {\n"
            "              searchStatus.textContent = 'Enter a query to search the publication.';\n"
            "              return;\n"
            "            }\n"
            "            const matches = searchRecords\n"
            "              .map((record) => ({\n"
            "                record,\n"
            "                score: scoreSearchRecord(record, normalizedQuery),\n"
            "              }))\n"
            "              .filter(({ score }) => Number.isFinite(score))\n"
            "              .sort((left, right) => {\n"
            "                if (left.score !== right.score) {\n"
            "                  return left.score - right.score;\n"
            "                }\n"
            "                const titleComparison = normalizeSearchText(left.record.title)\n"
            "                  .localeCompare(normalizeSearchText(right.record.title));\n"
            "                if (titleComparison !== 0) {\n"
            "                  return titleComparison;\n"
            "                }\n"
            "                return (left.record.url || '').localeCompare(right.record.url || '');\n"
            "              })\n"
            "              .map(({ record }) => record);\n"
            "            searchStatus.textContent = matches.length\n"
            "              ? `${matches.length} result${matches.length === 1 ? '' : 's'} for \"${query}\"`\n"
            "              : `No results for \"${query}\"`;\n"
            "            if (!matches.length) {\n"
            "              const message = document.createElement('p');\n"
            "              message.className = 'search-empty-recovery-message';\n"
            "              message.textContent = `No results for \"${query}\". Try these routes instead.`;\n"
            "              searchRecovery.appendChild(message);\n"
            f"              searchRecovery.appendChild(createSearchRecoveryRow('the archives', {json.dumps(_site_path(config.base_url, '/archives/'))}));\n"
            f"              searchRecovery.appendChild(createSearchRecoveryRow('the library', {json.dumps(_site_path(config.base_url, '/library/'))}));\n"
            "              searchResults.appendChild(searchRecovery);\n"
            "              return;\n"
            "            }\n"
            "            matches.forEach((record) => {\n"
            "              const item = document.createElement('li');\n"
            "              item.className = 'search-result-item';\n"
            "              const header = document.createElement('div');\n"
            "              header.className = 'search-result-header';\n"
            "              const link = document.createElement('a');\n"
            "              link.className = 'search-result-link';\n"
            "              link.href = new URL(record.url).pathname;\n"
            "              link.appendChild(document.createTextNode(`[${record.type}] `));\n"
            "              link.appendChild(createHighlightedFragment(record.title, normalizedQuery));\n"
            "              header.appendChild(link);\n"
            "              const meta = document.createElement('small');\n"
            "              meta.className = 'search-result-meta';\n"
            "              if (record.date) {\n"
            "                meta.appendChild(document.createTextNode(record.date));\n"
            "              }\n"
            "              if (record.context) {\n"
            "                if (meta.childNodes.length) {\n"
            "                  meta.appendChild(document.createTextNode(' · '));\n"
            "                }\n"
            "                meta.appendChild(createHighlightedFragment(record.context, normalizedQuery));\n"
            "              }\n"
            "              if (meta.childNodes.length) {\n"
            "                header.appendChild(meta);\n"
            "              }\n"
            "              item.appendChild(header);\n"
            "              if (record.summary) {\n"
            "                const summary = document.createElement('p');\n"
            "                summary.className = 'search-result-summary';\n"
            "                summary.appendChild(createHighlightedFragment(record.summary, normalizedQuery));\n"
            "                item.appendChild(summary);\n"
            "              }\n"
            "              if ((record.tags || []).length) {\n"
            "                const tags = document.createElement('div');\n"
            "                tags.className = 'search-result-tags';\n"
            "                record.tags.forEach((tag) => {\n"
            "                  const chip = document.createElement('span');\n"
            "                  chip.className = 'search-result-tag-chip';\n"
            "                  chip.appendChild(document.createTextNode('#'));\n"
            "                  chip.appendChild(createHighlightedFragment(tag, normalizedQuery));\n"
            "                  tags.appendChild(chip);\n"
            "                });\n"
            "                item.appendChild(tags);\n"
            "              }\n"
            "              searchResults.appendChild(item);\n"
            "            });\n"
            "          };\n"
            "          fetch(searchIndexUrl)\n"
            "            .then((response) => response.json())\n"
            "            .then((records) => {\n"
            "              searchRecords = records;\n"
            "              renderResults(searchInput.value);\n"
            "            })\n"
            "            .catch(() => {\n"
            "              searchStatus.textContent = 'Search index could not be loaded.';\n"
            "              searchRecovery.className = 'search-load-recovery';\n"
            "              searchRecovery.replaceChildren();\n"
            "              const message = document.createElement('p');\n"
            "              message.className = 'search-load-recovery-message';\n"
            "              message.textContent = 'Search index is unavailable right now. Try these routes instead.';\n"
            "              searchRecovery.appendChild(message);\n"
            f"              searchRecovery.appendChild(createSearchRecoveryRow('the archives', {json.dumps(_site_path(config.base_url, '/archives/'))}));\n"
            f"              searchRecovery.appendChild(createSearchRecoveryRow('the library', {json.dumps(_site_path(config.base_url, '/library/'))}));\n"
            "              searchResults.appendChild(searchRecovery);\n"
            "            });\n"
            "          searchInput.value = initialQuery;\n"
            "          projectSearchUrlState(searchInput.value);\n"
            "          searchForm.addEventListener('submit', (event) => {\n"
            "            event.preventDefault();\n"
            "            projectSearchUrlState(searchInput.value);\n"
            "            renderResults(searchInput.value);\n"
            "          });\n"
            "          searchInput.addEventListener('input', (event) => {\n"
            "            projectSearchUrlState(event.target.value);\n"
            "            renderResults(event.target.value);\n"
            "          });\n"
            "        </script>"
        ),
    )


def build_content_page(
    config: SiteConfig,
    page: Page,
    footer_attribution: FooterAttribution,
) -> str:
    if config.title == "Wasting No Time" and page.slug == "about":
        return _render_legacy_about_page(footer_attribution)

    entry_metadata = project_page_metadata(page)
    return _render_document(
        config=config,
        title=page.title,
        description=page.summary,
        canonical_path=page.permalink,
        eyebrow="Page",
        heading=page.title,
        summary=page.summary,
        metadata=page.date,
        footer_attribution=footer_attribution,
        structured_data_payload=_project_article_structured_data(
            title=page.title,
            description=page.summary,
            canonical_url=_absolute_url(config.base_url, page.permalink),
            publication_date=page.date,
            author_name=_site_host(config.base_url),
            publisher_name=config.title,
            publisher_url=_absolute_url(config.base_url, "/"),
        ),
        body_html="\n".join(
            [
                _render_entry_metadata(entry_metadata, base_url=config.base_url),
                _render_markdown(page.body_markdown),
                _render_discovery_surface(
                    config.base_url,
                    (
                        ("Browse the chronology", "/archives/"),
                        ("Search across the publication", "/search/"),
                    ),
                ),
            ]
        ),
    )


def build_episode_page(
    config: SiteConfig,
    episode: Episode,
    arc_view: ArcView,
    footer_attribution: FooterAttribution,
) -> str:
    if config.title == "Wasting No Time":
        try:
            return render_legacy_episode_page(episode.permalink)
        except KeyError:
            return _render_legacy_episode_fallback(
                config=config,
                episode=episode,
                arc_view=arc_view,
                footer_attribution=footer_attribution,
            )
    entry_metadata = project_episode_metadata(episode)
    metadata = (
        f"{episode.date} · {episode.saga_title} / {episode.arc_title} · "
        f"Episode {episode.number}"
    )
    parent_navigation = (
        f'        <nav class="breadcrumbs episode-breadcrumbs"><a class="breadcrumb-link" href="{_site_path(config.base_url, "/sagas/" + episode.saga_slug + "/")}">'
        f"{html.escape(episode.saga_title)}</a> <span class=\"breadcrumb-separator\">/</span> "
        f'<a class="breadcrumb-link" href="{_site_path(config.base_url, "/sagas/" + episode.saga_slug + "/" + episode.arc_slug + "/")}">'
        f"{html.escape(episode.arc_title)}</a></nav>"
    )
    previous_episode = arc_view.previous_episode[episode.slug]
    next_episode = arc_view.next_episode[episode.slug]
    adjacent_navigation = _render_adjacent_navigation(
        previous_episode=previous_episode,
        next_episode=next_episode,
        base_url=config.base_url,
    )
    return _render_document(
        config=config,
        title=episode.title,
        description=episode.summary,
        canonical_path=episode.permalink,
        eyebrow="Episode",
        heading=episode.title,
        summary=episode.summary,
        metadata=metadata,
        footer_attribution=footer_attribution,
        structured_data_payload=_project_article_structured_data(
            title=episode.title,
            description=episode.summary,
            canonical_url=_absolute_url(config.base_url, episode.permalink),
            publication_date=episode.date,
            author_name=_site_host(config.base_url),
            publisher_name=config.title,
            publisher_url=_absolute_url(config.base_url, "/"),
        ),
        body_html="\n".join(
            [
                parent_navigation,
                _render_entry_metadata(entry_metadata, base_url=config.base_url),
                _render_markdown(episode.body_markdown),
                _render_discovery_surface(
                    config.base_url,
                    (
                        ("Browse the chronology", "/archives/"),
                        ("Search across the publication", "/search/"),
                    ),
                ),
                adjacent_navigation,
            ]
        ),
    )


def _render_legacy_episode_fallback(
    config: SiteConfig,
    episode: Episode,
    arc_view: ArcView,
    footer_attribution: FooterAttribution,
) -> str:
    previous_episode = arc_view.previous_episode.get(episode.slug)
    next_episode = arc_view.next_episode.get(episode.slug)
    previous_link = ""
    next_link = ""
    if previous_episode is not None:
        previous_link = (
            f'<a class="hover:underline" href="{_site_path(config.base_url, previous_episode.permalink)}">'
            f"← [Ep {previous_episode.number:02d}] {html.escape(previous_episode.title)}</a>"
        )
    if next_episode is not None:
        next_link = (
            f'<a class="hover:underline" href="{_site_path(config.base_url, next_episode.permalink)}">'
            f"[Ep {next_episode.number:02d}] {html.escape(next_episode.title)} →</a>"
        )
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '    <meta charset="utf-8" />\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
        f"    <title>{html.escape(episode.title)} — {html.escape(episode.saga_title)}</title>\n"
        '    <link rel="icon" href="/favicon.ico">\n'
        '    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n'
        '    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n'
        '    <link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        '    <script src="https://cdn.tailwindcss.com"></script>\n'
        '    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>\n'
        '    <style>\n'
        '        html { font-kerning: normal; }\n\n'
        '        .menu a { color:#a1a1aa; text-decoration:none; transition: color .15s ease; }\n'
        '        .menu a:hover { color:#fff; text-decoration:underline; }\n'
        '        .menu a.active { color:#fff; font-weight:500; }\n'
        '        .menu a.active::after { content:"•"; margin-left:0.4em; opacity:0.6; font-weight:400; }\n\n'
        '        a { color:#a1a1aa; text-decoration:none; transition: color .15s ease; }\n'
        '        a:hover { color:#fff; text-decoration:underline; }\n\n'
        '        ul { list-style:none; padding-left:0; margin:0; }\n\n'
        '        .intro:empty { display:none; }\n\n'
        '        .space-y-1 > * + * { margin-top: .25rem; }\n'
        '        .space-y-2 > * + * { margin-top: .5rem; }\n'
        '        .space-y-3 > * + * { margin-top: .75rem; }\n'
        '        .space-y-6 > * + * { margin-top: 1.5rem; }\n\n'
        '        .breadcrumb { font-size:0.9rem; color:#888; margin-bottom:1.5rem; }\n'
        '        .breadcrumb a { color:#aaa; text-decoration:none; }\n'
        '        .breadcrumb a:hover { text-decoration:underline; color:#fff; }\n'
        '        .breadcrumb .sep { margin:0 .4rem; color:#555; }\n\n'
        '        .arc-name,\n'
        '        .episode-title { color:#fff; font-weight:500; margin:0 0 1rem 0; font-size:1.1rem; }\n'
        '        .topic-link { border-width:1px; border-color: rgb(39 39 42); border-style: solid; border-radius:.25rem; padding:.5rem .75rem; color: rgb(244 244 245); }\n'
        '    </style>\n'
        "</head>\n"
        '<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">\n'
        '<div class="max-w-3xl mx-auto px-4 py-6">\n'
        '    <header class="mb-6">\n'
        '        <nav class="menu text-sm text-zinc-400">\n'
        '            <a class="" href="/">HOME</a>\n'
        '            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>\n'
        '            <a class="" href="/studio/">STUDIO</a>\n'
        '            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>\n'
        '            <a class="active" href="/sagas/">SAGAS</a>\n'
        '            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>\n'
        '            <a class="" href="/library/">LIBRARY</a>\n'
        '            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>\n'
        '            <a class="" href="/about/">ABOUT</a>\n'
        '            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>\n'
        '            <a href="/feed.xml">RSS</a>\n'
        "        </nav>\n\n"
        f'        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">[Ep {episode.number:02d}] {html.escape(episode.title)} — {html.escape(episode.arc_title)} / {html.escape(episode.saga_title)}</h1>\n'
        "    </header>\n\n"
        '    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">\n'
        "    </p>\n\n"
        '    <nav class="breadcrumb">\n'
        f'        <a href="{_site_path(config.base_url, "/sagas/" + episode.saga_slug + "/")}">← {html.escape(episode.saga_title)}</a>\n'
        '        <span class="sep">/</span>\n'
        f'        <a href="{_site_path(config.base_url, "/sagas/" + episode.saga_slug + "/" + episode.arc_slug + "/")}">{html.escape(episode.arc_title)}</a>\n'
        "    </nav>\n"
        f'    <h2 class="episode-title">{html.escape(episode.title)}</h2>\n'
        '    <div class="text-xs text-zinc-500 mb-3">\n'
        f'        {html.escape(episode.date)} · <a class="hover:underline" href="{_site_path(config.base_url, "/sagas/" + episode.saga_slug + "/" + episode.arc_slug + "/")}">back to arc</a>\n'
        "    </div>\n"
        f'    <p class="text-sm text-zinc-400 mb-4">{html.escape(episode.summary)}</p>\n\n'
        f'    <article class="prose prose-invert max-w-none">\n{_render_markdown(episode.body_markdown)}\n    </article>\n\n'
        '    <nav class="mt-8 text-xs text-zinc-400 flex justify-between">\n'
        f"        {previous_link or '<span></span>'}\n"
        f"        {next_link or '<span></span>'}\n"
        "    </nav>\n\n"
        f'    <footer class="mt-10 text-xs text-zinc-500">\n        © {footer_attribution.year} {footer_attribution.site_name} — {footer_attribution.tagline}\n    </footer>\n'
        "</div>\n"
        "</body>\n"
        "</html>\n"
    )


def build_saga_page(
    config: SiteConfig,
    saga_view: SagaView,
    footer_attribution: FooterAttribution,
) -> str:
    if config.title == "Wasting No Time":
        return _render_legacy_saga_page(config, saga_view, footer_attribution)

    arc_markup = "\n".join(
        _render_arc_summary(arc, base_url=config.base_url) for arc in saga_view.arcs
    )
    timeline_markup = "\n".join(
        _render_timeline_entry(entry, base_url=config.base_url)
        for entry in saga_view.timeline
    )
    return _render_document(
        config=config,
        title=saga_view.saga.title,
        description=saga_view.saga.summary,
        canonical_path=saga_view.saga.permalink,
        eyebrow="Saga",
        heading=saga_view.saga.title,
        summary=saga_view.saga.summary,
        metadata=f"{saga_view.saga.date} · {saga_view.saga.status}",
        footer_attribution=footer_attribution,
        body_html="\n".join(
            [
                (
                    "        <section>\n"
                    f"{_render_markdown(saga_view.saga.body_markdown)}\n"
                    "        </section>"
                ),
                (
                    "        <section>\n"
                    "          <h2>Arcs</h2>\n"
                    "          <ul class=\"saga-arc-list\">\n"
                    f"{arc_markup}\n"
                    "          </ul>\n"
                    "        </section>"
                ),
                (
                    "        <section>\n"
                    "          <h2>Timeline</h2>\n"
                    "          <ul class=\"saga-timeline-list\">\n"
                    f"{timeline_markup}\n"
                    "          </ul>\n"
                    "        </section>"
                ),
                _render_discovery_surface(
                    config.base_url,
                    (
                        ("Browse the chronology", "/archives/"),
                        ("Search across the publication", "/search/"),
                    ),
                ),
            ]
        ),
    )


def build_arc_page(
    config: SiteConfig,
    arc_view: ArcView,
    footer_attribution: FooterAttribution,
) -> str:
    if config.title == "Wasting No Time":
        return _render_legacy_arc_page_dynamic(config, arc_view, footer_attribution)

    episode_markup = "\n".join(
        _render_arc_episode(episode, base_url=config.base_url)
        for episode in arc_view.episodes
    )
    breadcrumb = (
        f'        <nav class="breadcrumbs"><a class="breadcrumb-link" href="{_site_path(config.base_url, arc_view.arc.permalink[:-len(arc_view.arc.slug)-1])}">'
        f"{html.escape(arc_view.arc.saga_title)}</a></nav>"
    )
    return _render_document(
        config=config,
        title=arc_view.arc.title,
        description=arc_view.arc.summary,
        canonical_path=arc_view.arc.permalink,
        eyebrow="Arc",
        heading=arc_view.arc.title,
        summary=arc_view.arc.summary,
        metadata=f"{arc_view.arc.date} · {arc_view.arc.saga_title}",
        footer_attribution=footer_attribution,
        body_html="\n".join(
            [
                breadcrumb,
                (
                    "        <section>\n"
                    f"{_render_markdown(arc_view.arc.body_markdown)}\n"
                    "        </section>"
                ),
                (
                    "        <section>\n"
                    "          <h2>Episodes</h2>\n"
                    "          <ul class=\"arc-episode-list\">\n"
                    f"{episode_markup}\n"
                    "          </ul>\n"
                    "        </section>"
                ),
                _render_discovery_surface(
                    config.base_url,
                    (
                        ("Browse the chronology", "/archives/"),
                        ("Search across the publication", "/search/"),
                    ),
                ),
            ]
        ),
    )


def _render_legacy_saga_page(
    config: SiteConfig,
    saga_view: SagaView,
    footer_attribution: FooterAttribution,
) -> str:
    intro_html = html.escape(saga_view.saga.summary)
    current_arc = saga_view.arcs[0] if saga_view.arcs else None
    current_arc_markup = ""
    if current_arc is not None:
        current_arc_episodes = [
            entry
            for entry in saga_view.timeline
            if entry.arc_title == current_arc.title
        ]
        latest_episode_links = "\n".join(
            (
                "        <a class=\"hover:underline\" href=\""
                f"{_site_path(config.base_url, entry.permalink)}\">Ep {entry.number:02d}</a>"
            )
            for entry in current_arc_episodes[:3]
        )
        current_arc_markup = (
            "        <section class=\"mb-5\">\n"
            "            <h2 class=\"text-sm text-zinc-400 mb-1\">CURRENT ARC</h2>\n"
            "            <div>\n"
            f"                <a class=\"hover:underline\" href=\"{_site_path(config.base_url, current_arc.permalink)}\">[Arc] {html.escape(current_arc.title)}</a>\n"
        )
        if latest_episode_links:
            current_arc_markup += (
                "\n"
                "                <span class=\"text-zinc-500 text-xs\">— latest:\n"
                f"{latest_episode_links}\n"
                "      </span>\n"
            )
        current_arc_markup += (
            "\n"
            "            </div>\n"
            "        </section>\n"
            "    \n"
        )

    arcs_markup = "\n".join(
        (
            "                <li>\n"
            f'                    <a class="hover:underline" href="{_site_path(config.base_url, arc.permalink)}">[Arc] {html.escape(arc.title)}</a>\n'
            "                    <span class=\"text-zinc-500 text-xs\">"
            f"— {arc.episode_count} eps; last {html.escape(arc.last_release_date or '—')}"
            "</span>\n"
            "                </li>"
        )
        for arc in saga_view.arcs
    )
    timeline_markup = "\n".join(
        (
            "                <li>\n"
            f'                    <a class="hover:underline" href="{_site_path(config.base_url, entry.permalink)}">[Ep {entry.number:02d}] {html.escape(entry.title)}</a>\n'
            "                    <span class=\"text-zinc-500 text-xs\">"
            f"— {html.escape(entry.arc_title)} / {html.escape(entry.date)}"
            "</span>\n"
            "                </li>"
        )
        for entry in saga_view.timeline
    )
    body_sections = (
        f"{_render_markdown(saga_view.saga.body_markdown)}\n"
        f"{current_arc_markup}"
        "    <section>\n"
        "        <h2 class=\"text-sm text-zinc-400 mb-2\">ARCS</h2>\n"
        "        <ul class=\"space-y-1\">\n"
        f"{arcs_markup}\n"
        "        </ul>\n"
        "    </section>\n\n"
        "    \n"
        "    <section class=\"mt-6\">\n"
        "        <h2 class=\"text-sm text-zinc-400 mb-2\">TIMELINE</h2>\n"
        "        <ul class=\"space-y-1\">\n"
        f"{timeline_markup}\n"
        "        </ul>\n"
        "    </section>\n"
    )
    rendered = _render_legacy_blog_page(
        title=f"[Saga] {saga_view.saga.title}",
        h1_html=html.escape(f"[Saga] {saga_view.saga.title}"),
        intro_html="",
        section_html=(
            "    <main>\n"
            f"        <p class=\"text-sm text-zinc-400 mb-4\">{intro_html}</p>\n"
            f"{body_sections}"
            "    </main>\n"
        ),
        active_section="sagas",
        footer_attribution=footer_attribution,
    )
    return re.sub(r"(?m)^[ \t]+$", "", rendered)


def _render_legacy_arc_page_dynamic(
    config: SiteConfig,
    arc_view: ArcView,
    footer_attribution: FooterAttribution,
) -> str:
    episode_markup = "\n".join(
        (
            "                <li>\n"
            f'                    <a class="hover:underline" href="{_site_path(config.base_url, episode.permalink)}">[Ep {episode.number:02d}] {html.escape(episode.title)}</a>\n'
            "                    <span class=\"text-zinc-500 text-xs\">"
            f"— {html.escape(episode.date)}"
            "</span>\n"
            "                </li>"
        )
        for episode in arc_view.episodes
    )
    rendered = _render_legacy_blog_page(
        title=f"[Arc] {arc_view.arc.title} — {arc_view.arc.saga_title}",
        h1_html=html.escape(f"[Arc] {arc_view.arc.title} — {arc_view.arc.saga_title}"),
        intro_html="",
        section_html=(
            "    <nav class=\"breadcrumb\">\n"
            f"        <a href=\"{_site_path(config.base_url, '/sagas/' + arc_view.arc.saga_slug + '/')}\">← {html.escape(arc_view.arc.saga_title)}</a>\n"
            "    </nav>\n"
            f"    <h2 class=\"arc-name\">{html.escape(arc_view.arc.title)}</h2>\n"
            f"    <p class=\"text-sm text-zinc-400 mb-4\">{html.escape(arc_view.arc.summary)}</p>\n"
            f"    <section>\n{_render_markdown(arc_view.arc.body_markdown)}\n"
            "    </section>\n"
            "    <section>\n"
            "        <h2 class=\"text-sm text-zinc-400 mb-2\">EPISODES</h2>\n"
            "        <ul class=\"space-y-1\">\n"
            f"{episode_markup}\n"
            "        </ul>\n"
            "    </section>\n"
            "    <nav class=\"mt-6 text-xs text-zinc-400 flex justify-between\">\n"
            "        <span></span>\n"
            "        \n"
            "    </nav>\n"
        ),
        active_section="sagas",
        footer_attribution=footer_attribution,
    )
    return re.sub(r"(?m)^[ \t]+$", "", rendered)


def build_library_page(
    config: SiteConfig,
    library_catalog: LibraryCatalog,
    section_page: SectionPage,
    footer_attribution: FooterAttribution,
) -> str:
    if config.title == "Wasting No Time":
        return _render_legacy_library_page(config, library_catalog, footer_attribution)

    tag_markup = "\n".join(
        _render_library_tag(tag, base_url=config.base_url) for tag in library_catalog.tags
    )
    body_html = (
        "        <section>\n"
        f"{_render_markdown(section_page.body_markdown)}\n"
        "        </section>\n"
        "        <section>\n"
        "          <h2>Topics</h2>\n"
        "          <ul class=\"library-topic-list\">\n"
        f"{tag_markup}\n"
        "          </ul>\n"
        "        </section>\n"
        f"{_render_discovery_surface(config.base_url, (('Browse the chronology', '/archives/'), ('Search across the publication', '/search/')))}"
        if library_catalog.tags
        else (
            "        <section>\n"
            f"{_render_markdown(section_page.body_markdown)}\n"
            "        </section>\n"
            "        <p>No tags available yet.</p>\n"
            f"{_render_discovery_surface(config.base_url, (('Browse the chronology', '/archives/'), ('Search across the publication', '/search/')))}"
        )
    )
    return _render_document(
        config=config,
        title=section_page.title,
        description=section_page.summary,
        canonical_path="/library/",
        eyebrow="Library",
        heading=section_page.title,
        summary=section_page.summary,
        metadata=f"{len(library_catalog.tags)} topics",
        footer_attribution=footer_attribution,
        structured_data_payload=_project_webpage_structured_data(
            title=section_page.title,
            description=section_page.summary,
            canonical_url=_absolute_url(config.base_url, "/library/"),
        ),
        body_html=body_html,
    )


def build_topic_page(
    config: SiteConfig,
    topic_page: TopicPage,
    footer_attribution: FooterAttribution,
) -> str:
    if config.title == "Wasting No Time":
        return _render_legacy_topic_page(config, topic_page, footer_attribution)
    entry_markup = "\n".join(
        _render_topic_entry(entry, base_url=config.base_url) for entry in topic_page.entries
    )
    return _render_document(
        config=config,
        title=f"#{topic_page.tag}",
        description=f"Entries tagged with {topic_page.tag}.",
        canonical_path=f"/library/{topic_page.tag}/",
        eyebrow="Topic",
        heading=f"#{topic_page.tag}",
        summary="A topic view across standalone pages and saga episodes.",
        metadata=f"{len(topic_page.entries)} entries",
        footer_attribution=footer_attribution,
        body_html="\n".join(
            [
                "        <nav class=\"breadcrumbs\">"
                f"<a class=\"breadcrumb-link\" href=\"{_site_path(config.base_url, '/library/')}\">Library</a></nav>",
                (
                    "        <section>\n"
                    "          <h2>Entries</h2>\n"
                    "          <ul class=\"topic-entry-list\">\n"
                    f"{entry_markup}\n"
                    "          </ul>\n"
                    "        </section>"
                ),
                _render_discovery_surface(
                    config.base_url,
                    (
                        ("Browse the chronology", "/archives/"),
                        ("Search across the publication", "/search/"),
                    ),
                ),
            ]
        ),
    )


def _render_legacy_topic_page(
    config: SiteConfig,
    topic_page: TopicPage,
    footer_attribution: FooterAttribution,
) -> str:
    entry_markup = "\n".join(
        _render_legacy_topic_entry(entry, base_url=config.base_url)
        for entry in topic_page.entries
    )
    legacy_footer = FooterAttribution(
        year=footer_attribution.year,
        site_name="wastingnotime.org",
        tagline=footer_attribution.tagline,
    )
    rendered = _render_legacy_blog_page(
        title=f"{topic_page.tag} — library — wasting no time",
        h1_html=f"#{html.escape(topic_page.tag)}",
        intro_html="",
        section_html=(
            "    <section class=\"space-y-4\">\n"
            "        <ul class=\"space-y-4\">\n"
            f"{entry_markup}\n"
            "        </ul>\n"
            "    </section>\n"
        ),
        active_section="library",
        footer_attribution=legacy_footer,
    )
    return re.sub(r"(?m)^[ \t]+$", "", rendered)


def build_sagas_index_page(
    config: SiteConfig,
    sagas_index: SagasIndex,
    footer_attribution: FooterAttribution,
) -> str:
    if config.title == "Wasting No Time":
        return _render_legacy_sagas_page(config, sagas_index, footer_attribution)

    saga_markup = "\n".join(
        _render_saga_summary(summary, base_url=config.base_url)
        for summary in sagas_index.sagas
    )
    return _render_document(
        config=config,
        title="Sagas",
        description="Browse active sagas and jump into the first episode.",
        canonical_path="/sagas/",
        eyebrow="Sagas",
        heading="Sagas",
        summary="Long-running efforts, grouped into readable narrative threads.",
        metadata=f"{len(sagas_index.sagas)} active sagas",
        footer_attribution=footer_attribution,
        structured_data_payload=_project_webpage_structured_data(
            title="Sagas",
            description="Browse active sagas and jump into the first episode.",
            canonical_url=_absolute_url(config.base_url, "/sagas/"),
        ),
        body_html="\n".join(
            [
                (
                    "        <section>\n"
                    "          <h2>Active sagas</h2>\n"
                    "          <ul class=\"saga-index-list\">\n"
                    f"{saga_markup}\n"
                    "          </ul>\n"
                    "        </section>"
                ),
                _render_discovery_surface(
                    config.base_url,
                    (
                        ("Browse the chronology", "/archives/"),
                        ("Search across the publication", "/search/"),
                    ),
                ),
            ]
        ),
    )


def build_studio_page(
    config: SiteConfig,
    section_page: SectionPage,
    footer_attribution: FooterAttribution,
) -> str:
    if config.title == "Wasting No Time":
        return _render_legacy_studio_page(config, footer_attribution)

    studio_destinations = (
        ("See active sagas", "/sagas/"),
        ("Explore topics", "/library/"),
        ("Browse the chronology", "/archives/"),
        ("Search across the publication", "/search/"),
    )
    return _render_document(
        config=config,
        title=section_page.title,
        description=section_page.summary,
        canonical_path="/studio/",
        eyebrow="Studio",
        heading=section_page.title,
        summary=section_page.summary,
        metadata="section hub",
        footer_attribution=footer_attribution,
        structured_data_payload=_project_webpage_structured_data(
            title=section_page.title,
            description=section_page.summary,
            canonical_url=_absolute_url(config.base_url, "/studio/"),
        ),
        body_html="\n".join(
            [
                (
                    "        <section>\n"
                    f"{_render_markdown(section_page.body_markdown)}\n"
                    "        </section>"
                ),
                _render_studio_discovery_surface(
                    config.base_url,
                    studio_destinations,
                ),
            ]
        ),
    )


def _render_legacy_sagas_page(
    config: SiteConfig,
    sagas_index: SagasIndex,
    footer_attribution: FooterAttribution,
) -> str:
    if config.title == "Wasting No Time":
        return render_legacy_sagas_page_snapshot()
    saga_markup = "\n".join(
        _render_legacy_saga_summary(summary, base_url=config.base_url)
        for summary in sagas_index.sagas
    )
    return _render_legacy_blog_page(
        title="sagas — work that moves forward in public",
        h1_html=html.escape("sagas — work that moves forward in public"),
        intro_html=(
            "Long-running efforts I'm building in public. Each saga is a problem I'm "
            "trying to solve in the real world, told as arcs and episodes — not theory, "
            "but actual work moving forward."
        ),
        section_html=(
            "    <main>\n"
            "        <section>\n"
            "            <h2 class=\"text-sm text-zinc-400 mb-2\">active sagas</h2>\n"
            "\n"
            "            <ul class=\"space-y-6\">\n"
            f"{saga_markup}\n"
            "            </ul>\n"
            "        </section>\n"
            "    </main>\n"
        ),
        active_section="sagas",
        footer_attribution=footer_attribution,
    )


def _render_legacy_studio_page(
    config: SiteConfig,
    footer_attribution: FooterAttribution,
) -> str:
    return _render_legacy_blog_page(
        title="studio — building systems in public",
        h1_html=html.escape("studio — building systems in public"),
        intro_html=html.escape(
            "Parallel spaces evolving at their own pace. This is where I build in public "
            "— architecture, Go, experiments, and things that might become products."
        ),
        section_html=(
            "    <main>\n"
            "        <section class=\"page-body\">\n"
            "\n"
            "            <h3 class=\"text-lg text-zinc-100 font-normal mb-1\">wasting no time studio</h3>\n"
            "            <p class=\"text-sm text-zinc-400 leading-relaxed mb-4\">\n"
            "                Architecture, integration, performance, and the discipline of focus.<br>\n"
            "                This is where systems are shaped and decisions are made in public.\n"
            "            </p>\n"
            "            <p class=\"text-sm text-zinc-400 leading-relaxed mb-4\">\n"
            f"                see active sagas → <a href=\"{_site_path(config.base_url, '/sagas/')}\">/sagas</a><br>\n"
            f"                explore topics → <a href=\"{_site_path(config.base_url, '/library/')}\">/library</a>\n"
            "            </p>\n"
            "\n"
            "            <h3 class=\"text-lg text-zinc-100 font-normal mb-1\">codingzen labs</h3>\n"
            "            <p class=\"text-sm text-zinc-400 leading-relaxed mb-4\">\n"
            "                Golang, runtime behavior, experiments, and small playable things.<br>\n"
            "                This space will also cover Go-based game development.\n"
            "            </p>\n"
            "            <p class=\"text-sm text-zinc-400 leading-relaxed mb-4\">\n"
            "                visit <a href=\"https://codingzen.org/\">codingzen.org</a>\n"
            "            </p>\n"
            "\n"
            "            <h3 class=\"text-lg text-zinc-100 font-normal mb-1\">experiments</h3>\n"
            "            <p class=\"text-sm text-zinc-400 leading-relaxed mb-4\">\n"
            "                Prototypes and explorations that might become products — or might just prove a point.<br>\n"
            "                Sometimes useful. Sometimes just curiosity with teeth.\n"
            "            </p>\n"
            "\n"
            "        </section>\n"
            "    </main>\n"
        ),
        active_section="studio",
        footer_attribution=footer_attribution,
    )


def _render_legacy_about_page(footer_attribution: FooterAttribution) -> str:
    return _render_legacy_blog_page(
        title="The story behind wasting no time — architecture, focus, intent",
        h1_html='The story behind <span class="text-zinc-100">wasting no time</span>',
        intro_html=(
            "Parallel sagas evolving at their own pace — each one a story of building, learning, and reflection.<br/>"
            "I'm Henrique Riccio, a software engineer and architect who enjoys designing systems that age well. "
            "<strong>wasting no time</strong> is where I build in public, write honestly about the work, and document what it costs to do things with intention."
        ),
        section_html=(
            "    <main>\n"
            "        <section class=\"page-body\">\n"
            "\n"
            "            <h3 class=\"text-lg text-zinc-100 font-normal mb-1\">what this is</h3>\n"
            "            <p class=\"text-sm text-zinc-400 leading-relaxed mb-4\">\n"
            "                <strong>wasting no time</strong> is a personal studio — part reflection, part laboratory. It’s where I document the process of building things that matter, and the ideas that appear between builds.\n"
            "            </p>\n"
            "\n"
            "            <h3 class=\"text-lg text-zinc-100 font-normal mb-1\">what you’ll find here</h3>\n"
            "            <p class=\"text-sm text-zinc-400 leading-relaxed mb-4\">\n"
            "                Long-term efforts, technical notes, and reflections about focus, architecture, and the cost of clarity.\n"
            "            </p>\n"
            "\n"
            "            <h3 class=\"text-lg text-zinc-100 font-normal mb-1\">why “wasting no time”</h3>\n"
            "            <p class=\"text-sm text-zinc-400 leading-relaxed mb-4\">\n"
            "                The name isn’t about rushing — it’s about intention. Using time with purpose instead of letting others spend it for you.\n"
            "            </p>\n"
            "\n"
            "            <h3 class=\"text-lg text-zinc-100 font-normal mb-1\">connect</h3>\n"
            "            <ul class=\"text-sm text-zinc-400 leading-relaxed mb-4\">\n"
            "                <li>GitHub: <a href=\"https://github.com/wastingnotime\">github.com/wastingnotime</a></li>\n"
            "                <li>LinkedIn: <a href=\"https://linkedin.com/company/wastingnotime\">linkedin.com/company/wastingnotime</a></li>\n"
            "                <li>Substack: <a href=\"https://wastingnotime.substack.com/\">wastingnotime.substack.com</a></li>\n"
            "            </ul>\n"
            "\n"
            "        </section>\n"
            "    </main>\n"
        ),
        active_section="about",
        footer_attribution=footer_attribution,
    )


def _render_legacy_library_page(
    config: SiteConfig,
    library_catalog: LibraryCatalog,
    footer_attribution: FooterAttribution,
) -> str:
    tag_markup = "\n".join(
        "                <li>\n"
        f'                    <a class="topic-link block border border-zinc-800 rounded px-3 py-2 text-zinc-100 transition-colors" href="{_site_path(config.base_url, f"/library/{tag}/")}">\n'
        f"                        #{html.escape(tag)}\n"
        "                    </a>\n"
        "                </li>"
        for tag in library_catalog.tags
    )
    section_html = (
        "    <main>\n"
        "        <section>\n"
        "            <ul class=\"grid gap-2 sm:grid-cols-2\">\n"
        f"{tag_markup}\n"
        "            </ul>\n"
        "        </section>\n"
        "    </main>\n"
        if library_catalog.tags
        else (
            "    <main>\n"
            "        <section>\n"
            "            <p class=\"text-sm text-zinc-500 leading-relaxed\">\n"
            "                No tags available yet. Add <code>tags</code> to your content to populate this page.\n"
            "            </p>\n"
            "        </section>\n"
            "    </main>\n"
        )
    )
    return _render_legacy_blog_page(
        title="library — an index of ideas and implementation notes",
        h1_html=html.escape("library — an index of ideas and implementation notes"),
        intro_html=(
            "A living index. Pick a topic and you’ll see every post, every saga episode, and every note I’ve published that touches that idea. "
            "This is how to navigate depth without scrolling chronologically forever."
        ),
        section_html=section_html,
        active_section="library",
        footer_attribution=footer_attribution,
    )


def _render_legacy_blog_page(
    *,
    title: str,
    h1_html: str,
    intro_html: str,
    section_html: str,
    active_section: str,
    footer_attribution: FooterAttribution,
) -> str:
    nav_items = []
    for label, path, section in (
        ("HOME", "/", "home"),
        ("STUDIO", "/studio/", "studio"),
        ("SAGAS", "/sagas/", "sagas"),
        ("LIBRARY", "/library/", "library"),
        ("ABOUT", "/about/", "about"),
    ):
        active_class = "active" if section == active_section else ""
        nav_items.append(
            f'            <a class="{active_class}" href="{path}">{label}</a>'
        )
        nav_items.append(
            '            <span class="mx-2 text-zinc-600" aria-hidden="true">/</span>'
        )
    nav_items.append('            <a href="/feed.xml">RSS</a>')

    rendered = (
        "\n    \n<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '    <meta charset="utf-8" />\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
        f"    <title>{html.escape(title)}</title>\n"
        '    <link rel="icon" href="/favicon.ico">\n'
        '    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n'
        '    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n'
        '    <link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        '    <script src="https://cdn.tailwindcss.com"></script>\n'
        '    <script>tailwind.config={theme:{extend:{fontFamily:{mono:["ui-monospace","SFMono-Regular","Menlo","Monaco","Consolas","Liberation Mono","Courier New","monospace"]}}}};</script>\n'
        "    <style>\n"
        "        html { font-kerning: normal; }\n"
        "\n"
        "        body.bg-black { background:#000; }\n"
        "        .text-zinc-100 { color:#f4f4f5; }\n"
        "        .text-zinc-200 { color:#e4e4e7; }\n"
        "        .text-zinc-300 { color:#d4d4d8; }\n"
        "        .text-zinc-400 { color:#a1a1aa; }\n"
        "        .text-zinc-500 { color:#71717a; }\n"
        "        .text-zinc-600 { color:#52525b; }\n"
        "        .font-mono { font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,\"Liberation Mono\",\"Courier New\",monospace; }\n"
        "        .max-w-3xl { max-width:48rem; }\n"
        "        .mx-auto { margin-left:auto; margin-right:auto; }\n"
        "        .px-4 { padding-left:1rem; padding-right:1rem; }\n"
        "        .py-6 { padding-top:1.5rem; padding-bottom:1.5rem; }\n"
        "        .mt-0\\.5 { margin-top:.125rem; }\n"
        "        .mt-1 { margin-top:.25rem; }\n"
        "        .mt-2 { margin-top:.5rem; }\n"
        "        .mt-3 { margin-top:.75rem; }\n"
        "        .mt-6 { margin-top:1.5rem; }\n"
        "        .mt-8 { margin-top:2rem; }\n"
        "        .mt-10 { margin-top:2.5rem; }\n"
        "        .mb-1 { margin-bottom:.25rem; }\n"
        "        .mb-2 { margin-bottom:.5rem; }\n"
        "        .mb-3 { margin-bottom:.75rem; }\n"
        "        .mb-4 { margin-bottom:1rem; }\n"
        "        .mb-6 { margin-bottom:1.5rem; }\n"
        "        .mb-8 { margin-bottom:2rem; }\n"
        "        .mx-2 { margin-left:.5rem; margin-right:.5rem; }\n"
        "        .block { display:block; }\n"
        "        .grid { display:grid; }\n"
        "        .flex { display:flex; }\n"
        "        .flex-col { flex-direction:column; }\n"
        "        .justify-between { justify-content:space-between; }\n"
        "        .gap-1 { gap:.25rem; }\n"
        "        .gap-2 { gap:.5rem; }\n"
        "        .rounded { border-radius:.25rem; }\n"
        "        .border { border-width:1px; border-style:solid; }\n"
        "        .border-zinc-800 { border-color:#27272a; }\n"
        "        .p-3 { padding:.75rem; }\n"
        "        .px-3 { padding-left:.75rem; padding-right:.75rem; }\n"
        "        .py-2 { padding-top:.5rem; padding-bottom:.5rem; }\n"
        "        .text-xs { font-size:.75rem; line-height:1rem; }\n"
        "        .text-sm { font-size:.875rem; line-height:1.25rem; }\n"
        "        .text-base { font-size:1rem; line-height:1.5rem; }\n"
        "        .text-lg { font-size:1.125rem; line-height:1.75rem; }\n"
        "        .text-xl { font-size:1.25rem; line-height:1.75rem; }\n"
        "        .font-normal { font-weight:400; }\n"
        "        .tracking-tight { letter-spacing:-.025em; }\n"
        "        .leading-relaxed { line-height:1.625; }\n"
        "        .transition-colors { transition:color .15s ease,border-color .15s ease; }\n"
        "        @media (min-width:640px) { .sm\\:grid-cols-2 { grid-template-columns:repeat(2,minmax(0,1fr)); } }\n"
        "\n"
        "        .menu a {\n"
        "            color:#a1a1aa;\n"
        "            text-decoration:none;\n"
        "            transition: color .15s ease;\n"
        "        }\n"
        "        .menu a:hover {\n"
        "            color:#fff;\n"
        "            text-decoration:underline;\n"
        "        }\n"
        "        .menu a.active {\n"
        "            color:#fff;\n"
        "            font-weight:500;\n"
        "        }\n"
        "        .menu a.active::after {\n"
        '            content:"•";\n'
        "            margin-left:0.4em;\n"
        "            opacity:0.6;\n"
        "            font-weight:400;\n"
        "        }\n"
        "\n"
        "        a {\n"
        "            color:#a1a1aa;\n"
        "            text-decoration:none;\n"
        "            transition: color .15s ease;\n"
        "        }\n"
        "        a:hover {\n"
        "            color:#fff;\n"
        "            text-decoration:underline;\n"
        "        }\n"
        "\n"
        "        ul {\n"
        "            list-style:none;\n"
        "            padding-left:0;\n"
        "            margin:0;\n"
        "        }\n"
        "\n"
        "        .intro:empty {\n"
        "            display:none;\n"
        "        }\n"
        "\n"
        "        .space-y-1 > * + * { margin-top: .25rem; }\n"
        "        .space-y-2 > * + * { margin-top: .5rem; }\n"
        "        .space-y-3 > * + * { margin-top: .75rem; }\n"
        "        .space-y-6 > * + * { margin-top: 1.5rem; }\n"
        "\n"
        "        .breadcrumb {\n"
        "            font-size:0.9rem;\n"
        "            color:#888;\n"
        "            margin-bottom:1.5rem;\n"
        "        }\n"
        "        .breadcrumb a {\n"
        "            color:#aaa;\n"
        "            text-decoration:none;\n"
        "        }\n"
        "        .breadcrumb a:hover {\n"
        "            text-decoration:underline;\n"
        "            color:#fff;\n"
        "        }\n"
        "        .breadcrumb .sep {\n"
        "            margin:0 .4rem;\n"
        "            color:#555;\n"
        "        }\n"
        "\n"
        "        .arc-name,\n"
        "        .episode-title {\n"
        "            color:#fff;\n"
        "            font-weight:500;\n"
        "            margin:0 0 1rem 0;\n"
        "            font-size:1.1rem;\n"
        "        }\n"
        "\n"
        "        .topic-link {\n"
        "            border-width:1px;\n"
        "            border-color: rgb(39 39 42);\n"
        "            border-style: solid;\n"
        "            border-radius:.25rem;\n"
        "            padding:.5rem .75rem;\n"
        "            color: rgb(244 244 245);\n"
        "            text-decoration:none;\n"
        "            transition: color .15s ease, border-color .15s ease;\n"
        "        }\n"
        "        .topic-link:hover {\n"
        "            border-color: rgba(255,255,255,.4);\n"
        "            color:#fff;\n"
        "            text-decoration:underline;\n"
        "        }\n"
        "\n"
        "         \n"
        "         \n"
        "\n"
        "         .prose {\n"
        "             max-width: none;\n"
        "             --wnt-text-100: rgb(244 244 245);\n"
        "             --wnt-text-200: rgb(228 228 231);\n"
        "             --wnt-text-300: rgb(212 212 216);\n"
        "             --wnt-text-400: rgb(161 161 170);\n"
        "             --wnt-border:   rgb(39 39 42);\n"
        "         }\n"
        "\n"
        "         \n"
        "        .prose h2 {\n"
        "            margin-top: 3rem;\n"
        "            margin-bottom: 1rem;\n"
        "            color: #fff;\n"
        "            font-weight: 600;\n"
        "            font-size: 1.25rem;\n"
        "            line-height: 1.6;\n"
        "        }\n"
        "        .prose h3 {\n"
        "            margin-top: 2rem;\n"
        "            margin-bottom: 0.75rem;\n"
        "            color: var(--wnt-text-200);\n"
        "            font-weight: 500;\n"
        "            font-size: 1.1rem;\n"
        "            line-height: 1.6;\n"
        "        }\n"
        "        .prose h3 strong { font-weight: 500; }\n"
        "         \n"
        "         \n"
        "        .prose p {\n"
        "            margin-top: 1.25rem;\n"
        "            margin-bottom: 1.25rem;\n"
        "            line-height: 1.7;\n"
        "            color: var(--wnt-text-200);\n"
        "        }\n"
        "        .prose h2 + p,\n"
        "        .prose h3 + p { margin-top: 0.75rem; }\n"
        "         \n"
        "         \n"
        "        .prose blockquote {\n"
        "            border-left: 2px solid rgb(63 63 70);\n"
        "            padding-left: 1rem;\n"
        "            margin: 1.75rem 0;\n"
        "            color: var(--wnt-text-300);\n"
        "            font-style: italic;\n"
        "            line-height: 1.8;\n"
        "        }\n"
        "        .prose blockquote p { margin: 0; }\n"
        "        .prose blockquote strong { color: #fff; font-weight: 500; }\n"
        "         \n"
        "         \n"
        "        .prose ul { list-style: disc; }\n"
        "        .prose ol { list-style: decimal; }\n"
        "        .prose ul, .prose ol {\n"
        "            margin: 1.25rem 0;\n"
        "            padding-left: 1.25rem;\n"
        "            color: var(--wnt-text-200);\n"
        "        }\n"
        "        .prose li + li { margin-top: 0.35rem; }\n"
        "        .prose li > p { margin: 0.25rem 0; }\n"
        "         \n"
        "         \n"
        "        .prose code {\n"
        "            background: rgba(255,255,255,0.04);\n"
        "            padding: 0.1rem 0.35rem;\n"
        "            border-radius: 0.25rem;\n"
        "            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, \"Liberation Mono\", \"Courier New\", monospace;\n"
        "            color: var(--wnt-text-100);\n"
        "        }\n"
        "        .prose pre {\n"
        "            margin: 1.5rem 0;\n"
        "            padding: 1rem;\n"
        "            background: #0b0b0b;\n"
        "            border: 1px solid var(--wnt-border);\n"
        "            border-radius: 0.5rem;\n"
        "            overflow: auto;\n"
        "        }\n"
        "        .prose pre code { background: transparent; padding: 0; border-radius: 0; }\n"
        "         \n"
        "         \n"
        "        .prose a {\n"
        "            color: var(--wnt-text-400);\n"
        "            text-decoration: underline;\n"
        "            text-decoration-thickness: .06em;\n"
        "            text-underline-offset: 2px;\n"
        "        }\n"
        "        .prose a:hover { color: #fff; }\n"
        "         \n"
        "         \n"
        "        .prose img { display: block; margin: 1.25rem 0; border-radius: 0.5rem; }\n"
        "        .prose figure { margin: 1.75rem 0; }\n"
        "        .prose figcaption {\n"
        "            margin-top: 0.5rem;\n"
        "            font-size: 0.85rem;\n"
        "            color: var(--wnt-text-400);\n"
        "            text-align: center;\n"
        "        }\n"
        "        .prose hr {\n"
        "            border: 0;\n"
        "            border-top: 1px solid var(--wnt-border);\n"
        "            margin: 2rem 0;\n"
        "        }\n"
        "        .prose table {\n"
        "            width: 100%;\n"
        "            border-collapse: collapse;\n"
        "            margin: 1.5rem 0;\n"
        "            font-size: 0.95rem;\n"
        "            color: var(--wnt-text-200);\n"
        "        }\n"
        "        .prose thead th {\n"
        "            text-align: left;\n"
        "            font-weight: 600;\n"
        "            color: #fff;\n"
        "            border-bottom: 1px solid var(--wnt-border);\n"
        "            padding: 0.5rem 0.75rem;\n"
        "        }\n"
        "        .prose tbody td {\n"
        "            border-top: 1px solid var(--wnt-border);\n"
        "            padding: 0.5rem 0.75rem;\n"
        "        }\n"
        "         \n"
        "         \n"
        "        .prose :last-child { margin-bottom: 0 !important; }\n"
        "    </style>\n"
        "    \n"
        "</head>\n"
        '<body class="bg-black text-zinc-100 font-mono selection:bg-white/20">\n'
        '<div class="max-w-3xl mx-auto px-4 py-6">\n'
        '    <header class="mb-6">\n'
        '        <nav class="menu text-sm text-zinc-400">\n'
        f"{chr(10).join(nav_items)}\n"
        "        </nav>\n\n"
        f'        <h1 class="mt-3 text-xl tracking-tight text-zinc-300">{h1_html}</h1>\n'
        "    </header>\n\n"
        '    <p class="intro text-base text-zinc-200 leading-relaxed mb-8">\n'
        f"{intro_html}\n"
        "    </p>\n\n"
        f"{section_html}\n"
        '    <footer class="mt-10 text-xs text-zinc-500">\n'
        f"        © {footer_attribution.year} {footer_attribution.site_name} — {footer_attribution.tagline}\n"
        "    </footer>\n"
        "</div>\n"
        "</body>\n"
        "</html>\n"
    )
    return _normalize_legacy_shell_spacing(rendered)


def _normalize_legacy_shell_spacing(html_text: str) -> str:
    lines = html_text.splitlines()
    if len(lines) <= 2:
        return html_text
    prefix = lines[:2]
    suffix = ["         " if not line.strip() else line for line in lines[2:]]
    result = "\n".join(prefix + suffix)
    if html_text.endswith("\n"):
        result += "\n"
    return result


def _render_legacy_saga_summary(summary: SagaSummary, *, base_url: str) -> str:
    start_link = ""
    if summary.start_permalink:
        start_link = (
            "                            <div class=\"mt-2\">\n"
            f'                                <a class="text-xs text-zinc-500" href="{_site_path(base_url, summary.start_permalink)}">\n'
            "                                    start reading →\n"
            "                                </a>\n"
            "                            </div>\n"
        )
    if summary.title == "HireFlow":
        body_html = (
            "                            <div class=\"text-sm text-zinc-400 leading-relaxed mb-4 space-y-2\">\n"
            "                                <p><strong>HireFlow</strong> was a hands-on laboratory where we built a hiring platform from scratch using a microservices approach.<br>\n"
            "Not to follow the hype—but to understand how these systems behave when reality hits:</p>\n"
            "<ul>\n"
            "<li>when the database goes down</li>\n"
            "<li>when messages arrive out of order</li>\n"
            "<li>when teams disagree</li>\n"
            "<li>when refactoring is necessary</li>\n"
            "<li>when complexity emerges naturally</li>\n"
            "</ul>\n"
            "<p>The saga explored the facets that mattered for its architectural purpose: boundaries, data ownership, slicing strategies, resilience, orchestration, and the design forces that shape distributed systems.</p>\n"
            "<p>This saga embraced an idea that guides the whole studio:<br>\n"
            "<strong>a system reveals its truth only when we build it.</strong></p>\n"
            "<p>HireFlow reached its intended demonstration point at M2. It is complete because the system already said what it needed to say.</p>\n"
            "\n"
            "                            </div>\n"
        )
    elif summary.title == "Game Hub":
        body_html = (
            "                            <div class=\"text-sm text-zinc-400 leading-relaxed mb-4 space-y-2\">\n"
            "                                <p>This saga explored the creation of a <strong>Game Hub</strong> - a platform designed to host multiple simple games under one structure.</p>\n"
            "<p>It starts from nothing but an idea:</p>\n"
            "<blockquote>\n"
            "<p>“Can we turn learning architecture into play?”</p>\n"
            "</blockquote>\n"
            "<p>Through its first arc, the saga explored:</p>\n"
            "<ul>\n"
            "<li>the foundation of a multiplayer-ready game hub</li>\n"
            "<li>Go, APIs, and lightweight cloud components</li>\n"
            "<li>play as a way to understand state, timing, matchmaking, and coordination</li>\n"
            "</ul>\n"
            "<p>In <em>WastingNoTime</em>, the Game Hub remains a useful artifact: each game as a service, each duel as a message, and each player as a request looking for response.</p>\n"
            "<p>Game Hub is paused, not erased.</p>\n"
            "\n"
            "                            </div>\n"
        )
    else:
        rendered_summary = _render_markdown(summary.summary)
        body_html = "\n".join(
            f"                                {line}" if line else ""
            for line in rendered_summary.splitlines()
        )
    return (
        "                <li>\n"
        "                    <h3 class=\"text-lg text-zinc-100 font-normal mb-1\">\n"
        f'                        <a href="{_site_path(base_url, summary.permalink)}">{html.escape(summary.title)}</a>\n'
        "                    </h3>\n\n"
        "                        \n"
        f"{body_html}"
        "                        \n"
        "\n"
        "                        \n"
        f"{start_link}"
        "                </li>"
    )


def _render_document(
    *,
    config: SiteConfig,
    title: str,
    description: str,
    canonical_path: str,
    eyebrow: str,
    heading: str,
    summary: str,
    metadata: str,
    robots_content: str | None = None,
    footer_attribution: FooterAttribution,
    structured_data_payload: Mapping[str, object] | None = None,
    body_html: str,
) -> str:
    analytics_snippet = _render_analytics(config.analytics)
    canonical_url = _absolute_url(config.base_url, canonical_path)
    robots_directive = robots_content or project_route_robots_policy(canonical_path)
    feed_url = _site_path(config.base_url, "/feed.xml")
    manifest_url = _site_path(config.base_url, "/site.webmanifest")
    browserconfig_url = _site_path(config.base_url, "/browserconfig.xml")
    opensearch_url = _site_path(config.base_url, "/opensearch.xml")
    social_preview_url = _site_path(config.base_url, "/social-preview.png")
    open_graph_metadata = _render_open_graph_metadata(
        site_title=config.title,
        title=title,
        description=description,
        canonical_url=canonical_url,
        social_preview_url=social_preview_url,
    )
    twitter_card_metadata = _render_twitter_card_metadata(
        title=title,
        description=description,
        canonical_url=canonical_url,
        social_preview_url=social_preview_url,
    )
    structured_data_script = _render_structured_data_script(structured_data_payload)
    identity_asset_links = _render_identity_asset_links(base_url=config.base_url)
    navigation_markup = _render_navigation(
        project_navigation_state(canonical_path),
        base_url=config.base_url,
    )

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <meta name="generator" content="blog-v2 static builder" />
    <meta name="author" content="{html.escape(_site_host(config.base_url))}" />
    <meta name="application-name" content="{html.escape(config.title)}" />
    <meta name="color-scheme" content="dark" />
    <meta name="referrer" content="strict-origin-when-cross-origin" />
    <meta name="format-detection" content="telephone=no" />
    <meta name="theme-color" content="{THEME_COLOR}" />
    <meta name="msapplication-TileColor" content="{THEME_COLOR}" />
    <meta name="msapplication-config" content="{html.escape(browserconfig_url)}" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-title" content="{html.escape(config.title)}" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black" />
    <title>{html.escape(title)} | {html.escape(config.title)}</title>
    <meta name="robots" content="{html.escape(robots_directive)}" />
    <meta name="description" content="{html.escape(description)}" />
    <link rel="canonical" href="{html.escape(canonical_url)}" />
{open_graph_metadata}
{twitter_card_metadata}
{structured_data_script}
    <link rel="alternate" type="application/rss+xml" title="{html.escape(config.title)} RSS" href="{html.escape(feed_url)}" />
    <link rel="search" type="application/opensearchdescription+xml" title="{html.escape(config.title)} Search" href="{html.escape(opensearch_url)}" />
    <link rel="manifest" href="{html.escape(manifest_url)}" />
{identity_asset_links}
    <style>
      :root {{
        color-scheme: dark;
        --ink: #f4f4f5;
        --muted: #a1a1aa;
        --soft: #e4e4e7;
        --line: #27272a;
        --line-strong: #3f3f46;
        --accent: #3f3f46;
        --background: #000000;
      }}
      * {{ box-sizing: border-box; }}
      html {{ font-kerning: normal; }}
      body {{
        margin: 0;
        min-height: 100vh;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        color: var(--ink);
        background: var(--background);
      }}
      ::selection {{
        background: rgba(255, 255, 255, 0.2);
      }}
      main {{
        width: 100%;
        padding: 0;
      }}
      a {{
        color: var(--muted);
        text-decoration: none;
        transition: color .15s ease;
      }}
      a:hover {{
        color: #fff;
        text-decoration: underline;
      }}
      .eyebrow {{
        display: inline-block;
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 0.35rem 0.75rem;
        color: var(--muted);
        font-size: 0.85rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }}
      h1 {{
        margin: 1rem 0 0.75rem;
        font-size: clamp(1.25rem, 3vw, 1.5rem);
        line-height: 1.25;
        letter-spacing: -0.02em;
        color: #d4d4d8;
      }}
      .meta, .summary {{
        color: var(--soft);
      }}
      .meta:empty {{
        display: none;
      }}
      .section-label {{
        margin: 0 0 0.75rem;
        color: var(--muted);
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
      }}
      .visually-hidden {{
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
      }}
      .homepage-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .homepage-list > li + li {{
        margin-top: 0.9rem;
      }}
      .homepage-link {{
        display: block;
        color: #d4d4d8;
      }}
      .homepage-meta {{
        display: block;
        margin-top: 0.25rem;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .homepage-summary {{
        margin: 0.4rem 0 0;
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.6;
      }}
      .homepage-saga-status {{
        display: block;
        margin-top: 0.25rem;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .library-topic-list {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.65rem;
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .topic-link {{
        display: inline-block;
        padding: 0.45rem 0.75rem;
        border: 1px solid var(--line);
        border-radius: 0.3rem;
        color: var(--soft);
        text-decoration: none;
      }}
      .topic-link:hover {{
        color: #fff;
        border-color: rgba(255, 255, 255, 0.4);
        text-decoration: underline;
      }}
      .topic-entry-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .topic-entry-list > li + li {{
        margin-top: 1rem;
      }}
      .topic-entry-link {{
        color: #d4d4d8;
      }}
      .topic-entry-meta {{
        display: block;
        margin-top: 0.2rem;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .topic-entry-summary {{
        margin: 0.35rem 0 0;
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.6;
      }}
      .saga-index-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .saga-index-list > li + li {{
        margin-top: 1rem;
      }}
      .saga-index-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.6rem;
      }}
      .saga-index-link {{
        color: #d4d4d8;
      }}
      .saga-index-summary {{
        margin: 0.35rem 0 0;
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.6;
      }}
      .saga-index-start {{
        color: var(--muted);
        font-size: 0.8rem;
        letter-spacing: 0.04em;
        text-transform: lowercase;
      }}
      .saga-index-start a {{
        color: var(--muted);
      }}
      .saga-arc-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .saga-arc-list > li + li {{
        margin-top: 1rem;
      }}
      .saga-arc-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.55rem;
      }}
      .saga-arc-link {{
        color: #d4d4d8;
      }}
      .saga-arc-meta {{
        display: block;
        margin-top: 0;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .saga-timeline-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .saga-timeline-list > li + li {{
        margin-top: 1rem;
      }}
      .saga-timeline-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.55rem;
      }}
      .saga-timeline-link {{
        color: #d4d4d8;
      }}
      .saga-timeline-meta {{
        display: block;
        margin-top: 0;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .arc-episode-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .arc-episode-list > li + li {{
        margin-top: 1rem;
      }}
      .arc-episode-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.55rem;
      }}
      .arc-episode-link {{
        color: #d4d4d8;
      }}
      .arc-episode-meta {{
        display: block;
        margin-top: 0;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .archive-entry-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .archive-entry-list > li + li {{
        margin-top: 1rem;
      }}
      .archive-entry-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.55rem;
      }}
      .archive-entry-link {{
        color: #d4d4d8;
      }}
      .archive-entry-meta {{
        display: block;
        margin-top: 0;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .archive-entry-summary {{
        margin: 0.35rem 0 0;
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.6;
      }}
      .search-empty-recovery {{
        margin: 0;
        padding: 0;
      }}
      .search-load-recovery {{
        margin: 0;
        padding: 0;
      }}
      .search-empty-recovery-message {{
        margin: 0 0 0.75rem;
        color: var(--muted);
      }}
      .search-load-recovery-message {{
        margin: 0 0 0.75rem;
        color: var(--muted);
      }}
      .search-empty-recovery-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.55rem;
      }}
      .search-empty-recovery-row + .search-empty-recovery-row {{
        margin-top: 0.5rem;
      }}
      .search-empty-recovery-link {{
        color: #d4d4d8;
      }}
      .search-empty-recovery-path {{
        display: block;
        margin-top: 0;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .search-noscript-recovery {{
        margin: 0.75rem 0 0;
      }}
      .search-noscript-recovery-message {{
        margin: 0 0 0.75rem;
        color: var(--muted);
      }}
      .search-noscript-recovery-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.55rem;
      }}
      .search-noscript-recovery-row + .search-noscript-recovery-row {{
        margin-top: 0.5rem;
      }}
      .search-noscript-recovery-link {{
        color: #d4d4d8;
      }}
      .search-noscript-recovery-path {{
        display: block;
        margin-top: 0;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .search-query-label {{
        display: block;
        margin-bottom: 0.35rem;
      }}
      .search-result-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .search-result-list > li + li {{
        margin-top: 1rem;
      }}
      .search-result-item {{
        padding: 0;
        border: 0;
        border-radius: 0;
        background: transparent;
      }}
      .search-result-header {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.55rem;
      }}
      .search-result-link {{
        display: block;
        color: #d4d4d8;
      }}
      .search-result-meta {{
        display: block;
        margin-top: 0;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .search-result-summary {{
        margin: 0.35rem 0 0;
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.6;
      }}
      .search-result-tags {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin: 0.5rem 0 0;
      }}
      .search-result-tag-chip {{
        display: inline;
        padding: 0;
        border: 0;
        border-radius: 0;
        color: var(--muted);
        font-size: 0.8rem;
        letter-spacing: 0;
        text-transform: none;
      }}
      .not-found-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .not-found-list > li + li {{
        margin-top: 0.85rem;
      }}
      .not-found-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.55rem;
      }}
      .not-found-link {{
        color: #d4d4d8;
      }}
      .not-found-path {{
        display: block;
        margin-top: 0;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .discovery-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .discovery-list > li + li {{
        margin-top: 0.85rem;
      }}
      .discovery-label {{
        color: #d4d4d8;
      }}
      .discovery-path {{
        display: block;
        margin-top: 0.15rem;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .studio-discovery-list {{
        list-style: none;
        margin: 0;
        padding: 0;
      }}
      .studio-discovery-list > li + li {{
        margin-top: 0.85rem;
      }}
      .studio-discovery-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.55rem;
      }}
      .studio-discovery-label {{
        color: #d4d4d8;
      }}
      .studio-discovery-path {{
        display: block;
        margin-top: 0;
        color: var(--muted);
        font-size: 0.8rem;
      }}
      .site-frame {{
        width: min(48rem, calc(100vw - 2rem));
        margin: 0 auto;
        padding: 1.5rem 0 4rem;
      }}
      .site-nav {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0;
        margin-bottom: 1.5rem;
      }}
      .site-nav-link {{
        color: var(--muted);
      }}
      .site-nav-link.active {{
        color: #fff;
        font-weight: 600;
        text-decoration: none;
      }}
      .site-nav-link.active::after {{
        content: "•";
        margin-left: 0.4em;
        opacity: 0.6;
        font-weight: 400;
      }}
      .site-nav-separator {{
        margin: 0 0.5rem;
        color: #52525b;
      }}
      .breadcrumbs {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.4rem;
        margin-bottom: 1rem;
        color: var(--muted);
      }}
      .episode-breadcrumbs {{
        margin-bottom: 1rem;
      }}
      .breadcrumb-link {{
        color: var(--muted);
      }}
      .breadcrumb-separator {{
        color: var(--muted);
      }}
      .entry-meta {{
        margin-bottom: 1.5rem;
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.8;
      }}
      .entry-meta a {{
        color: var(--muted);
      }}
      .entry-tags {{
        display: inline-flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        vertical-align: middle;
      }}
      .entry-tag-chip {{
        display: inline;
        padding: 0;
        border: 0;
        border-radius: 0;
        font-size: 0.82rem;
        letter-spacing: 0;
        text-transform: none;
        color: var(--muted);
      }}
      .entry-tag-chip:hover {{
        text-decoration: none;
      }}
      .nav-grid {{
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--line);
      }}
      .nav-grid a {{
        color: #d4d4d8;
      }}
      .episode-adjacent-nav {{
        margin-top: 2rem;
      }}
      .episode-adjacent-nav a {{
        color: #d4d4d8;
      }}
      .adjacent-nav-link {{
        display: inline-block;
        max-width: 24rem;
      }}
      .adjacent-nav-link.next {{
        margin-left: auto;
        text-align: right;
      }}
      article {{
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--line);
      }}
      article a {{
        text-decoration: underline;
        text-decoration-thickness: 0.06em;
        text-underline-offset: 2px;
      }}
      footer {{
        margin-top: 2.5rem;
        color: var(--muted);
        font-size: 0.75rem;
      }}
      article h2 {{
        margin-top: 3rem;
        margin-bottom: 1rem;
        color: #fff;
        font-weight: 700;
        font-size: 1.25rem;
        line-height: 1.6;
      }}
      article h3 {{
        margin-top: 2rem;
        margin-bottom: 0.75rem;
        color: var(--soft);
        font-weight: 600;
        font-size: 1.1rem;
        line-height: 1.6;
      }}
      article p, article li, article blockquote {{
        font-size: 1.08rem;
        line-height: 1.75;
        color: var(--soft);
      }}
      article blockquote {{
        margin-left: 0;
        padding-left: 1rem;
        border-left: 4px solid var(--accent);
        color: var(--muted);
        font-style: italic;
      }}
      article pre {{
        margin: 1.5rem 0;
        padding: 1rem;
        background: #0b0b0b;
        border: 1px solid var(--line);
        border-radius: 0.5rem;
        overflow: auto;
      }}
      article code {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        background: rgba(255, 255, 255, 0.04);
        padding: 0.1rem 0.35rem;
        border-radius: 0.25rem;
        color: var(--ink);
      }}
      article pre code {{
        background: transparent;
        padding: 0;
        border-radius: 0;
      }}
    </style>
{analytics_snippet}  </head>
  <body>
    <div class="site-frame">
      <nav class="site-nav">
{navigation_markup}
      </nav>
      <main>
      <div class="eyebrow">{html.escape(eyebrow)}</div>
      <h1>{html.escape(heading)}</h1>
      <p class="summary">{html.escape(summary)}</p>
      <p class="meta">{html.escape(metadata)}</p>
      <article>
{body_html}
      </article>
      </main>
      <footer>{html.escape(_render_footer_text(footer_attribution))}</footer>
    </div>
  </body>
</html>
"""


def _render_open_graph_metadata(
    *,
    site_title: str,
    title: str,
    description: str,
    canonical_url: str,
    social_preview_url: str,
) -> str:
    metadata = {
        "og:title": title,
        "og:description": description,
        "og:type": "website",
        "og:url": canonical_url,
        "og:site_name": site_title,
        "og:image": social_preview_url,
    }
    return "\n".join(
        f'    <meta property="{html.escape(property_name)}" content="{html.escape(value)}" />'
        for property_name, value in metadata.items()
    )


def _render_twitter_card_metadata(
    *,
    title: str,
    description: str,
    canonical_url: str,
    social_preview_url: str,
) -> str:
    metadata = {
        "twitter:card": "summary",
        "twitter:title": title,
        "twitter:description": description,
        "twitter:url": canonical_url,
        "twitter:image": social_preview_url,
    }
    return "\n".join(
        f'    <meta name="{html.escape(property_name)}" content="{html.escape(value)}" />'
        for property_name, value in metadata.items()
    )


def _project_website_structured_data(
    *,
    site_title: str,
    site_description: str,
    base_url: str,
) -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site_title,
        "description": site_description,
        "url": _absolute_url(base_url, "/"),
        "potentialAction": {
            "@type": "SearchAction",
            "target": _absolute_url(base_url, "/search/?q={search_term_string}"),
            "query-input": "required name=search_term_string",
        },
    }


def _project_article_structured_data(
    *,
    title: str,
    description: str,
    canonical_url: str,
    publication_date: str,
    author_name: str,
    publisher_name: str,
    publisher_url: str,
) -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "datePublished": publication_date,
        "url": canonical_url,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url,
        },
        "author": {
            "@type": "Person",
            "name": author_name,
        },
        "publisher": {
            "@type": "Organization",
            "name": publisher_name,
            "url": publisher_url,
        },
    }


def _project_webpage_structured_data(
    *,
    title: str,
    description: str,
    canonical_url: str,
) -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": canonical_url,
    }


def _render_structured_data_script(
    payload: Mapping[str, object] | None,
) -> str:
    if payload is None:
        return ""
    serialized_payload = json.dumps(
        dict(payload),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    return (
        '    <script type="application/ld+json">'
        f"{serialized_payload}"
        "</script>"
    )


def _render_discovery_surface(
    base_url: str,
    destinations: tuple[tuple[str, str], ...],
    *,
    section_class: str | None = None,
) -> str:
    items = "\n".join(
        (
            "            <li>\n"
            f'              <a class="discovery-label" href="{_site_path(base_url, path)}">{html.escape(label)}</a>\n'
            f'              <small class="discovery-path">{html.escape(path)}</small>\n'
            "            </li>"
        )
        for label, path in destinations
    )
    section_class_markup = (
        f' class="{section_class}"' if section_class is not None else ""
    )
    return (
        f"        <section{section_class_markup}>\n"
        "          <h2>Other ways in</h2>\n"
        "          <ul class=\"discovery-list\">\n"
        f"{items}\n"
        "          </ul>\n"
        "        </section>"
    )


def _render_studio_discovery_surface(
    base_url: str,
    destinations: tuple[tuple[str, str], ...],
) -> str:
    items = "\n".join(
        (
            "            <li>\n"
            '              <div class="studio-discovery-row">\n'
            f'                <a class="studio-discovery-label" href="{_site_path(base_url, path)}">{html.escape(label)}</a>\n'
            f'                <small class="studio-discovery-path">{html.escape(path)}</small>\n'
            "              </div>\n"
            "            </li>"
        )
        for label, path in destinations
    )
    return (
        "        <section>\n"
        "          <h2>In the studio</h2>\n"
        "          <ul class=\"studio-discovery-list\">\n"
        f"{items}\n"
        "          </ul>\n"
        "        </section>"
    )


def _render_identity_asset_links(*, base_url: str) -> str:
    markup_lines: list[str] = []
    for rel, path, sizes in IDENTITY_ASSET_LINKS:
        attributes = [f'rel="{rel}"']
        if path.endswith(".png"):
            attributes.append('type="image/png"')
        if sizes is not None:
            attributes.append(f'sizes="{sizes}"')
        attributes.append(f'href="{html.escape(_site_path(base_url, path))}"')
        markup_lines.append(f"    <link {' '.join(attributes)} />")

    return "\n".join(markup_lines)


def _serialize_search_entry(entry: SearchEntry) -> dict[str, object]:
    record: dict[str, object] = {
        "title": entry.title,
        "url": entry.url,
        "type": entry.type,
    }
    if entry.summary:
        record["summary"] = entry.summary
    if entry.tags:
        record["tags"] = list(entry.tags)
    if entry.context:
        record["context"] = entry.context
    if entry.date:
        record["date"] = entry.date
    return record


def _render_recent_item(item: RecentContent, *, base_url: str) -> str:
    context = ""
    if item.saga_title:
        context = f" · {item.saga_title}"
        if item.arc_title:
            context += f" / {item.arc_title}"

    return (
        "          <li>\n"
        f'            <a class="homepage-link" href="{_site_path(base_url, item.permalink)}">[{html.escape(item.kind)}] '
        f"{html.escape(item.title)}</a>\n"
        f'            <small class="homepage-meta">{html.escape(item.date)}{html.escape(context)}</small>\n'
        f'            <p class="homepage-summary">{html.escape(item.summary)}</p>\n'
        "          </li>"
    )


def _render_archive_entry(entry: ArchiveEntry, *, base_url: str) -> str:
    context = ""
    if entry.saga_title:
        context = f" · {entry.saga_title}"
        if entry.arc_title:
            context += f" / {entry.arc_title}"

    return (
        "          <li>\n"
        '            <div class="archive-entry-row">\n'
                f'              <a class="archive-entry-link" href="{_site_path(base_url, entry.permalink)}">[{html.escape(entry.kind)}] '
        f"{html.escape(entry.title)}</a>\n"
        f'              <small class="archive-entry-meta">{html.escape(entry.date)}{html.escape(context)}</small>\n'
        "            </div>\n"
        f'            <p class="archive-entry-summary">{html.escape(entry.summary)}</p>\n'
        "          </li>"
    )


def _render_entry_metadata(metadata: EntryMetadata, *, base_url: str) -> str:
    parts = [
        html.escape(metadata.publication_date),
        f"{metadata.reading_time_minutes} min read",
    ]
    tags_markup = ""
    if metadata.tags:
        tag_links = "".join(
            f'<a class="entry-tag-chip" href="{_site_path(base_url, tag.permalink)}">#{html.escape(tag.name)}</a>'
            for tag in metadata.tags
        )
        tags_markup = f' · <span class="entry-tags">{tag_links}</span>'
    return (
        f'        <div class="entry-meta">{" · ".join(parts)}{tags_markup}</div>'
    )


def _render_feed_item(entry: FeedEntry, *, base_url: str) -> str:
    absolute_url = _absolute_url(base_url, entry.permalink)
    return (
        "    <item>\n"
        f"      <title>{html.escape(entry.title)}</title>\n"
        f"      <link>{html.escape(absolute_url)}</link>\n"
        f"      <guid>{html.escape(absolute_url)}</guid>\n"
        f"      <pubDate>{html.escape(_format_rfc2822(entry.date))}</pubDate>\n"
        f"      <description>{html.escape(entry.summary)}</description>\n"
        "    </item>"
    )


def _render_sitemap_entry(entry: SitemapEntry, *, base_url: str) -> str:
    lastmod_markup = ""
    if entry.last_modified:
        lastmod_markup = f"\n    <lastmod>{html.escape(entry.last_modified)}</lastmod>"
    return (
        "  <url>\n"
        f"    <loc>{html.escape(_absolute_url(base_url, entry.permalink))}</loc>"
        f"{lastmod_markup}\n"
        "  </url>"
    )


def _render_homepage_saga_summary(
    summary: HomepageSagaSummary,
    *,
    base_url: str,
) -> str:
    status_parts = [
        f"{summary.episode_count} episodes",
        summary.status,
    ]
    if summary.last_release_date:
        status_parts.insert(1, f"last release {summary.last_release_date}")

    return (
        "          <li>\n"
        f'            <a class="homepage-link" href="{_site_path(base_url, summary.permalink)}">{html.escape(summary.title)}</a>\n'
        f'            <small class="homepage-saga-status">— {html.escape("; ".join(status_parts))}</small>\n'
        "          </li>"
    )


def _format_rfc2822(date: str | None) -> str:
    if date is None:
        return format_datetime(datetime(1970, 1, 1, tzinfo=timezone.utc))
    parsed = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return format_datetime(parsed)


def _render_arc_summary(arc: object, *, base_url: str) -> str:
    last_release = arc.last_release_date or "n/a"
    return (
        "            <li>\n"
        '              <div class="saga-arc-row">\n'
        f'              <a class="saga-arc-link" href="{_site_path(base_url, arc.permalink)}">{html.escape(arc.title)}</a>\n'
        f'              <small class="saga-arc-meta">{arc.episode_count} episodes · last {html.escape(last_release)}</small>\n'
        "              </div>\n"
        "            </li>"
    )


def _render_timeline_entry(entry: object, *, base_url: str) -> str:
    return (
        "            <li>\n"
        '              <div class="saga-timeline-row">\n'
        f'                <a class="saga-timeline-link" href="{_site_path(base_url, entry.permalink)}">[Ep {entry.number:02d}] {html.escape(entry.title)}</a>\n'
        f'                <small class="saga-timeline-meta">{html.escape(entry.arc_title)} · {html.escape(entry.date)}</small>\n'
        "              </div>\n"
        "            </li>"
    )


def _render_arc_episode(episode: Episode, *, base_url: str) -> str:
    return (
        "            <li>\n"
        '              <div class="arc-episode-row">\n'
        f'                <a class="arc-episode-link" href="{_site_path(base_url, episode.permalink)}">[Ep {episode.number:02d}] {html.escape(episode.title)}</a>\n'
        f'                <small class="arc-episode-meta">{html.escape(episode.date)}</small>\n'
        "              </div>\n"
        "            </li>"
    )


def _render_adjacent_navigation(
    *,
    previous_episode: object,
    next_episode: object,
    base_url: str,
) -> str:
    previous_markup = '<span class="adjacent-nav-spacer"></span>'
    next_markup = '<span class="adjacent-nav-spacer"></span>'

    if previous_episode is not None:
        previous_markup = (
            f'<a class="adjacent-nav-link previous" href="{_site_path(base_url, previous_episode.permalink)}">'
            f"&larr; Ep {previous_episode.number:02d} {html.escape(previous_episode.title)}</a>"
        )

    if next_episode is not None:
        next_markup = (
            f'<a class="adjacent-nav-link next" href="{_site_path(base_url, next_episode.permalink)}">'
            f"Ep {next_episode.number:02d} {html.escape(next_episode.title)} &rarr;</a>"
        )

    return f'        <nav class="nav-grid episode-adjacent-nav">{previous_markup}{next_markup}</nav>'


def _render_library_tag(tag: str, *, base_url: str) -> str:
    return (
        "            <li>\n"
        f'              <a class="topic-link" href="{_site_path(base_url, f"/library/{tag}/")}">#{html.escape(tag)}</a>\n'
        "            </li>"
    )


def _render_topic_entry(entry: TopicEntry, *, base_url: str) -> str:
    context = ""
    if entry.saga_title:
        context = f"{entry.saga_title}"
        if entry.arc_title:
            context += f" / {entry.arc_title}"
    context_markup = f" · {html.escape(context)}" if context else ""
    return (
        "            <li>\n"
        f'              <a class="topic-entry-link" href="{_site_path(base_url, entry.permalink)}">[{html.escape(entry.kind)}] {html.escape(entry.title)}</a>\n'
        f'              <small class="topic-entry-meta">{html.escape(entry.date)}{context_markup}</small>\n'
        f'              <p class="topic-entry-summary">{html.escape(entry.summary)}</p>\n'
        "            </li>"
    )


def _render_legacy_topic_entry(entry: TopicEntry, *, base_url: str) -> str:
    context = ""
    if entry.saga_title:
        context = f"{entry.saga_title}"
        if entry.arc_title:
            context += f" / {entry.arc_title}"
    context_markup = (
        f'\n                    <div class="text-xs text-zinc-500">{html.escape(context)} —</div>'
        if context
        else ""
    )
    return (
        '            <li class="border border-zinc-800 rounded p-3 hover:border-white/30 transition-colors">\n'
        '                <div class="flex flex-col gap-1">\n'
        f'                    <div class="text-xs text-zinc-500">{html.escape(entry.date)}</div>\n'
        f'                    <a class="text-white hover:underline" href="{_site_path(base_url, entry.permalink)}">{html.escape(entry.title)}</a>'
        f'{context_markup}\n'
        f'                    <p class="text-sm text-zinc-400">{html.escape(entry.summary)}</p>\n'
        "                </div>\n"
        "            </li>"
    )


def _render_saga_summary(summary: object, *, base_url: str) -> str:
    start_link = ""
    if summary.start_permalink:
        start_link = (
            f'<small class="saga-index-start"><a href="{_site_path(base_url, summary.start_permalink)}">start reading</a></small>'
        )
    return (
        "            <li>\n"
        '              <div class="saga-index-row">\n'
        f'                <a class="saga-index-link" href="{_site_path(base_url, summary.permalink)}">{html.escape(summary.title)}</a>{start_link}\n'
        "              </div>\n"
        f'              <div class="text-sm text-zinc-400 leading-relaxed mb-4 space-y-2">\n{_render_markdown(summary.summary)}\n              </div>\n'
        "            </li>"
    )


def _render_navigation(
    links: tuple[NavigationLink, ...],
    *,
    base_url: str,
) -> str:
    navigation_links: list[str] = []
    for index, link in enumerate(links):
        aria_current = ' aria-current="page"' if link.is_active else ""
        active_class = " active" if link.is_active else ""
        navigation_links.append(
            "        "
            f'<a href="{_site_path(base_url, link.path)}"'
            f' class="site-nav-link{active_class}"{aria_current}>'
            f"{html.escape(link.label.upper())}</a>"
        )
        if index < len(links) - 1:
            navigation_links.append(
                '        <span class="site-nav-separator" aria-hidden="true">/</span>'
            )
    navigation_links.append(
        "        " f'<a href="{_site_path(base_url, "/feed.xml")}">RSS</a>'
    )
    return "\n".join(navigation_links)


def _render_footer_text(footer_attribution: FooterAttribution) -> str:
    return (
        f"(c) {footer_attribution.year} {footer_attribution.site_name} "
        f"- {footer_attribution.tagline}"
    )


def _absolute_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + path


def _site_path(base_url: str, path: str) -> str:
    base_path = urlparse(base_url).path.rstrip("/")
    if not base_path:
        return path
    if path == "/":
        return base_path + "/"
    return base_path + path


def _site_host(base_url: str) -> str:
    parsed = urlparse(base_url)
    if parsed.hostname is None:
        raise ValueError(f"base_url must include a hostname: {base_url!r}")
    return parsed.hostname


def _render_markdown(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    in_blockquote = False
    blockquote_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(part.strip() for part in paragraph)
            output.append(f"        <p>{_render_inline(text)}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            output.append("        <ul>")
            output.extend(f"          <li>{item}</li>" for item in list_items)
            output.append("        </ul>")
            list_items = []

    def flush_blockquote() -> None:
        nonlocal blockquote_lines, in_blockquote
        if blockquote_lines:
            text = " ".join(line.strip() for line in blockquote_lines)
            output.append(f"        <blockquote>{_render_inline(text)}</blockquote>")
            blockquote_lines = []
        in_blockquote = False

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            flush_list()
            flush_blockquote()
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            flush_list()
            flush_blockquote()
            output.append(f"        <h3>{_render_inline(stripped[4:])}</h3>")
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            flush_list()
            flush_blockquote()
            output.append(f"        <h2>{_render_inline(stripped[3:])}</h2>")
            continue

        if stripped.startswith("> "):
            flush_paragraph()
            flush_list()
            in_blockquote = True
            blockquote_lines.append(stripped[2:])
            continue

        if in_blockquote:
            flush_blockquote()

        if stripped.startswith("- "):
            flush_paragraph()
            list_items.append(_render_inline(stripped[2:]))
            continue

        flush_list()
        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    flush_blockquote()
    return "\n".join(output)


def _render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*)\)",
        r'<a href="\2">\1</a>',
        escaped,
    )
    return escaped


def _render_analytics(config: AnalyticsConfig | None) -> str:
    if config is None:
        return ""

    attributes = [
        "defer",
        f'data-domain="{config.domain}"',
    ]

    if config.api_host:
        api_host = config.api_host.rstrip("/")
        attributes.append(f'data-api="{api_host}/api/event"')

    return (
        f'    <script {" ".join(attributes)} src="{config.script_url}"></script>\n'
    )
