# Dev Browser Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blue)](https://claude.ai)

## Version 1.0.0

**Browser automation with a persistent session for Claude Code.**
Navigate websites, fill forms, take screenshots, extract web data, test web
applications, and automate browser workflows — with short, incremental Python
scripts built on the [Playwright](https://playwright.dev/python/) API.

---

## Why This Plugin?

| Problem | Solution |
|---|---|
| Interact with web pages programmatically | Playwright-driven Chromium automation |
| Multi-step workflows that build on each other | Persistent profile (cookies/logins survive between scripts) |
| Unknown page layouts | YAML accessibility snapshots for element discovery |
| Form filling, clicking, navigation | Small focused scripts that print state between steps |
| Web scraping at scale | Network request interception and paginated API replay |

No background server, no Node toolchain, no browser extension — one small Python
helper and the Playwright library.

---

## Installation

### 1. Install the plugin

In your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": { "source": "github", "repo": "talent-factory/claude-plugins" }
    }
  },
  "enabledPlugins": {
    "dev-browser@talent-factory": true
  }
}
```

Or in Claude Code: `/plugin` → Browse Plugins → talent-factory → dev-browser → Install.

### 2. Prerequisites

```bash
pip install playwright
playwright install chromium   # skip in Claude Code web — Chromium is pre-installed
```

- Python 3.9+
- Chromium (installed by `playwright install`, or already present in Claude Code web/sandbox)

---

## Skill: `dev-browser`

Browser automation that keeps a persistent session across script runs.

**Key features:**

- Persistent profile — cookies and logins carry over between scripts
- YAML accessibility-tree snapshots for robust, role-based element targeting
- Screenshot capture for visual feedback
- Network request interception for efficient scraping
- Honours an ambient `HTTPS_PROXY` (works out-of-the-box in Claude Code web)

**Trigger phrases:** "go to [url]", "click on", "fill out the form", "take a
screenshot", "scrape", "automate", "test the website", "log into".

---

## Quick Start

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/skills/dev-browser/scripts" python3 - <<'EOF'
from browser import browser, snapshot

with browser() as page:
    page.goto("https://example.com")
    print(page.title(), page.url())
    print(snapshot(page))            # YAML accessibility tree
    page.screenshot(path="tmp/example.png")
EOF
```

---

## Helper API (`scripts/browser.py`)

| Symbol | Description |
|---|---|
| `browser(headless=True, viewport=(1280, 800))` | Context manager yielding a persistent-profile Playwright `Page` |
| `snapshot(page, selector="body", max_chars=6000)` | YAML accessibility tree for element discovery |

The yielded `page` is a standard [Playwright Page](https://playwright.dev/python/docs/api/class-page) — full API available.

**Environment variables:** `DEV_BROWSER_PROFILE` (profile dir), `DEV_BROWSER_CHROMIUM` (explicit Chromium path), `HTTPS_PROXY` (honoured if set).

See [`skills/dev-browser/SKILL.md`](skills/dev-browser/SKILL.md) for the full
workflow guide and [`references/scraping.md`](skills/dev-browser/references/scraping.md)
for the scraping playbook.

---

## Self-check

```bash
python3 skills/dev-browser/scripts/browser.py
# → dev-browser self-check OK
```

Network-free: it exercises browser launch, DOM, accessibility snapshot, a
fill/click round-trip, and a screenshot against a `data:` URL.

---

## Changelog

### 1.0.0

- Initial release: persistent-session browser automation on the Playwright Python API
- YAML accessibility-tree element discovery
- Network request interception for scraping
- Ambient `HTTPS_PROXY` support and pre-installed-Chromium auto-detection

---

## Attribution

Inspired by [SawyerHood/dev-browser](https://github.com/SawyerHood/dev-browser)
(MIT). Reimplemented on the Playwright Python API for the Talent Factory
marketplace.

---

**Made with ❤️ by Talent Factory GmbH**
