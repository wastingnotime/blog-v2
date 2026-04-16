from __future__ import annotations

from pathlib import Path

from src.app.application.use_cases.build_site import build_homepage
from src.app.domain.models.site_config import SiteConfig


class StaticSiteBuilder:
    def __init__(self, output_dir: Path) -> None:
        self._output_dir = output_dir

    def build(self, config: SiteConfig) -> Path:
        self._output_dir.mkdir(parents=True, exist_ok=True)
        homepage_path = self._output_dir / "index.html"
        homepage_path.write_text(build_homepage(config), encoding="utf-8")
        return homepage_path
