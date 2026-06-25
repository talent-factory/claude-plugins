# Dev Browser Plugin

Browser automation for Claude Code, built on the [Playwright](https://playwright.dev/python/) Python API. Navigate websites, fill forms, take screenshots, test web applications, and scrape data with short, incremental scripts and a persistent session profile.

## Version 1.0.0

No background server, no Node toolchain, no browser extension — a single small Python helper (`scripts/browser.py`) plus the Playwright library. The browser runs with a **persistent profile**, so cookies and logins survive across separate script runs.

## Skill

### `dev-browser`

Drive a real Chromium browser one focused step at a time: write a small script, run it, read the printed state, decide the next step. Once a flow is proven, fold it into a single script.

**Features:**

- 🔁 Persistent session — cookies and logins carry over between scripts
- 🌳 YAML accessibility-tree snapshots for robust, role-based element targeting
- 📸 Screenshot capture for visual feedback
- 🕸️ Network request interception for efficient, paginated scraping
- 🌐 Honours an ambient `HTTPS_PROXY` and auto-detects a pre-installed Chromium (works out-of-the-box in Claude Code web)

**Trigger phrases:** "go to [url]", "click on", "fill out the form", "take a screenshot", "scrape", "automate", "test the website", "log into".

## Setup

```bash
pip install playwright
playwright install chromium   # skip in Claude Code web — Chromium is pre-installed
```

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

## Helper API (`scripts/browser.py`)

| Symbol | Description |
|---|---|
| `browser(headless=True, viewport=(1280, 800))` | Context manager yielding a persistent-profile Playwright `Page` |
| `snapshot(page, selector="body", max_chars=6000)` | YAML accessibility tree for element discovery |

The yielded `page` is a standard [Playwright Page](https://playwright.dev/python/docs/api/class-page).

**Environment variables:** `DEV_BROWSER_PROFILE` (profile dir), `DEV_BROWSER_CHROMIUM` (explicit Chromium path), `HTTPS_PROXY` (honoured if set).

## Element Discovery

`snapshot(page)` returns the accessibility tree — roles and accessible names — which you target by role and name rather than brittle CSS:

```python
page.get_by_role("button", name="Submit").click()
page.get_by_label("Search").fill("playwright")
page.get_by_role("link", name="Sign in").click()
```

## Scraping

For large datasets, intercept and replay the page's own API calls instead of scrolling the DOM. The skill's `references/scraping.md` covers request capture, schema discovery, and paginated replay using `page.request` (which reuses the browser's authenticated session).

## Self-check

```bash
python3 skills/dev-browser/scripts/browser.py
# → dev-browser self-check OK
```

Network-free: exercises browser launch, DOM, accessibility snapshot, a fill/click round-trip, and a screenshot against a `data:` URL.

## Installation

```json
{
  "enabledPlugins": {
    "dev-browser@talent-factory": true
  }
}
```

## Attribution

Inspired by [SawyerHood/dev-browser](https://github.com/SawyerHood/dev-browser) (MIT). Reimplemented on the Playwright Python API for the Talent Factory marketplace.
