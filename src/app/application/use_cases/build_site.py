from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from email.utils import format_datetime
import html
import json
import re
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

IDENTITY_ASSET_LINKS: tuple[tuple[str, str, str | None], ...] = (
    ("icon", "/favicon.ico", None),
    ("icon", "/favicon-16x16.png", "16x16"),
    ("icon", "/favicon-32x32.png", "32x32"),
    ("apple-touch-icon", "/apple-touch-icon.png", None),
)
THEME_COLOR = "#0b0b0b"
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
        "index.html": build_homepage(config, homepage_surface, footer_attribution),
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
        f"    <title>{html.escape(config.title)}</title>\n"
        f"    <link>{html.escape(_absolute_url(config.base_url, '/'))}</link>\n"
        f"    <description>{html.escape(config.description)}</description>\n"
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
        "start_url": _absolute_url(config.base_url, "/"),
        "display": "standalone",
        "theme_color": THEME_COLOR,
        "background_color": BACKGROUND_COLOR,
        "icons": [
            {
                "src": _absolute_url(config.base_url, "/favicon-16x16.png"),
                "sizes": "16x16",
                "type": "image/png",
            },
            {
                "src": _absolute_url(config.base_url, "/favicon-32x32.png"),
                "sizes": "32x32",
                "type": "image/png",
            },
            {
                "src": _absolute_url(config.base_url, "/apple-touch-icon.png"),
                "sizes": "180x180",
                "type": "image/png",
            },
        ],
    }
    return json.dumps(manifest, ensure_ascii=True, indent=2) + "\n"


def build_browserconfig(config: SiteConfig) -> str:
    square_logo_url = _absolute_url(config.base_url, "/apple-touch-icon.png")
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
    homepage_surface: HomepageSurface,
    footer_attribution: FooterAttribution,
) -> str:
    recent_items = homepage_surface.recent_entries
    recent_markup = "\n".join(
        _render_recent_item(item, base_url=config.base_url) for item in recent_items
    )
    saga_markup = "\n".join(
        _render_homepage_saga_summary(summary, base_url=config.base_url)
        for summary in homepage_surface.saga_summaries
    )
    recent_metadata = (
        f"{len(recent_items)} recent entries shown"
        if recent_items
        else "no recent entries yet"
    )

    return _render_document(
        config=config,
        title=config.title,
        description=config.description,
        canonical_path="/",
        eyebrow="Home",
        heading=config.title,
        summary="Architecture, focus, and growth in public.",
        metadata=recent_metadata,
        footer_attribution=footer_attribution,
        structured_data_payload=_project_website_structured_data(
            site_title=config.title,
            site_description=config.description,
            base_url=config.base_url,
        ),
        body_html=(
            "        <section class=\"homepage-discovery-shell\">\n"
            "          <p class=\"homepage-intro\">Experiments in architecture, focus, and growth, built in public one saga at a time.</p>\n"
            f'          <p class="homepage-paths"><a href="{_absolute_url(config.base_url, "/search/")}">Search</a> / <a href="{_absolute_url(config.base_url, "/archives/")}">Archives</a> / <a href="{_absolute_url(config.base_url, "/library/")}">Library</a></p>\n'
            "        </section>\n"
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
            f'          <a href="{_absolute_url(config.base_url, "/sagas/")}">Browse all sagas</a>\n'
            "        </section>\n"
            "        <section>\n"
            "          <h2 class=\"section-label\">LIBRARY</h2>\n"
            "          <p>Browse ideas and implementation threads by topic.</p>\n"
            f'          <a href="{_absolute_url(config.base_url, "/library/")}">Explore the library</a>\n'
            "        </section>"
        ),
    )


def build_not_found_page(
    config: SiteConfig,
    footer_attribution: FooterAttribution,
) -> str:
    recovery_rows = "\n".join(
        (
            "            <li>\n"
            '              <div class="not-found-row">\n'
            f'                <a class="not-found-link" href="{_absolute_url(config.base_url, path)}">{html.escape(label)}</a>\n'
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
                    section_class="archives-discovery-shell",
                ),
            ]
        ),
    )


def build_search_page(
    config: SiteConfig,
    footer_attribution: FooterAttribution,
) -> str:
    search_index_url = _absolute_url(config.base_url, "/search.json")
    search_action_url = _absolute_url(config.base_url, "/search/")
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
            "        <section class=\"search-page-shell\">\n"
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
            f'                <a class="search-noscript-recovery-link" href="{_absolute_url(config.base_url, "/archives/")}">Browse the archives</a>\n'
            f'                <small class="search-noscript-recovery-path">/archives/</small>\n'
            "              </div>\n"
            "              <div class=\"search-noscript-recovery-row\">\n"
            f'                <a class="search-noscript-recovery-link" href="{_absolute_url(config.base_url, "/library/")}">Explore the library</a>\n'
            f'                <small class="search-noscript-recovery-path">/library/</small>\n'
            "              </div>\n"
            "            </div>\n"
            "          </noscript>\n"
            '          <p id="search-status" role="status" aria-live="polite" aria-atomic="true">Enter a query to search the publication.</p>\n'
            '          <h3 id="search-results-heading" class="visually-hidden">Search results</h3>\n'
            '          <ul id="search-results" class="search-result-list" aria-labelledby="search-results-heading"></ul>\n'
            "        </section>\n"
        f"{_render_discovery_surface(config.base_url, (('Browse the chronology', '/archives/'), ('Move by topic instead', '/library/')), section_class='search-discovery-shell')}\n"
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
            f"              searchRecovery.appendChild(createSearchRecoveryRow('the archives', {json.dumps(_absolute_url(config.base_url, '/archives/'))}));\n"
            f"              searchRecovery.appendChild(createSearchRecoveryRow('the library', {json.dumps(_absolute_url(config.base_url, '/library/'))}));\n"
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
            "              link.href = record.url;\n"
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
            f"              searchRecovery.appendChild(createSearchRecoveryRow('the archives', {json.dumps(_absolute_url(config.base_url, '/archives/'))}));\n"
            f"              searchRecovery.appendChild(createSearchRecoveryRow('the library', {json.dumps(_absolute_url(config.base_url, '/library/'))}));\n"
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
    entry_metadata = project_episode_metadata(episode)
    metadata = (
        f"{episode.date} · {episode.saga_title} / {episode.arc_title} · "
        f"Episode {episode.number}"
    )
    parent_navigation = (
        f'        <nav class="breadcrumbs episode-breadcrumbs"><a class="breadcrumb-link" href="{_absolute_url(config.base_url, "/sagas/" + episode.saga_slug + "/")}">'
        f"{html.escape(episode.saga_title)}</a> <span class=\"breadcrumb-separator\">/</span> "
        f'<a class="breadcrumb-link" href="{_absolute_url(config.base_url, "/sagas/" + episode.saga_slug + "/" + episode.arc_slug + "/")}">'
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


def build_saga_page(
    config: SiteConfig,
    saga_view: SagaView,
    footer_attribution: FooterAttribution,
) -> str:
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
    episode_markup = "\n".join(
        _render_arc_episode(episode, base_url=config.base_url)
        for episode in arc_view.episodes
    )
    breadcrumb = (
        f'        <nav class="breadcrumbs"><a class="breadcrumb-link" href="{_absolute_url(config.base_url, arc_view.arc.permalink[:-len(arc_view.arc.slug)-1])}">'
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


def build_library_page(
    config: SiteConfig,
    library_catalog: LibraryCatalog,
    section_page: SectionPage,
    footer_attribution: FooterAttribution,
) -> str:
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
        f"{_render_discovery_surface(config.base_url, (('Browse the chronology', '/archives/'), ('Search across the publication', '/search/')), section_class='library-discovery-shell')}"
        if library_catalog.tags
        else (
            "        <section>\n"
            f"{_render_markdown(section_page.body_markdown)}\n"
            "        </section>\n"
            "        <p>No tags available yet.</p>\n"
            f"{_render_discovery_surface(config.base_url, (('Browse the chronology', '/archives/'), ('Search across the publication', '/search/')), section_class='library-discovery-shell')}"
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
                f"<a class=\"breadcrumb-link\" href=\"{_absolute_url(config.base_url, '/library/')}\">Library</a></nav>",
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


def build_sagas_index_page(
    config: SiteConfig,
    sagas_index: SagasIndex,
    footer_attribution: FooterAttribution,
) -> str:
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
    feed_url = _absolute_url(config.base_url, "/feed.xml")
    manifest_url = _absolute_url(config.base_url, "/site.webmanifest")
    browserconfig_url = _absolute_url(config.base_url, "/browserconfig.xml")
    opensearch_url = _absolute_url(config.base_url, "/opensearch.xml")
    social_preview_url = _absolute_url(config.base_url, "/social-preview.png")
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
        --bg: #000000;
        --surface: #0b0b0b;
        --text-100: #f4f4f5;
        --text-200: #e4e4e7;
        --text-300: #d4d4d8;
        --text-400: #a1a1aa;
        --line: #27272a;
        --line-strong: #3f3f46;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        min-height: 100vh;
        font-family: ui-monospace, "SFMono-Regular", Menlo, Monaco, Consolas,
          "Liberation Mono", "Courier New", monospace;
        color: var(--text-200);
        background:
          radial-gradient(circle at top, rgba(255, 255, 255, 0.045), transparent 42%),
          radial-gradient(circle at bottom right, rgba(255, 255, 255, 0.018), transparent 32%),
          linear-gradient(180deg, #050505 0%, var(--bg) 72%);
      }}
      main {{
        width: min(46rem, calc(100vw - 3rem));
        margin: 0 auto;
        padding: 3.5rem 0 5rem;
      }}
      a {{
        color: var(--text-400);
        text-decoration: none;
        transition: color 0.15s ease;
      }}
      a:hover {{
        color: #ffffff;
        text-decoration: underline;
      }}
      .eyebrow {{
        color: var(--text-400);
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}
      h1 {{
        margin: 1.25rem 0 0.75rem;
        font-size: clamp(2.2rem, 6vw, 4rem);
        line-height: 1.05;
        color: #ffffff;
      }}
      .meta, .summary {{
        color: var(--text-400);
      }}
      .homepage-intro {{
        margin: 0;
        color: var(--text-200);
        line-height: 1.7;
      }}
      .homepage-paths {{
        margin-top: 0.85rem;
        color: var(--text-400);
        font-size: 0.8rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
      }}
      .homepage-discovery-shell {{
        display: grid;
        gap: 0.75rem;
      }}
      .homepage-paths a {{
        color: var(--text-400);
      }}
      .section-label {{
        margin: 0 0 0.75rem;
        color: var(--text-400);
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
        margin-top: 1rem;
      }}
      .homepage-recent-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.45rem;
      }}
      .homepage-link {{
        color: var(--text-100);
      }}
      .homepage-meta {{
        display: block;
        margin-top: 0;
        color: var(--text-400);
        font-size: 0.8rem;
      }}
      .homepage-summary {{
        margin: 0.35rem 0 0;
        color: var(--text-400);
        font-size: 0.92rem;
        line-height: 1.6;
      }}
      .homepage-saga-row {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.45rem;
      }}
      .homepage-saga-status {{
        color: var(--text-400);
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
        color: var(--text-100);
        text-decoration: none;
        transition: color 0.15s ease, border-color 0.15s ease;
      }}
      .topic-link:hover {{
        color: #ffffff;
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
        color: var(--text-100);
      }}
      .topic-entry-meta {{
        display: block;
        margin-top: 0.2rem;
        color: var(--text-400);
        font-size: 0.8rem;
      }}
      .topic-entry-summary {{
        margin: 0.35rem 0 0;
        color: var(--text-400);
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
        color: var(--text-100);
      }}
      .saga-index-summary {{
        margin: 0.35rem 0 0;
        color: var(--text-400);
        font-size: 0.92rem;
        line-height: 1.6;
      }}
      .saga-index-start {{
        color: var(--text-400);
        font-size: 0.8rem;
        letter-spacing: 0.04em;
        text-transform: lowercase;
      }}
      .saga-index-start a {{
        color: var(--text-400);
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
        color: var(--text-100);
      }}
      .saga-arc-meta {{
        display: block;
        margin-top: 0;
        color: var(--text-400);
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
        color: var(--text-100);
      }}
      .saga-timeline-meta {{
        display: block;
        margin-top: 0;
        color: var(--text-400);
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
        color: var(--text-100);
      }}
      .arc-episode-meta {{
        display: block;
        margin-top: 0;
        color: var(--text-400);
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
        color: var(--text-100);
      }}
      .archive-entry-meta {{
        display: block;
        margin-top: 0;
        color: var(--text-400);
        font-size: 0.8rem;
      }}
      .archive-entry-summary {{
        margin: 0.35rem 0 0;
        color: var(--text-400);
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
        color: var(--text-400);
      }}
      .search-load-recovery-message {{
        margin: 0 0 0.75rem;
        color: var(--text-400);
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
        color: var(--text-100);
      }}
      .search-empty-recovery-path {{
        display: block;
        margin-top: 0;
        color: var(--text-400);
        font-size: 0.8rem;
      }}
      .search-noscript-recovery {{
        margin: 0.75rem 0 0;
      }}
      .search-noscript-recovery-message {{
        margin: 0 0 0.75rem;
        color: var(--text-400);
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
        color: var(--text-100);
      }}
      .search-noscript-recovery-path {{
        display: block;
        margin-top: 0;
        color: var(--text-400);
        font-size: 0.8rem;
      }}
      .search-query-label {{
        display: block;
        margin-bottom: 0.35rem;
      }}
      .search-page-shell {{
        display: grid;
        gap: 1rem;
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
        padding: 1rem 1.05rem;
        border: 1px solid var(--line);
        border-radius: 0.7rem;
        background: rgba(255, 255, 255, 0.015);
      }}
      .search-result-header {{
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: 0.55rem;
      }}
      .search-result-link {{
        display: block;
        color: var(--text-100);
      }}
      .search-result-meta {{
        display: block;
        margin-top: 0;
        color: var(--text-400);
        font-size: 0.8rem;
      }}
      .search-result-summary {{
        margin: 0.35rem 0 0;
        color: var(--text-400);
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
        display: inline-block;
        padding: 0.1rem 0.55rem;
        border: 1px solid var(--line-strong);
        border-radius: 999px;
        color: var(--text-400);
        font-size: 0.8rem;
        letter-spacing: 0.04em;
        text-transform: lowercase;
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
        color: var(--text-100);
      }}
      .not-found-path {{
        display: block;
        margin-top: 0;
        color: var(--text-400);
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
        color: var(--text-100);
      }}
      .discovery-path {{
        display: block;
        margin-top: 0.15rem;
        color: var(--text-400);
        font-size: 0.8rem;
      }}
      .library-discovery-shell {{
        display: grid;
        gap: 0.75rem;
      }}
      .search-discovery-shell {{
        display: grid;
        gap: 0.75rem;
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
        color: var(--text-100);
      }}
      .studio-discovery-path {{
        display: block;
        margin-top: 0;
        color: var(--text-400);
        font-size: 0.8rem;
      }}
      .site-frame {{
        width: min(64rem, calc(100vw - 3rem));
        margin: 0 auto;
        padding: 1.5rem 0 5rem;
      }}
      .site-nav {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.9rem;
        margin-bottom: 2.25rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--line);
      }}
      .site-nav-link {{
        color: var(--text-400);
      }}
      .site-nav-link.active {{
        color: #ffffff;
        font-weight: 500;
      }}
      .site-nav-link.active::after {{
        content: "•";
        margin-left: 0.4em;
        opacity: 0.6;
        font-weight: 400;
      }}
      .breadcrumbs {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.4rem;
        margin-bottom: 1rem;
        color: var(--text-400);
      }}
      .episode-breadcrumbs {{
        margin-bottom: 1rem;
      }}
      .breadcrumb-link {{
        color: var(--text-400);
      }}
      .breadcrumb-separator {{
        color: var(--text-400);
      }}
      .entry-meta {{
        margin-bottom: 1.5rem;
        color: var(--text-400);
        font-size: 0.95rem;
        line-height: 1.8;
      }}
      .entry-meta a {{
        color: var(--text-400);
      }}
      .entry-tags {{
        display: inline-flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        vertical-align: middle;
      }}
      .entry-tag-chip {{
        display: inline-block;
        padding: 0.1rem 0.55rem;
        border: 1px solid var(--line-strong);
        border-radius: 999px;
        font-size: 0.82rem;
        letter-spacing: 0.04em;
        text-transform: lowercase;
      }}
      .entry-tag-chip:hover {{
        border-color: var(--text-300);
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
        color: var(--text-100);
      }}
      .episode-adjacent-nav {{
        margin-top: 2rem;
      }}
      .episode-adjacent-nav a {{
        color: var(--text-100);
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
        color: var(--text-400);
        font-size: 0.85rem;
      }}
      article h2 {{
        margin-top: 3rem;
        margin-bottom: 1rem;
        color: #ffffff;
        font-weight: 600;
        font-size: 1.25rem;
        line-height: 1.6;
      }}
      article h3 {{
        margin-top: 2rem;
        margin-bottom: 0.75rem;
        color: var(--text-200);
        font-weight: 500;
        font-size: 1.1rem;
        line-height: 1.6;
      }}
      article p, article li, article blockquote {{
        font-size: 1rem;
        line-height: 1.7;
        color: var(--text-200);
      }}
      article blockquote {{
        margin-left: 0;
        padding-left: 1rem;
        border-left: 2px solid var(--line-strong);
        color: var(--text-300);
        font-style: italic;
      }}
      article pre {{
        margin: 1.5rem 0;
        padding: 1rem;
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 0.5rem;
        overflow: auto;
      }}
      article code {{
        font-family: ui-monospace, "SFMono-Regular", Menlo, Monaco, Consolas,
          "Liberation Mono", "Courier New", monospace;
        background: rgba(255, 255, 255, 0.04);
        padding: 0.1rem 0.35rem;
        border-radius: 0.25rem;
        color: var(--text-100);
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
            f'              <a class="discovery-label" href="{_absolute_url(base_url, path)}">{html.escape(label)}</a>\n'
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
            f'                <a class="studio-discovery-label" href="{_absolute_url(base_url, path)}">{html.escape(label)}</a>\n'
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
        attributes.append(f'href="{html.escape(_absolute_url(base_url, path))}"')
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
        '            <div class="homepage-recent-row">\n'
        f'              <a class="homepage-link" href="{_absolute_url(base_url, item.permalink)}">[{html.escape(item.kind)}] '
        f"{html.escape(item.title)}</a>\n"
        f'              <small class="homepage-meta">{html.escape(item.date)}{html.escape(context)}</small>\n'
        "            </div>\n"
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
        f'              <a class="archive-entry-link" href="{_absolute_url(base_url, entry.permalink)}">[{html.escape(entry.kind)}] '
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
            f'<a class="entry-tag-chip" href="{_absolute_url(base_url, tag.permalink)}">#{html.escape(tag.name)}</a>'
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
        '            <div class="homepage-saga-row">\n'
        f'              <a class="homepage-link" href="{_absolute_url(base_url, summary.permalink)}">{html.escape(summary.title)}</a>\n'
        f'              <small class="homepage-saga-status">{html.escape(" - ".join(status_parts))}</small>\n'
        "            </div>\n"
        f'            <p class="homepage-summary">{html.escape(summary.summary)}</p>\n'
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
        f'              <a class="saga-arc-link" href="{_absolute_url(base_url, arc.permalink)}">{html.escape(arc.title)}</a>\n'
        f'              <small class="saga-arc-meta">{arc.episode_count} episodes · last {html.escape(last_release)}</small>\n'
        "              </div>\n"
        "            </li>"
    )


def _render_timeline_entry(entry: object, *, base_url: str) -> str:
    return (
        "            <li>\n"
        '              <div class="saga-timeline-row">\n'
        f'                <a class="saga-timeline-link" href="{_absolute_url(base_url, entry.permalink)}">[Ep {entry.number:02d}] {html.escape(entry.title)}</a>\n'
        f'                <small class="saga-timeline-meta">{html.escape(entry.arc_title)} · {html.escape(entry.date)}</small>\n'
        "              </div>\n"
        "            </li>"
    )


def _render_arc_episode(episode: Episode, *, base_url: str) -> str:
    return (
        "            <li>\n"
        '              <div class="arc-episode-row">\n'
        f'                <a class="arc-episode-link" href="{_absolute_url(base_url, episode.permalink)}">[Ep {episode.number:02d}] {html.escape(episode.title)}</a>\n'
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
            f'<a class="adjacent-nav-link previous" href="{_absolute_url(base_url, previous_episode.permalink)}">'
            f"&larr; Ep {previous_episode.number:02d} {html.escape(previous_episode.title)}</a>"
        )

    if next_episode is not None:
        next_markup = (
            f'<a class="adjacent-nav-link next" href="{_absolute_url(base_url, next_episode.permalink)}">'
            f"Ep {next_episode.number:02d} {html.escape(next_episode.title)} &rarr;</a>"
        )

    return f'        <nav class="nav-grid episode-adjacent-nav">{previous_markup}{next_markup}</nav>'


def _render_library_tag(tag: str, *, base_url: str) -> str:
    return (
        "            <li>\n"
        f'              <a class="topic-link" href="{_absolute_url(base_url, f"/library/{tag}/")}">#{html.escape(tag)}</a>\n'
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
        f'              <a class="topic-entry-link" href="{_absolute_url(base_url, entry.permalink)}">[{html.escape(entry.kind)}] {html.escape(entry.title)}</a>\n'
        f'              <small class="topic-entry-meta">{html.escape(entry.date)}{context_markup}</small>\n'
        f'              <p class="topic-entry-summary">{html.escape(entry.summary)}</p>\n'
        "            </li>"
    )


def _render_saga_summary(summary: object, *, base_url: str) -> str:
    start_link = ""
    if summary.start_permalink:
        start_link = (
            f'<small class="saga-index-start"><a href="{_absolute_url(base_url, summary.start_permalink)}">start reading</a></small>'
        )
    return (
        "            <li>\n"
        '              <div class="saga-index-row">\n'
        f'                <a class="saga-index-link" href="{_absolute_url(base_url, summary.permalink)}">{html.escape(summary.title)}</a>{start_link}\n'
        "              </div>\n"
        f'              <p class="saga-index-summary">{html.escape(summary.summary)}</p>\n'
        "            </li>"
    )


def _render_navigation(
    links: tuple[NavigationLink, ...],
    *,
    base_url: str,
) -> str:
    navigation_links: list[str] = []
    for link in links:
        aria_current = ' aria-current="page"' if link.is_active else ""
        active_class = " active" if link.is_active else ""
        navigation_links.append(
            "        "
            f'<a href="{_absolute_url(base_url, link.path)}"'
            f' class="site-nav-link{active_class}"{aria_current}>'
            f"{html.escape(link.label)}</a>"
        )
    navigation_links.append(
        "        " f'<a href="{_absolute_url(base_url, "/feed.xml")}">RSS</a>'
    )
    return "\n".join(navigation_links)


def _render_footer_text(footer_attribution: FooterAttribution) -> str:
    return (
        f"(c) {footer_attribution.year} {footer_attribution.site_name} "
        f"- {footer_attribution.tagline}"
    )


def _absolute_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + path


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
