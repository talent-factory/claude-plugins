# Priority Guide — Extended Rules

## Edge Cases

### Multiple sources referencing the same topic
If a Plane work item, a TaskNote, and an Apple Reminder reference the same
deliverable (same Plane identifier such as `PROJ-123` in the title, or the same
title), merge them into a single entry and use the highest score.

### All-day calendar events
All-day events (e.g., a submission deadline or off-site day) function as
due-date constraints. If an event title matches a task in TaskNotes or Plane,
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
  plugin-monitored folders. Always use `--scan` when running `/obsidian:today`.
- The `scheduled` field stores full ISO datetime (e.g.,
  `2026-05-08T09:00:00+02:00`). Truncate to `[:10]` for date comparisons.

## Apple Reminders

- Reminders are fetched with `remindctl show overdue|today --json`. Apple stores
  date-only reminders at local midnight, so a due time of 00:00 means "all day".
- Reminders overdue by more than 7 days are counted, not listed. In practice they
  are read-later links; listing them would bury real work. Adjust the 7-day
  threshold in Step 5 of `SKILL.md` if needed.
- `REMINDERS_LISTS` (comma-separated) limits the lists. Use it to exclude shared
  lists such as family shopping lists.
- First run: macOS asks for Reminders access. If the prompt never appeared, run
  `remindctl authorize` once in a terminal.

## Plane

- The self-hosted edition rejects PQL. Filtering by assignee and state group
  happens client-side (see Step 4 in `SKILL.md`).
- Backlog items count only when `targetDate` ≤ today, so an unprioritised
  backlog does not flood the briefing.
