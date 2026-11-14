# Reminders script

Run this in the same shell command that exports `REMINDERS_LISTS` (leave it unset for all lists). It prints the open reminders as JSON, each with `_bucket` (`today`, `overdue`, `stale`), `_due_local`, `_all_day` and `_age_days`.

```bash
python3 - <<'PY'
import json, os, subprocess
from datetime import date, datetime

today = date.today()
lists = {s.strip() for s in os.environ.get("REMINDERS_LISTS", "").split(",") if s.strip()}
seen, out = set(), []
for flt in ("overdue", "today"):
    r = subprocess.run(["remindctl", "show", flt, "--json", "--no-input"],
                       capture_output=True, text=True)
    if r.returncode:
        continue
    for rem in json.loads(r.stdout or "[]"):
        if rem["id"] in seen or rem.get("isCompleted"):
            continue
        if lists and rem.get("listName") not in lists:
            continue
        seen.add(rem["id"])
        due = rem.get("dueDate")
        d = datetime.fromisoformat(due.replace("Z", "+00:00")).astimezone() if due else None
        age = (today - d.date()).days if d else 0
        rem["_due_local"] = d.isoformat(timespec="minutes") if d else None
        rem["_all_day"] = bool(d) and d.hour == 0 and d.minute == 0
        rem["_age_days"] = max(age, 0)
        rem["_bucket"] = "today" if age <= 0 else ("overdue" if age <= 7 else "stale")
        out.append(rem)
print(json.dumps(out, indent=2, ensure_ascii=False))
PY
```
