from src.app.application.use_cases.project_navigation_state import project_navigation_state


def test_project_navigation_state_marks_home_active_for_root() -> None:
    links = project_navigation_state("/")

    active = [link.label for link in links if link.is_active]

    assert active == ["Home"]


def test_project_navigation_state_marks_saga_routes_under_sagas() -> None:
    links = project_navigation_state("/sagas/hireflow/the-origin-blueprint/")

    active = [link.label for link in links if link.is_active]

    assert active == ["Sagas"]


def test_project_navigation_state_marks_topic_routes_under_library() -> None:
    links = project_navigation_state("/library/architecture/")

    active = [link.label for link in links if link.is_active]

    assert active == ["Library"]


def test_project_navigation_state_marks_search_route_active() -> None:
    links = project_navigation_state("/search/")

    active = [link.label for link in links if link.is_active]

    assert active == ["Search"]


def test_project_navigation_state_marks_archive_route_active() -> None:
    links = project_navigation_state("/archives/")

    active = [link.label for link in links if link.is_active]

    assert active == ["Archives"]


def test_project_navigation_state_includes_search_link() -> None:
    links = project_navigation_state("/")

    labels = [link.label for link in links]

    assert labels == [
        "Home",
        "Search",
        "Archives",
        "Sagas",
        "Library",
        "Studio",
        "About",
    ]
