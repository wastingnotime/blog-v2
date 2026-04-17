from __future__ import annotations

import math
import re

from src.app.domain.models.content import EntryMetadata, EntryTag, Episode, Page

WORDS_PER_MINUTE = 200


def project_page_metadata(page: Page) -> EntryMetadata:
    return EntryMetadata(
        publication_date=page.date,
        reading_time_minutes=_estimate_reading_time_minutes(page.body_markdown),
        tags=_project_tags(page.tags),
    )


def project_episode_metadata(episode: Episode) -> EntryMetadata:
    return EntryMetadata(
        publication_date=episode.date,
        reading_time_minutes=_estimate_reading_time_minutes(episode.body_markdown),
        tags=_project_tags(episode.tags),
    )


def _project_tags(tags: tuple[str, ...]) -> tuple[EntryTag, ...]:
    return tuple(
        EntryTag(
            name=tag,
            permalink=f"/library/{tag}/",
        )
        for tag in tags
    )


def _estimate_reading_time_minutes(body_markdown: str) -> int:
    words = re.findall(r"[A-Za-z0-9']+", body_markdown)
    if not words:
        return 1
    return max(1, math.ceil(len(words) / WORDS_PER_MINUTE))
