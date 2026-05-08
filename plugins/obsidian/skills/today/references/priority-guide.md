# Priority Guide — Extended Rules

## Edge Cases

### Multiple sources referencing the same topic
If a Linear issue and a TaskNote both reference the same project or deliverable,
merge them into a single entry and use the higher of the two scores.

### All-day calendar events
All-day events (e.g., a submission deadline or off-site day) function as
due-date constraints. If an event title matches a task in TaskNotes or Linear,
boost that task's score by +20.

### GitHub staleness
A pull request that has not been updated in > 3 days receives a +10 score
bonus. A pull request created within the last 2 hours is informational only
(score 5).

### Gmail heuristics
Skip threads where:
- Sender domain ends in `noreply`, `notifications`, or `mailer-daemon`
- Subject starts with `Re:` and the thread has > 5 messages (likely handled)
- Labels include `CATEGORY_PROMOTIONS` or `CATEGORY_UPDATES`

Boost by +10 if the subject contains keywords that signal urgency or financial
or deadline relevance — adapt these to your own domain conventions.

## Recurring Patterns

### Monday morning
Add a synthetic "Weekly Review" item at score 40 if it is Monday before 10:00.

### Friday afternoon
Add a synthetic "Weekly wrap-up" item at score 30 if it is Friday after 14:00.

## Tuning the Threshold

If the user says "too much noise" — raise the minimum display threshold from
score 10 to 20.

If the user says "missing items" — include all items regardless of bucket
(remove the `else: continue` branch in Step 1).

## Vault Quirks

- Tasks in the daily notes folder may use either `tags: [task]` or the older
  `tag: task` frontmatter form. The `tasks.py --scan` fallback handles both.
- The TaskNotes HTTP API (without `--scan`) only finds tasks in
  plugin-monitored folders. Always use `--scan` when running `/today`.
- The `scheduled` field stores full ISO datetime (e.g.,
  `2026-05-08T09:00:00+02:00`). Truncate to `[:10]` for date comparisons.
