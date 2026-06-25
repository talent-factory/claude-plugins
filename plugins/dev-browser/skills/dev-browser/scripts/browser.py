"""Lean Playwright helper for the dev-browser skill.

Launches the pre-installed Chromium with a *persistent* profile directory, so
cookies, logins, and local storage survive across separate script runs — no
background server, no daemon, no Node toolchain. Each script is a short,
self-contained run that opens the same profile.

Usage (inline, run from anywhere):

    from browser import browser, snapshot

    with browser() as page:
        page.goto("https://example.com")
        print(page.title())

Headful display is rarely available in CI/sandbox environments, so headless is
the default. Override per call: ``browser(headless=False)``.
"""

from __future__ import annotations

import glob
import os
from contextlib import contextmanager
from pathlib import Path

from playwright.sync_api import sync_playwright

# One profile dir = one persistent session. Override with DEV_BROWSER_PROFILE.
PROFILE_DIR = Path(
    os.environ.get("DEV_BROWSER_PROFILE", Path.home() / ".dev-browser-profile")
)


def _chromium_executable() -> str | None:
    """Locate a pre-installed Chromium, or None to use Playwright's default.

    Sandboxed/web environments ship a Chromium under PLAYWRIGHT_BROWSERS_PATH
    whose build may not match the pip-installed Playwright; point at it directly
    to skip the version check. On a normal machine nothing is pre-installed, so
    we return None and Playwright uses the browser from ``playwright install``.
    """
    override = os.environ.get("DEV_BROWSER_CHROMIUM")
    if override:
        return override
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if base:
        hits = sorted(glob.glob(os.path.join(base, "chromium-*/chrome-linux/chrome")))
        if hits:
            return hits[-1]  # newest build present
    return None


@contextmanager
def browser(headless: bool = True, viewport: tuple[int, int] = (1280, 800)):
    """Yield a Playwright ``Page`` backed by a persistent Chromium profile.

    The browser context is closed on exit; the profile dir (cookies, storage)
    persists on disk for the next run.
    """
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    # Honour an ambient HTTPS proxy (Claude Code web/sandbox route outbound
    # traffic through one). Unset on a normal machine → no proxy, no effect.
    proxy_url = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    proxy = {"server": proxy_url} if proxy_url else None
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            headless=headless,
            executable_path=_chromium_executable(),
            proxy=proxy,
            ignore_https_errors=bool(proxy),
            viewport={"width": viewport[0], "height": viewport[1]},
        )
        page = context.pages[0] if context.pages else context.new_page()
        try:
            yield page
        finally:
            context.close()


def snapshot(page, selector: str = "body", max_chars: int = 6000) -> str:
    """Return the YAML accessibility tree for element discovery.

    Roles and accessible names nested by depth, e.g. ``- button "Sign in"``.
    Use it to find what to target, then interact with normal Playwright
    locators (``page.get_by_role``, ``get_by_text``, …). Scope it by passing a
    CSS ``selector`` to snapshot only part of a large page.
    """
    tree = page.locator(selector).aria_snapshot()
    if len(tree) > max_chars:
        return tree[:max_chars] + "\n… (truncated, pass a narrower selector)"
    return tree


if __name__ == "__main__":
    # ponytail: one runnable self-check. Hermetic — a data: URL, no network — so
    # it proves launch + DOM + a11y snapshot + interaction anywhere. Exercises a
    # real fill+read round-trip. Run: `python browser.py`.
    html = (
        "<title>Self Check</title><h1>Hello</h1>"
        "<input aria-label='name' id='n'>"
        "<button onclick=\"document.title=document.getElementById('n').value\">go</button>"
    )
    with browser() as page:
        page.goto("data:text/html," + html)
        assert page.title() == "Self Check", page.title()

        tree = snapshot(page)
        assert 'heading "Hello"' in tree, f"snapshot missing heading:\n{tree}"

        page.get_by_label("name").fill("typed-ok")
        page.get_by_role("button", name="go").click()
        assert page.title() == "typed-ok", f"interaction failed: {page.title()!r}"

        page.screenshot(path="/tmp/dev-browser-selfcheck.png")
    print("dev-browser self-check OK")
