def project_route_robots_policy(canonical_path: str) -> str:
    if canonical_path == "/search/":
        return "noindex,follow"
    return "index,follow"
