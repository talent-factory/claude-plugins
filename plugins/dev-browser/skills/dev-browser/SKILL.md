---
name: dev-browser
version: 1.0.0
description: |
  Browser automation with a persistent session, driven by the Playwright Python
  API. Use when users ask to navigate websites, fill forms, take screenshots,
  extract web data, test web apps, or automate browser workflows. Trigger
  phrases include "go to [url]", "click on", "fill out the form", "take a
  screenshot", "scrape", "automate", "test the website", "log into", or any
  browser interaction request.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
---

# Dev Browser Skill

Drive a real Chromium browser with short, focused Python scripts. Write one
small script per step (navigate, inspect, click, fill), observe the result, then
decide the next step. Once a multi-step flow is proven and worth repeating, fold
it into a single script.

A small helper, `scripts/browser.py`, launches Chromium with a **persistent
profile**, so cookies and logins survive across separate runs — no server, no
daemon, no Node toolchain.

## Setup

The skill needs the Playwright Python package. Chromium itself is pre-installed
in Claude Code web/sandbox environments; on a local machine install it once.

```bash
pip install playwright
playwright install chromium   # skip in Claude Code web — Chromium is already present
```

## Running scripts

Run scripts with the helper directory on `PYTHONPATH` so `import browser` works.
In an installed plugin the path is `$CLAUDE_PLUGIN_ROOT`:

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/skills/dev-browser/scripts" python3 - <<'EOF'
from browser import browser, snapshot

with browser() as page:                       # persistent profile, headless
    page.goto("https://example.com")
    print(page.title(), page.url())
EOF
```

If `$CLAUDE_PLUGIN_ROOT` is unset (e.g. running the files directly), `cd` into
`skills/dev-browser/scripts/` first and drop the `PYTHONPATH` prefix.

### Key principles

1. **Small scripts** — each does ONE thing; print state at the end to decide what's next.
2. **`with browser() as page:`** — the context closes the browser; the profile (cookies, storage) persists on disk for the next run.
3. **Discover, then target** — use `snapshot(page)` to find elements, then act with normal Playwright locators (`get_by_role`, `get_by_text`, `get_by_label`).
4. **Save reusable scripts** to `tmp/` only when a flow is complex or explicitly requested; otherwise run inline.

## Helper API (`browser.py`)

```python
from browser import browser, snapshot

with browser(headless=True, viewport=(1280, 800)) as page:
    ...   # `page` is a standard Playwright Page

snapshot(page, selector="body", max_chars=6000)  # YAML accessibility tree (str)
```

- Persistent profile dir defaults to `~/.dev-browser-profile`; override with `DEV_BROWSER_PROFILE`.
- An ambient `HTTPS_PROXY` is honoured automatically (required in Claude Code web/sandbox); unset on a normal machine, it has no effect.

## Element discovery

`snapshot(page)` returns the YAML accessibility tree — roles and accessible
names, the same view a screen reader gets:

```yaml
- heading "Top stories" [level=1]
- link "Sign in"
- textbox "Search"
- button "Submit"
```

Target those by role and name — robust against markup churn:

```python
page.get_by_role("button", name="Submit").click()
page.get_by_label("Search").fill("playwright")
page.get_by_role("link", name="Sign in").click()
```

Scope the snapshot to part of a large page with a CSS selector:
`snapshot(page, "main")`.

## Common operations

```python
# Navigation + waiting
page.goto("https://example.com", wait_until="domcontentloaded")
page.wait_for_selector(".results")
page.wait_for_url("**/success")

# Reading
title = page.title()
text = page.inner_text("body")
value = page.get_by_label("Email").input_value()

# Screenshots (visual feedback)
page.screenshot(path="tmp/page.png")
page.screenshot(path="tmp/full.png", full_page=True)
```

## Workflow loop

1. **Write** a script for one action.
2. **Run** it and read the printed state.
3. **Evaluate** — did it work? what's the current URL/title/visible text?
4. **Decide** — done, or another step?
5. **Repeat** until the task is complete.

## Scraping data

For large datasets, intercept and replay the page's own API calls instead of
scrolling the DOM. See [references/scraping.md](references/scraping.md) for
request capture, schema discovery, and paginated replay in Python.

## Error recovery

The persistent profile means state survives a failed run. Re-open and inspect:

```bash
PYTHONPATH="$CLAUDE_PLUGIN_ROOT/skills/dev-browser/scripts" python3 - <<'EOF'
from browser import browser
with browser() as page:
    page.goto("https://example.com")
    page.screenshot(path="tmp/debug.png")
    print({"url": page.url(), "title": page.title(),
           "body": page.inner_text("body")[:200]})
EOF
```

## Self-check

`scripts/browser.py` has a runnable, network-free self-check that exercises
launch, DOM, accessibility snapshot, a fill/click round-trip, and a screenshot:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/skills/dev-browser/scripts/browser.py"
# prints: dev-browser self-check OK
```

---

Inspired by [SawyerHood/dev-browser](https://github.com/SawyerHood/dev-browser);
reimplemented on the Playwright Python API for this marketplace.
