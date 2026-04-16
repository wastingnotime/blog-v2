from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalyticsConfig:
    provider: str
    domain: str
    script_url: str
    api_host: str | None = None


@dataclass(frozen=True)
class SiteConfig:
    title: str
    description: str
    base_url: str
    analytics: AnalyticsConfig | None = None
