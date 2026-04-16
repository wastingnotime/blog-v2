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
