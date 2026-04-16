from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    title: str
    slug: str
    summary: str
    date: str
    body_markdown: str

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
class ContentCatalog:
    pages: tuple[Page, ...]
    sagas: tuple[Saga, ...]
    episodes: tuple[Episode, ...]

