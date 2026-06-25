# Scraping Guide

## Overview

For scraping large datasets, intercept and replay the page's own network
requests rather than scrolling the DOM. This is faster, more reliable, and
sidesteps infinite-scroll and pagination quirks.

## Request capture

Use Playwright route interception to record the API calls a page makes:

```python
from browser import browser

requests = []

with browser() as page:
    def record(route):
        req = route.request
        requests.append({"url": req.url, "method": req.method,
                         "headers": req.headers})
        route.continue_()

    page.route("**/*", record)
    page.goto("https://example.com/data", wait_until="networkidle")

# Find the data endpoints
api = [r for r in requests if "/api/" in r["url"]]
for r in api:
    print(r["method"], r["url"])
```

## Schema discovery

1. Navigate to the page and trigger the data load (scroll, click "load more", etc.).
2. Inspect the captured requests to find the JSON endpoint.
3. Fetch one page of the endpoint and examine the response shape before looping.

```python
resp = page.request.get(api[0]["url"])
print(resp.status, resp.json())
```

`page.request` reuses the browser's cookies and session, so authenticated
endpoints work without copying headers by hand.

## Paginated replay

Once the endpoint and pagination pattern are known, loop with the in-browser
request context (keeps auth/cookies) instead of the DOM:

```python
all_items, page_num = [], 1
while True:
    resp = page.request.get(f"{api_url}?page={page_num}&limit=100")
    data = resp.json()
    items = data.get("items", [])
    all_items.extend(items)
    if len(items) < 100:
        break
    page_num += 1

print(f"collected {len(all_items)} items")
```

## Best practices

- **Respect rate limits** — add small delays (`page.wait_for_timeout(ms)`) between requests to external sites.
- **Cache intermediate results** — write each page to `tmp/` so a failure mid-run doesn't force a full re-fetch.
- **Validate before processing** — check `resp.status` and the response shape on the first call.
- **Handle transient errors** — retry on timeouts/5xx with a short backoff.
