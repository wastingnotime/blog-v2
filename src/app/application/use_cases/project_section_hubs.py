from __future__ import annotations

from src.app.domain.models.content import ArcView, SagasIndex, SagaSummary, SagaView


def project_sagas_index(
    saga_views: dict[str, SagaView],
    arc_views: dict[tuple[str, str], ArcView],
) -> SagasIndex:
    summaries: list[tuple[str, str, SagaSummary]] = []

    for saga_slug, saga_view in saga_views.items():
        start_permalink = _first_episode_permalink(saga_slug, arc_views)
        last_release_date = _last_release_date(saga_slug, saga_views, arc_views)
        summaries.append(
            (
                last_release_date or "0000-00-00",
                saga_view.saga.title,
                SagaSummary(
                    title=saga_view.saga.title,
                    permalink=saga_view.saga.permalink,
                    summary=saga_view.saga.summary,
                    start_permalink=start_permalink,
                ),
            )
        )

    return SagasIndex(
        sagas=tuple(summary for _, _, summary in sorted(summaries, reverse=True))
    )


def _last_release_date(
    saga_slug: str,
    saga_views: dict[str, SagaView],
    arc_views: dict[tuple[str, str], ArcView],
) -> str | None:
    release_dates: list[str] = []
    for (current_saga_slug, _), arc_view in arc_views.items():
        if current_saga_slug != saga_slug:
            continue
        release_dates.extend(episode.date for episode in arc_view.episodes)

    if release_dates:
        return max(release_dates)

    saga_view = saga_views.get(saga_slug)
    return saga_view.saga.date if saga_view else None


def _first_episode_permalink(
    saga_slug: str,
    arc_views: dict[tuple[str, str], ArcView],
) -> str | None:
    candidate_arcs = [
        arc_view
        for (current_saga_slug, _), arc_view in arc_views.items()
        if current_saga_slug == saga_slug
    ]
    candidate_arcs.sort(key=lambda arc_view: (arc_view.arc.date, arc_view.arc.slug))

    for arc_view in candidate_arcs:
        if arc_view.episodes:
            return arc_view.episodes[0].permalink

    return None
