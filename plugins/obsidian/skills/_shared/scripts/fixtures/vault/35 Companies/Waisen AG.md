---
tags:
  - company
slug: waisen
---

### Mitarbeiter

```dataview
table role as Funktion
	where contains(tags, "person") and contains(company, "waisen")
	sort file.name asc
```
