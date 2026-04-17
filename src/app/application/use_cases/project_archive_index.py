from __future__ import annotations

from src.app.domain.models.content import ArchiveEntry, ArchiveIndex, ContentCatalog


def project_archive_index(catalog: ContentCatalog) -> ArchiveIndex:
    entries: list[ArchiveEntry] = [
        ArchiveEntry(
            title=page.title,
            kind="page",
            summary=page.summary,
            date=page.date,
            permalink=page.permalink,
        )
        for page in catalog.pages
    ]
    entries.extend(
        ArchiveEntry(
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
    return ArchiveIndex(
        entries=tuple(
            sorted(entries, key=lambda entry: (entry.date, entry.permalink), reverse=True)
        )
    )
