from __future__ import annotations

from src.app.domain.models.content import ArcView, SagasIndex, SagaSummary, SagaView


def project_sagas_index(
    saga_views: dict[str, SagaView],
    arc_views: dict[tuple[str, str], ArcView],
) -> SagasIndex:
    summaries: list[SagaSummary] = []

    for saga_slug, saga_view in sorted(saga_views.items()):
        start_permalink = _first_episode_permalink(saga_slug, arc_views)
        summaries.append(
            SagaSummary(
                title=saga_view.saga.title,
                permalink=saga_view.saga.permalink,
                summary=saga_view.saga.summary,
                start_permalink=start_permalink,
            )
        )

    return SagasIndex(sagas=tuple(summaries))


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
