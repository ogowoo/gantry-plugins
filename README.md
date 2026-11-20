# Gantry Plugins

Standalone plugin packages for [Gantry](https://github.com/ogowoo/gantry).
Each package contains a `plugin.json` at its root and can be installed without
the Gantry source tree.

Compatibility: **Gantry >=0.11.0-beta.27** or newer.

## Packages

| Package | Version | Tools | Download |
|---|---:|---:|---|
| `coding-harness-tools` | 1.0.0 | 3 | [zip](dist/coding-harness-tools-1.0.0.zip) |
| `deepseek-web` | 0.1.0 | 0 | [zip](dist/deepseek-web-0.1.0.zip) |
| `image-gen` | 0.1.0 | 1 | [zip](dist/image-gen-0.1.0.zip) |
| `kb` | 0.1.0 | 5 | [zip](dist/kb-0.1.0.zip) |
| `mcp` | 0.2.0 | 3 | [zip](dist/mcp-0.2.0.zip) |
| `power-apps` | 0.1.0 | 8 | [zip](dist/power-apps-0.1.0.zip) |
| `power-automate` | 0.1.0 | 9 | [zip](dist/power-automate-0.1.0.zip) |
| `power-platform` | 0.1.0 | 9 | [zip](dist/power-platform-0.1.0.zip) |
| `research` | 0.1.0 | 1 | [zip](dist/research-0.1.0.zip) |
| `schedule` | 0.1.0 | 4 | [zip](dist/schedule-0.1.0.zip) |
| `teams-bot` | 0.1.0 | 3 | [zip](dist/teams-bot-0.1.0.zip) |
| `telegram` | 0.1.0 | 0 | [zip](dist/telegram-0.1.0.zip) |
| `vector-index` | 0.1.0 | 4 | [zip](dist/vector-index-0.1.0.zip) |
| `visual-design` | 0.1.0 | 6 | [zip](dist/visual-design-0.1.0.zip) |
| `web-search` | 0.1.0 | 1 | [zip](dist/web-search-0.1.0.zip) |

## Install

### WebUI plugin manager

1. Download the `.zip` from `dist/` (or from this repository's Releases).
2. Open Gantry → Settings → Plugins → Install.
3. Choose the zip, install, then enable the plugin.

Installing requires `allow_plugin_install: true` in Gantry's `config.json`.

### Plugin API

```http
POST /v1/plugins/install
Content-Type: application/json

{"source": "C:\\path\\to\\visual-design-0.1.0.zip"}
```

### From this checkout

```text
POST /v1/plugins/install
{"source": "C:\\path\\to\\gantry-plugins\\packages\\visual-design"}
```

## Uninstall

Every package declares `allow_uninstall: true`. Use the plugin manager's
uninstall action, or:

```http
POST /v1/plugins/uninstall
{"name": "visual-design", "keep_backup": true}
```

## Repository layout

```text
packages/       editable plugin sources (one directory per plugin)
dist/           installable zip packages
catalog.json    versions, checksums, tools and download paths
scripts/        build and verify helpers
```

## Secrets

Packages include no `.env`, `data/`, `EdgeProfile/`, or local plugin state.
API keys are read from Gantry environment variables or plugin configuration
at runtime.

## License

No separate license is declared for this packaging repository; the bundled
plugin sources are provided as-is for use with Gantry.

