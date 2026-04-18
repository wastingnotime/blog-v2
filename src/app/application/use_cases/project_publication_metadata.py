from __future__ import annotations

from collections.abc import Iterable

from src.app.domain.models.content import (
    ArcView,
    ContentCatalog,
    FeedEntry,
    PublicationMetadata,
    SagaView,
    SitemapEntry,
    TopicPage,
)

DEFAULT_FEED_LIMIT = 10


def project_publication_metadata(
    catalog: ContentCatalog,
    saga_views: dict[str, SagaView],
    arc_views: dict[tuple[str, str], ArcView],
    topic_pages: tuple[TopicPage, ...],
    *,
    feed_limit: int = DEFAULT_FEED_LIMIT,
) -> PublicationMetadata:
    return PublicationMetadata(
        feed_entries=tuple(_build_feed_entries(catalog)[:feed_limit]),
        sitemap_entries=tuple(
            _build_sitemap_entries(catalog, saga_views, arc_views, topic_pages)
        ),
    )


def _build_feed_entries(catalog: ContentCatalog) -> list[FeedEntry]:
    entries: list[FeedEntry] = [
        FeedEntry(
            title=page.title,
            summary=page.summary,
            date=page.date,
            permalink=page.permalink,
        )
        for page in catalog.pages
    ]
    entries.extend(
        FeedEntry(
            title=episode.title,
            summary=episode.summary,
            date=episode.date,
            permalink=episode.permalink,
        )
        for episode in catalog.episodes
    )
    return sorted(entries, key=lambda entry: (entry.date, entry.permalink), reverse=True)


def _build_sitemap_entries(
    catalog: ContentCatalog,
    saga_views: dict[str, SagaView],
    arc_views: dict[tuple[str, str], ArcView],
    topic_pages: tuple[TopicPage, ...],
) -> list[SitemapEntry]:
    content_dates = [entry.date for entry in _build_feed_entries(catalog)]
    entries = [
        SitemapEntry(permalink="/", last_modified=_max_date(content_dates)),
        SitemapEntry(permalink="/archives/", last_modified=_max_date(content_dates)),
        SitemapEntry(
            permalink="/library/",
            last_modified=_max_date(
                entry.date for topic_page in topic_pages for entry in topic_page.entries
            ),
        ),
        SitemapEntry(
            permalink="/sagas/",
            last_modified=_max_date(
                saga_view.timeline[0].date if saga_view.timeline else saga_view.saga.date
                for saga_view in saga_views.values()
            ),
        ),
        SitemapEntry(permalink="/studio/", last_modified=None),
    ]

    entries.extend(
        SitemapEntry(
            permalink=page.permalink,
            last_modified=page.date,
        )
        for page in catalog.pages
    )

    entries.extend(
        SitemapEntry(
            permalink=saga_view.saga.permalink,
            last_modified=_max_date(
                [saga_view.saga.date, *(entry.date for entry in saga_view.timeline)]
            ),
        )
        for _, saga_view in sorted(saga_views.items())
    )

    entries.extend(
        SitemapEntry(
            permalink=arc_view.arc.permalink,
            last_modified=_max_date(
                [arc_view.arc.date, *(episode.date for episode in arc_view.episodes)]
            ),
        )
        for _, arc_view in sorted(arc_views.items())
    )

    entries.extend(
        SitemapEntry(
            permalink=episode.permalink,
            last_modified=episode.date,
        )
        for episode in sorted(catalog.episodes, key=lambda episode: episode.permalink)
    )

    entries.extend(
        SitemapEntry(
            permalink=f"/library/{topic_page.tag}/",
            last_modified=_max_date(entry.date for entry in topic_page.entries),
        )
        for topic_page in topic_pages
    )

    return sorted(entries, key=lambda entry: entry.permalink)


def _max_date(dates: Iterable[str]) -> str | None:
    normalized = tuple(date for date in dates if date)
    return max(normalized) if normalized else None
