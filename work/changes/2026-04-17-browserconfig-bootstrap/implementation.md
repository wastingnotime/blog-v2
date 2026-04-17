# Implementation

## Scope implemented

Implemented the bounded browserconfig metadata slice defined in `docs/slices/2026-04-17-browserconfig-bootstrap.md`:

- emit deterministic root artifact `browserconfig.xml`
- add shared `<meta name="msapplication-config" ...>` in generated document head
- keep tile color and identity icon reuse aligned with existing publication metadata

## Code changes

- `src/app/application/use_cases/build_site.py`
  - added `browserconfig.xml` to `build_static_site(...)` output map
  - added `build_browserconfig(config: SiteConfig) -> str`
  - added shared `browserconfig_url` projection and `msapplication-config` meta tag in `_render_document(...)`

## Deterministic projections

- `browserconfig.xml` is generated with stable structure and values:
  - `square150x150logo` points to the existing `apple-touch-icon.png` absolute URL
  - `TileColor` reuses existing `THEME_COLOR` (`#fffdf8`)
- head metadata now includes deterministic:
  - `<meta name="msapplication-config" content="<base>/browserconfig.xml" />`

## Test updates

- `tests/unit/test_build_site.py`
  - asserts `browserconfig.xml` is present in generated pages and includes expected logo and tile color
  - adds shared-route assertions for `msapplication-config` head metadata
- `tests/integration/test_run_scenario.py`
  - includes `dist/browserconfig.xml` in expected output paths
  - asserts generated browserconfig content and homepage `msapplication-config` metadata

## Validation

- Command: `pytest`
- Result: `57 passed`
