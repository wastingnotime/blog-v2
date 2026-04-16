from __future__ import annotations

from src.app.domain.models.site_config import AnalyticsConfig, SiteConfig


def build_homepage(config: SiteConfig) -> str:
    analytics_snippet = _render_analytics(config.analytics)

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{config.title}</title>
    <meta name="description" content="{config.description}" />
    <link rel="canonical" href="{config.base_url}" />
    <style>
      :root {{
        color-scheme: light;
        --ink: #111827;
        --muted: #4b5563;
        --line: #d1d5db;
        --paper: linear-gradient(180deg, #fffdf8 0%, #f3efe5 100%);
        --accent: #0f766e;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        min-height: 100vh;
        font-family: Georgia, "Times New Roman", serif;
        color: var(--ink);
        background: var(--paper);
      }}
      main {{
        width: min(56rem, calc(100vw - 3rem));
        margin: 0 auto;
        padding: 5rem 0 4rem;
      }}
      .eyebrow {{
        display: inline-block;
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 0.35rem 0.75rem;
        color: var(--muted);
        font-size: 0.85rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }}
      h1 {{
        margin: 1.5rem 0 1rem;
        font-size: clamp(2.5rem, 7vw, 4.75rem);
        line-height: 0.95;
      }}
      p {{
        max-width: 42rem;
        color: var(--muted);
        font-size: 1.1rem;
        line-height: 1.7;
      }}
      .card {{
        margin-top: 2.5rem;
        padding: 1.25rem 1.5rem;
        border-left: 4px solid var(--accent);
        background: rgba(255, 255, 255, 0.72);
        box-shadow: 0 1rem 2rem rgba(17, 24, 39, 0.06);
      }}
      code {{
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
        font-size: 0.95em;
      }}
    </style>
{analytics_snippet}  </head>
  <body>
    <main>
      <span class="eyebrow">blog-v2 bootstrap</span>
      <h1>{config.title}</h1>
      <p>{config.description}</p>
      <section class="card">
        <strong>Deployment target:</strong> GitHub Pages static files.<br />
        <strong>API dependency:</strong> none on <code>/api</code>.<br />
        <strong>Base URL:</strong> <code>{config.base_url}</code>
      </section>
    </main>
  </body>
</html>
"""


def _render_analytics(config: AnalyticsConfig | None) -> str:
    if config is None:
        return ""

    attributes = [
        "defer",
        f'data-domain="{config.domain}"',
    ]

    if config.api_host:
        api_host = config.api_host.rstrip("/")
        attributes.append(f'data-api="{api_host}/api/event"')

    return (
        f'    <script {" ".join(attributes)} src="{config.script_url}"></script>\n'
    )
