# marketplace.json Schema

!!! info "Coming Soon"
    This reference is currently being developed. Check back soon for complete schema documentation.

## Overview

The `marketplace.json` file defines the marketplace catalog and lists all available plugins.

## Location

```
.claude-plugin/marketplace.json
```

## Example

```json
{
  "name": "talent-factory",
  "version": "1.0.0",
  "owner": {
    "name": "Talent Factory GmbH",
    "email": "support@talent-factory.ch"
  },
  "description": "Professional Claude Code plugins",
  "plugins": [
    {
      "name": "git-workflow",
      "description": "Professional git workflow",
      "source": "./plugins/git-workflow",
      "version": "2.0.0",
      "tags": ["git", "workflow"]
    }
  ]
}
```

---

## Related Resources

- **[plugin.json](plugin-json.md)** - Plugin metadata schema
- **[Plugin Development](../development/plugin-development.md)** - Create plugins

