from __future__ import annotations

from pathlib import Path
from typing import Protocol

from src.app.domain.models.content import ContentCatalog


class ContentLoader(Protocol):
    def load(self, content_root: Path) -> ContentCatalog:
        ...

