from __future__ import annotations

from pathlib import Path

from src.app.application.ports.content_loader import ContentLoader
from src.app.domain.models.content import ContentCatalog


def load_content_catalog(*, loader: ContentLoader, content_root: Path) -> ContentCatalog:
    return loader.load(content_root)

