from __future__ import annotations

from src.app.domain.models.content import (
    ContentCatalog,
    LibraryCatalog,
    Page,
    TopicEntry,
    TopicPage,
)


def project_topic_catalog(catalog: ContentCatalog) -> LibraryCatalog:
    tags_to_entries: dict[str, list[TopicEntry]] = {}

    for page in catalog.pages:
        _add_page_entries(tags_to_entries, page)

    for episode in catalog.episodes:
        for tag in episode.tags:
            tags_to_entries.setdefault(tag, []).append(
                TopicEntry(
                    title=episode.title,
                    kind="episode",
                    summary=episode.summary,
                    date=episode.date,
                    permalink=episode.permalink,
                    saga_title=episode.saga_title,
                    arc_title=episode.arc_title,
                )
            )

    pages = tuple(
        TopicPage(
            tag=tag,
            entries=tuple(
                sorted(
                    entries,
                    key=lambda entry: (entry.date, entry.title),
                    reverse=True,
                )
            ),
        )
        for tag, entries in sorted(tags_to_entries.items())
        if entries
    )

    return LibraryCatalog(
        tags=tuple(page.tag for page in pages),
        pages=pages,
    )


def _add_page_entries(tags_to_entries: dict[str, list[TopicEntry]], page: Page) -> None:
    for tag in page.tags:
        tags_to_entries.setdefault(tag, []).append(
            TopicEntry(
                title=page.title,
                kind="page",
                summary=page.summary,
                date=page.date,
                permalink=page.permalink,
            )
        )
