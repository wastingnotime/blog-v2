from __future__ import annotations

from src.app.domain.models.content import (
    Arc,
    ArcNavigation,
    ArcView,
    ContentCatalog,
    Episode,
    EpisodeNavigation,
    Saga,
    SagaTimelineEntry,
    SagaView,
)


def project_arc_views(catalog: ContentCatalog) -> dict[tuple[str, str], ArcView]:
    episodes_by_arc: dict[tuple[str, str], list[Episode]] = {}
    for episode in catalog.episodes:
        key = (episode.saga_slug, episode.arc_slug)
        episodes_by_arc.setdefault(key, []).append(episode)

    arc_views: dict[tuple[str, str], ArcView] = {}
    for arc in catalog.arcs:
        key = (arc.saga_slug, arc.slug)
        ordered_episodes = tuple(_order_arc_episodes(episodes_by_arc.get(key, [])))
        previous_episode = {
            episode.slug: (
                None
                if index == 0
                else EpisodeNavigation(
                    title=ordered_episodes[index - 1].title,
                    permalink=ordered_episodes[index - 1].permalink,
                    number=ordered_episodes[index - 1].number,
                )
            )
            for index, episode in enumerate(ordered_episodes)
        }
        next_episode = {
            episode.slug: (
                None
                if index == len(ordered_episodes) - 1
                else EpisodeNavigation(
                    title=ordered_episodes[index + 1].title,
                    permalink=ordered_episodes[index + 1].permalink,
                    number=ordered_episodes[index + 1].number,
                )
            )
            for index, episode in enumerate(ordered_episodes)
        }
        arc_views[key] = ArcView(
            arc=arc,
            episodes=ordered_episodes,
            previous_episode=previous_episode,
            next_episode=next_episode,
        )

    return arc_views


def project_saga_views(
    catalog: ContentCatalog,
    arc_views: dict[tuple[str, str], ArcView],
) -> dict[str, SagaView]:
    saga_views: dict[str, SagaView] = {}

    for saga in catalog.sagas:
        saga_arc_views = [
            arc_view
            for arc_key, arc_view in arc_views.items()
            if arc_key[0] == saga.slug
        ]
        saga_arc_views.sort(key=lambda arc_view: (arc_view.arc.date, arc_view.arc.slug))

        arcs = tuple(
            ArcNavigation(
                title=arc_view.arc.title,
                permalink=arc_view.arc.permalink,
                episode_count=len(arc_view.episodes),
                last_release_date=(
                    arc_view.episodes[-1].date if arc_view.episodes else None
                ),
            )
            for arc_view in saga_arc_views
        )

        timeline_entries = [
            SagaTimelineEntry(
                title=episode.title,
                permalink=episode.permalink,
                number=episode.number,
                date=episode.date,
                arc_title=episode.arc_title,
            )
            for arc_view in saga_arc_views
            for episode in arc_view.episodes
        ]
        timeline_entries.sort(
            key=lambda entry: (entry.date, entry.number, entry.title),
            reverse=True,
        )

        saga_views[saga.slug] = SagaView(
            saga=saga,
            arcs=arcs,
            timeline=tuple(timeline_entries),
        )

    return saga_views


def _order_arc_episodes(episodes: list[Episode]) -> list[Episode]:
    return sorted(episodes, key=lambda episode: (episode.number, episode.date, episode.slug))
