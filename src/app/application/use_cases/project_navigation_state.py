from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NavigationLink:
    label: str
    path: str
    is_active: bool


def project_navigation_state(current_path: str) -> tuple[NavigationLink, ...]:
    active_section = _active_section_for_path(current_path)
    links = (
        ("Home", "/"),
        ("Search", "/search/"),
        ("Archives", "/archives/"),
        ("Sagas", "/sagas/"),
        ("Library", "/library/"),
        ("Studio", "/studio/"),
        ("About", "/about/"),
    )
    return tuple(
        NavigationLink(
            label=label,
            path=path,
            is_active=(label.lower() == active_section),
        )
        for label, path in links
    )


def _active_section_for_path(current_path: str) -> str:
    normalized = current_path if current_path.startswith("/") else f"/{current_path}"
    if normalized == "/":
        return "home"
    if normalized.startswith("/search/"):
        return "search"
    if normalized.startswith("/archives/"):
        return "archives"
    if normalized.startswith("/sagas/"):
        return "sagas"
    if normalized.startswith("/library/"):
        return "library"
    if normalized.startswith("/studio/"):
        return "studio"
    if normalized.startswith("/about/"):
        return "about"
    return "home"
