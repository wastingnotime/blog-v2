from __future__ import annotations

from pathlib import Path

from src.app.application.use_cases.build_site import build_static_site
from src.app.domain.models.content import ContentCatalog
from src.app.domain.models.site_config import SiteConfig


class StaticSiteBuilder:
    def __init__(self, output_dir: Path) -> None:
        self._output_dir = output_dir

    def build(self, config: SiteConfig, catalog: ContentCatalog) -> list[Path]:
        self._output_dir.mkdir(parents=True, exist_ok=True)
        written_paths: list[Path] = []

        for relative_path, html in build_static_site(config, catalog).items():
            output_path = self._output_dir / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")
            written_paths.append(output_path)

        return sorted(written_paths)
