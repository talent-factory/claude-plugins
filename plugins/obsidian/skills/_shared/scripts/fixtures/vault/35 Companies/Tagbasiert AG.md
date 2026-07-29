---
tags:
  - company
---

```dataview
table role as Funktion
	where contains(tags, "person") and contains(tags, "tagbasiert")
	sort file.name asc
```
