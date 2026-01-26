# Testing Plugins

!!! info "Coming Soon"
    This guide is currently being developed. Check back soon for comprehensive testing documentation.

## Quick Start

Test your plugin locally:

```bash
# Test single plugin
claude --plugin-dir ./plugins/your-plugin

# Test entire marketplace
claude --plugin-dir .
```

## Validation

Use core plugin commands:

```bash
/check-commands  # Validate command files
/check-agents    # Validate agent definitions
/run-ci          # Run CI checks locally
```

---

## Related Resources

- **[Plugin Development](plugin-development.md)** - Create plugins
- **[CI/CD](ci-cd.md)** - Automated testing

