from __future__ import annotations

from src.app.domain.models.content import (
    ArcView,
    ContentCatalog,
    HomepageSagaSummary,
    HomepageSurface,
    RecentContent,
    SagaView,
)

DEFAULT_RECENT_LIMIT = 3


def project_homepage_surface(
    catalog: ContentCatalog,
    saga_views: dict[str, SagaView],
    arc_views: dict[tuple[str, str], ArcView],
    *,
    recent_limit: int = DEFAULT_RECENT_LIMIT,
) -> HomepageSurface:
    recent_entries = tuple(_build_recent_entries(catalog)[:recent_limit])
    saga_summaries = tuple(
        _build_saga_summary(saga_view, arc_views)
        for _, saga_view in sorted(saga_views.items())
    )
    return HomepageSurface(
        recent_entries=recent_entries,
        saga_summaries=saga_summaries,
    )


def _build_recent_entries(catalog: ContentCatalog) -> list[RecentContent]:
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
    return sorted(items, key=lambda item: (item.date, item.permalink), reverse=True)


def _build_saga_summary(
    saga_view: SagaView,
    arc_views: dict[tuple[str, str], ArcView],
) -> HomepageSagaSummary:
    episode_dates = [
        episode.date
        for (saga_slug, _), arc_view in arc_views.items()
        if saga_slug == saga_view.saga.slug
        for episode in arc_view.episodes
    ]
    last_release_date = max(episode_dates) if episode_dates else None
    episode_count = sum(arc.episode_count for arc in saga_view.arcs)
    return HomepageSagaSummary(
        title=saga_view.saga.title,
        permalink=saga_view.saga.permalink,
        summary=saga_view.saga.summary,
        status=saga_view.saga.status,
        episode_count=episode_count,
        last_release_date=last_release_date,
    )
