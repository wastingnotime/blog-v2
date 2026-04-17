from __future__ import annotations

from src.app.domain.models.content import ContentCatalog, SearchEntry, SearchIndex
from src.app.domain.models.site_config import SiteConfig


def project_search_index(config: SiteConfig, catalog: ContentCatalog) -> SearchIndex:
    entries = [
        *(_build_page_entry(config, page) for page in catalog.pages),
        *(_build_saga_entry(config, saga) for saga in catalog.sagas),
        *(_build_arc_entry(config, arc) for arc in catalog.arcs),
        *(_build_episode_entry(config, episode) for episode in catalog.episodes),
    ]
    return SearchIndex(
        entries=tuple(
            sorted(
                entries,
                key=lambda entry: (
                    entry.date or "",
                    entry.type,
                    entry.url,
                ),
                reverse=True,
            )
        )
    )


def _build_page_entry(config: SiteConfig, page: object) -> SearchEntry:
    return SearchEntry(
        title=page.title,
        url=_absolute_url(config.base_url, page.permalink),
        type="page",
        summary=page.summary,
        tags=page.tags,
        date=page.date,
    )


def _build_saga_entry(config: SiteConfig, saga: object) -> SearchEntry:
    return SearchEntry(
        title=saga.title,
        url=_absolute_url(config.base_url, saga.permalink),
        type="saga",
        summary=saga.summary,
        date=saga.date,
    )


def _build_arc_entry(config: SiteConfig, arc: object) -> SearchEntry:
    return SearchEntry(
        title=arc.title,
        url=_absolute_url(config.base_url, arc.permalink),
        type="arc",
        summary=arc.summary,
        context=arc.saga_title,
        date=arc.date,
    )


def _build_episode_entry(config: SiteConfig, episode: object) -> SearchEntry:
    return SearchEntry(
        title=episode.title,
        url=_absolute_url(config.base_url, episode.permalink),
        type="episode",
        summary=episode.summary,
        tags=episode.tags,
        context=f"{episode.saga_title} · {episode.arc_title}",
        date=episode.date,
    )


def _absolute_url(base_url: str, path: str) -> str:
    normalized_base = base_url.rstrip("/")
    normalized_path = "/" + path.strip("/")
    if normalized_path == "/":
        return normalized_base + "/"
    return normalized_base + normalized_path + "/"
