---
tags:
  - company
slug: bedag
aliases:
  - Bedag
---

### Mitarbeiter

```dataview
table role as Funktion
	where contains(tags, "person") and contains(company, "bedag")
	sort file.name asc
```
