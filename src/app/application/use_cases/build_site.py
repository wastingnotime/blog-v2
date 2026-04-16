from __future__ import annotations

import html
import re

from src.app.domain.models.content import (
    ArcView,
    ContentCatalog,
    Episode,
    LibraryCatalog,
    Page,
    RecentContent,
    Saga,
    SagaView,
    TopicEntry,
    TopicPage,
)
from src.app.domain.models.site_config import AnalyticsConfig, SiteConfig
from src.app.application.use_cases.project_narrative_navigation import (
    project_arc_views,
    project_saga_views,
)
from src.app.application.use_cases.project_topic_catalog import project_topic_catalog


def build_static_site(config: SiteConfig, catalog: ContentCatalog) -> dict[str, str]:
    arc_views = project_arc_views(catalog)
    saga_views = project_saga_views(catalog, arc_views)
    topic_catalog = project_topic_catalog(catalog)
    pages = {
        "index.html": build_homepage(config, catalog),
        "library/index.html": build_library_page(config, topic_catalog),
    }

    for page in catalog.pages:
        pages[f"{page.slug}/index.html"] = build_content_page(config, page)

    for saga in catalog.sagas:
        pages[f"sagas/{saga.slug}/index.html"] = build_saga_page(
            config,
            saga_views[saga.slug],
        )

    for arc in catalog.arcs:
        pages[f"sagas/{arc.saga_slug}/{arc.slug}/index.html"] = build_arc_page(
            config,
            arc_views[(arc.saga_slug, arc.slug)],
        )

    for episode in catalog.episodes:
        pages[episode.permalink.strip("/") + "/index.html"] = build_episode_page(
            config,
            episode,
            arc_views[(episode.saga_slug, episode.arc_slug)],
        )

    for topic_page in topic_catalog.pages:
        pages[f"library/{topic_page.tag}/index.html"] = build_topic_page(
            config,
            topic_page,
        )

    return pages


def build_homepage(config: SiteConfig, catalog: ContentCatalog) -> str:
    analytics_snippet = _render_analytics(config.analytics)
    recent_items = _build_recent_items(catalog)
    recent_markup = "\n".join(
        _render_recent_item(item, base_url=config.base_url) for item in recent_items
    )
    saga_markup = "\n".join(
        _render_saga_item(saga, base_url=config.base_url) for saga in catalog.sagas
    )

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{config.title}</title>
    <meta name="description" content="{config.description}" />
    <link rel="canonical" href="{config.base_url}" />
    <style>
      :root {{
        color-scheme: light;
        --ink: #111827;
        --muted: #4b5563;
        --line: #d1d5db;
        --paper: linear-gradient(180deg, #fffdf8 0%, #f3efe5 100%);
        --accent: #0f766e;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        min-height: 100vh;
        font-family: Georgia, "Times New Roman", serif;
        color: var(--ink);
        background: var(--paper);
      }}
      main {{
        width: min(56rem, calc(100vw - 3rem));
        margin: 0 auto;
        padding: 5rem 0 4rem;
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
        margin: 1.5rem 0 1rem;
        font-size: clamp(2.5rem, 7vw, 4.75rem);
        line-height: 0.95;
      }}
      p {{
        max-width: 42rem;
        color: var(--muted);
        font-size: 1.1rem;
        line-height: 1.7;
      }}
      .card {{
        margin-top: 2.5rem;
        padding: 1.25rem 1.5rem;
        border-left: 4px solid var(--accent);
        background: rgba(255, 255, 255, 0.72);
        box-shadow: 0 1rem 2rem rgba(17, 24, 39, 0.06);
      }}
      code {{
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
        font-size: 0.95em;
      }}
      ul {{
        list-style: none;
        padding: 0;
      }}
      li + li {{
        margin-top: 1.25rem;
      }}
      a {{
        color: var(--ink);
      }}
      small {{
        display: block;
        margin-top: 0.35rem;
        color: var(--muted);
      }}
    </style>
{analytics_snippet}  </head>
  <body>
    <main>
      <span class="eyebrow">blog-v2 content bootstrap</span>
      <h1>{config.title}</h1>
      <p>{config.description}</p>
      <section class="card">
        <strong>Deployment target:</strong> GitHub Pages static files.<br />
        <strong>API dependency:</strong> none on <code>/api</code>.<br />
        <strong>Base URL:</strong> <code>{config.base_url}</code>
      </section>
      <section>
        <h2>Recent</h2>
        <ul>
{recent_markup}
        </ul>
      </section>
      <section>
        <h2>Sagas</h2>
        <ul>
{saga_markup}
        </ul>
      </section>
      <section>
        <h2>Library</h2>
        <p>Browse ideas and implementation threads by topic.</p>
        <a href="{_absolute_url(config.base_url, '/library/')}">Explore the library</a>
      </section>
    </main>
  </body>
</html>
"""


def build_content_page(config: SiteConfig, page: Page) -> str:
    return _render_document(
        config=config,
        title=page.title,
        description=page.summary,
        canonical_path=page.permalink,
        eyebrow="Page",
        heading=page.title,
        summary=page.summary,
        metadata=page.date,
        body_html=_render_markdown(page.body_markdown),
    )


def build_episode_page(config: SiteConfig, episode: Episode, arc_view: ArcView) -> str:
    metadata = (
        f"{episode.date} · {episode.saga_title} / {episode.arc_title} · "
        f"Episode {episode.number}"
    )
    parent_navigation = (
        f'        <nav class="breadcrumbs"><a href="{_absolute_url(config.base_url, "/sagas/" + episode.saga_slug + "/")}">'
        f"{html.escape(episode.saga_title)}</a> / "
        f'<a href="{_absolute_url(config.base_url, "/sagas/" + episode.saga_slug + "/" + episode.arc_slug + "/")}">'
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
        body_html="\n".join(
            [parent_navigation, _render_markdown(episode.body_markdown), adjacent_navigation]
        ),
    )


def build_saga_page(config: SiteConfig, saga_view: SagaView) -> str:
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
        body_html=(
            "        <section>\n"
            "          <h2>Arcs</h2>\n"
            "          <ul>\n"
            f"{arc_markup}\n"
            "          </ul>\n"
            "        </section>\n"
            "        <section>\n"
            "          <h2>Timeline</h2>\n"
            "          <ul>\n"
            f"{timeline_markup}\n"
            "          </ul>\n"
            "        </section>"
        ),
    )


def build_arc_page(config: SiteConfig, arc_view: ArcView) -> str:
    episode_markup = "\n".join(
        _render_arc_episode(episode, base_url=config.base_url)
        for episode in arc_view.episodes
    )
    breadcrumb = (
        f'        <nav class="breadcrumbs"><a href="{_absolute_url(config.base_url, arc_view.arc.permalink[:-len(arc_view.arc.slug)-1])}">'
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
        body_html=(
            f"{breadcrumb}\n"
            "        <section>\n"
            "          <h2>Episodes</h2>\n"
            "          <ul>\n"
            f"{episode_markup}\n"
            "          </ul>\n"
            "        </section>"
        ),
    )


def build_library_page(config: SiteConfig, library_catalog: LibraryCatalog) -> str:
    tag_markup = "\n".join(
        _render_library_tag(tag, base_url=config.base_url) for tag in library_catalog.tags
    )
    body_html = (
        "        <section>\n"
        "          <h2>Topics</h2>\n"
        "          <ul>\n"
        f"{tag_markup}\n"
        "          </ul>\n"
        "        </section>"
        if library_catalog.tags
        else "        <p>No tags available yet.</p>"
    )
    return _render_document(
        config=config,
        title="Library",
        description="Browse topics derived from repository-authored content.",
        canonical_path="/library/",
        eyebrow="Library",
        heading="Library",
        summary="Browse the site by topic instead of chronology alone.",
        metadata=f"{len(library_catalog.tags)} topics",
        body_html=body_html,
    )


def build_topic_page(config: SiteConfig, topic_page: TopicPage) -> str:
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
        body_html=(
            "        <nav class=\"breadcrumbs\">"
            f"<a href=\"{_absolute_url(config.base_url, '/library/')}\">Library</a></nav>\n"
            "        <section>\n"
            "          <h2>Entries</h2>\n"
            "          <ul>\n"
            f"{entry_markup}\n"
            "          </ul>\n"
            "        </section>"
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
    body_html: str,
) -> str:
    analytics_snippet = _render_analytics(config.analytics)
    canonical_url = _absolute_url(config.base_url, canonical_path)

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{html.escape(title)} | {html.escape(config.title)}</title>
    <meta name="description" content="{html.escape(description)}" />
    <link rel="canonical" href="{html.escape(canonical_url)}" />
    <style>
      :root {{
        color-scheme: light;
        --ink: #111827;
        --muted: #4b5563;
        --line: #d1d5db;
        --paper: linear-gradient(180deg, #fffdf8 0%, #f3efe5 100%);
        --accent: #0f766e;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        min-height: 100vh;
        font-family: Georgia, "Times New Roman", serif;
        color: var(--ink);
        background: var(--paper);
      }}
      main {{
        width: min(46rem, calc(100vw - 3rem));
        margin: 0 auto;
        padding: 4rem 0 5rem;
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
        margin: 1.25rem 0 0.75rem;
        font-size: clamp(2.2rem, 6vw, 4rem);
        line-height: 1;
      }}
      .meta, .summary {{
        color: var(--muted);
      }}
      .breadcrumbs {{
        margin-bottom: 1rem;
        color: var(--muted);
      }}
      .nav-grid {{
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--line);
      }}
      article {{
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--line);
      }}
      article p, article li, article blockquote {{
        font-size: 1.08rem;
        line-height: 1.75;
      }}
      article h2, article h3 {{
        margin-top: 2rem;
      }}
      article blockquote {{
        margin-left: 0;
        padding-left: 1rem;
        border-left: 4px solid var(--accent);
      }}
      article code {{
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      }}
    </style>
{analytics_snippet}  </head>
  <body>
    <main>
      <a href="{html.escape(config.base_url)}">Home</a>
      <div class="eyebrow">{html.escape(eyebrow)}</div>
      <h1>{html.escape(heading)}</h1>
      <p class="summary">{html.escape(summary)}</p>
      <p class="meta">{html.escape(metadata)}</p>
      <article>
{body_html}
      </article>
    </main>
  </body>
</html>
"""


def _build_recent_items(catalog: ContentCatalog) -> list[RecentContent]:
    items: list[RecentContent] = [
        RecentContent(
            title=page.title,
            kind="page",
            summary=page.summary,
            date=page.date,
            permalink=page.permalink,
        )
        for page in catalog.pages
    ]
    items.extend(
        RecentContent(
            title=episode.title,
            kind="episode",
            summary=episode.summary,
            date=episode.date,
            permalink=episode.permalink,
            saga_title=episode.saga_title,
            arc_title=episode.arc_title,
        )
        for episode in catalog.episodes
    )
    return sorted(items, key=lambda item: item.date, reverse=True)


def _render_recent_item(item: RecentContent, *, base_url: str) -> str:
    context = ""
    if item.saga_title:
        context = f" · {item.saga_title}"
        if item.arc_title:
            context += f" / {item.arc_title}"

    return (
        "          <li>\n"
        f'            <a href="{_absolute_url(base_url, item.permalink)}">[{html.escape(item.kind)}] '
        f"{html.escape(item.title)}</a>\n"
        f"            <small>{html.escape(item.date)}{html.escape(context)}</small>\n"
        f"            <p>{html.escape(item.summary)}</p>\n"
        "          </li>"
    )


def _render_saga_item(saga: Saga, *, base_url: str) -> str:
    return (
        "          <li>\n"
        f'            <a href="{_absolute_url(base_url, saga.permalink)}">{html.escape(saga.title)}</a>\n'
        f"            <small>{html.escape(saga.date)} · {html.escape(saga.status)}</small>\n"
        f"            <p>{html.escape(saga.summary)}</p>\n"
        "          </li>"
    )


def _render_arc_summary(arc: object, *, base_url: str) -> str:
    last_release = arc.last_release_date or "n/a"
    return (
        "            <li>\n"
        f'              <a href="{_absolute_url(base_url, arc.permalink)}">{html.escape(arc.title)}</a>\n'
        f"              <small>{arc.episode_count} episodes · last {html.escape(last_release)}</small>\n"
        "            </li>"
    )


def _render_timeline_entry(entry: object, *, base_url: str) -> str:
    return (
        "            <li>\n"
        f'              <a href="{_absolute_url(base_url, entry.permalink)}">[Ep {entry.number:02d}] {html.escape(entry.title)}</a>\n'
        f"              <small>{html.escape(entry.arc_title)} · {html.escape(entry.date)}</small>\n"
        "            </li>"
    )


def _render_arc_episode(episode: Episode, *, base_url: str) -> str:
    return (
        "            <li>\n"
        f'              <a href="{_absolute_url(base_url, episode.permalink)}">[Ep {episode.number:02d}] {html.escape(episode.title)}</a>\n'
        f"              <small>{html.escape(episode.date)}</small>\n"
        "            </li>"
    )


def _render_adjacent_navigation(
    *,
    previous_episode: object,
    next_episode: object,
    base_url: str,
) -> str:
    previous_markup = "<span></span>"
    next_markup = "<span></span>"

    if previous_episode is not None:
        previous_markup = (
            f'<a href="{_absolute_url(base_url, previous_episode.permalink)}">'
            f"&larr; Ep {previous_episode.number:02d} {html.escape(previous_episode.title)}</a>"
        )

    if next_episode is not None:
        next_markup = (
            f'<a href="{_absolute_url(base_url, next_episode.permalink)}">'
            f"Ep {next_episode.number:02d} {html.escape(next_episode.title)} &rarr;</a>"
        )

    return f'        <nav class="nav-grid">{previous_markup}{next_markup}</nav>'


def _render_library_tag(tag: str, *, base_url: str) -> str:
    return (
        "            <li>\n"
        f'              <a href="{_absolute_url(base_url, f"/library/{tag}/")}">{html.escape(tag)}</a>\n'
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
        f'              <a href="{_absolute_url(base_url, entry.permalink)}">[{html.escape(entry.kind)}] {html.escape(entry.title)}</a>\n'
        f"              <small>{html.escape(entry.date)}{context_markup}</small>\n"
        f"              <p>{html.escape(entry.summary)}</p>\n"
        "            </li>"
    )


def _absolute_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + path


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
