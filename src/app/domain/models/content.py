from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    title: str
    slug: str
    summary: str
    date: str
    body_markdown: str
    tags: tuple[str, ...] = ()

    @property
    def permalink(self) -> str:
        return f"/{self.slug}/"


@dataclass(frozen=True)
class Saga:
    title: str
    slug: str
    summary: str
    date: str
    status: str

    @property
    def permalink(self) -> str:
        return f"/sagas/{self.slug}/"


@dataclass(frozen=True)
class Arc:
    title: str
    slug: str
    summary: str
    date: str
    saga_slug: str
    saga_title: str

    @property
    def permalink(self) -> str:
        return f"/sagas/{self.saga_slug}/{self.slug}/"


@dataclass(frozen=True)
class Episode:
    title: str
    slug: str
    summary: str
    date: str
    saga_slug: str
    saga_title: str
    arc_slug: str
    arc_title: str
    number: int
    body_markdown: str
    tags: tuple[str, ...] = ()

    @property
    def permalink(self) -> str:
        return f"/sagas/{self.saga_slug}/{self.arc_slug}/{self.slug}/"


@dataclass(frozen=True)
class RecentContent:
    title: str
    kind: str
    summary: str
    date: str
    permalink: str
    saga_title: str | None = None
    arc_title: str | None = None


@dataclass(frozen=True)
class HomepageSagaSummary:
    title: str
    permalink: str
    summary: str
    status: str
    episode_count: int
    last_release_date: str | None


@dataclass(frozen=True)
class HomepageSurface:
    recent_entries: tuple[RecentContent, ...]
    saga_summaries: tuple[HomepageSagaSummary, ...]


@dataclass(frozen=True)
class EpisodeNavigation:
    title: str
    permalink: str
    number: int


@dataclass(frozen=True)
class ArcNavigation:
    title: str
    permalink: str
    episode_count: int
    last_release_date: str | None


@dataclass(frozen=True)
class SagaTimelineEntry:
    title: str
    permalink: str
    number: int
    date: str
    arc_title: str


@dataclass(frozen=True)
class TopicEntry:
    title: str
    kind: str
    summary: str
    date: str
    permalink: str
    saga_title: str | None = None
    arc_title: str | None = None


@dataclass(frozen=True)
class TopicPage:
    tag: str
    entries: tuple[TopicEntry, ...]


@dataclass(frozen=True)
class LibraryCatalog:
    tags: tuple[str, ...]
    pages: tuple[TopicPage, ...]


@dataclass(frozen=True)
class SagaSummary:
    title: str
    permalink: str
    summary: str
    start_permalink: str | None


@dataclass(frozen=True)
class SagasIndex:
    sagas: tuple[SagaSummary, ...]


@dataclass(frozen=True)
class ArcView:
    arc: Arc
    episodes: tuple[Episode, ...]
    previous_episode: dict[str, EpisodeNavigation | None]
    next_episode: dict[str, EpisodeNavigation | None]


@dataclass(frozen=True)
class SagaView:
    saga: Saga
    arcs: tuple[ArcNavigation, ...]
    timeline: tuple[SagaTimelineEntry, ...]


@dataclass(frozen=True)
class ContentCatalog:
    pages: tuple[Page, ...]
    sagas: tuple[Saga, ...]
    arcs: tuple[Arc, ...]
    episodes: tuple[Episode, ...]
