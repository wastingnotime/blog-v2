from src.app.application.use_cases.project_route_robots_policy import (
    project_route_robots_policy,
)


def test_project_route_robots_policy_returns_noindex_for_search_route() -> None:
    assert project_route_robots_policy("/search/") == "noindex,follow"


def test_project_route_robots_policy_keeps_index_for_durable_routes() -> None:
    assert project_route_robots_policy("/") == "index,follow"
    assert project_route_robots_policy("/archives/") == "index,follow"
    assert project_route_robots_policy("/about/") == "index,follow"
