# plugin.json Schema

!!! info "Coming Soon"
    This reference is currently being developed. Check back soon for complete schema documentation.

## Overview

The `plugin.json` file contains plugin metadata and configuration.

## Location

```
plugins/your-plugin/.claude-plugin/plugin.json
```

## Example

```json
{
  "name": "your-plugin",
  "version": "1.0.0",
  "displayName": "Your Plugin",
  "description": "Brief description",
  "keywords": ["tag1", "tag2"],
  "author": "Your Name",
  "license": "MIT"
}
```

---

## Related Resources

- **[marketplace.json](marketplace-json.md)** - Marketplace schema
- **[Plugin Development](../development/plugin-development.md)** - Create plugins

