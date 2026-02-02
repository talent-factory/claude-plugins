# External Resources

Discover more Claude Code plugins, MCP servers, and community resources beyond the Talent Factory ecosystem.

---

## Official Anthropic Resources

<div class="grid cards" markdown>

-   :material-shield-check:{ .lg .middle } **Anthropic Plugin Directory**

    ---

    The official, Anthropic-managed directory of high-quality Claude Code plugins.

    [:octicons-arrow-right-24: claude.com/plugins](https://claude.com/plugins)

-   :material-github:{ .lg .middle } **Official GitHub Repository**

    ---

    Anthropic's curated collection of verified plugins on GitHub.

    [:octicons-arrow-right-24: anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

-   :material-book-open-variant:{ .lg .middle } **MCP Documentation**

    ---

    Official documentation for connecting Claude Code to tools via MCP.

    [:octicons-arrow-right-24: Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)

</div>

---

## Community Marketplaces

These community-maintained marketplaces offer additional plugins and tools:

| Repository | Description | Focus |
|------------|-------------|-------|
| [ccplugins/marketplace](https://github.com/ccplugins/marketplace) | Curated awesome plugins marketplace | Quality-focused curation |
| [cased/claude-code-plugins](https://github.com/cased/claude-code-plugins) | Comprehensive plugin marketplace | Skills, MCP servers, hooks |
| [jmanhype/awesome-claude-code](https://github.com/jmanhype/awesome-claude-code) | Awesome list for Claude Code | Plugins, integrations, resources |

---

## MCP Server Directories

Model Context Protocol (MCP) servers extend Claude's capabilities. Find more servers here:

| Platform | Description |
|----------|-------------|
| [Build with Claude](https://www.buildwithclaude.com/mcp-servers) | MCP server discovery platform |
| [Composio MCP Guide](https://composio.dev/blog/claude-code-plugin) | Guide for improving workflows with plugins |

---

## Installing External Plugins

To install plugins from external marketplaces:

=== "Add Marketplace"

    ```bash
    # Add a community marketplace
    /plugin marketplace add owner/repo-name
    ```

=== "Browse & Install"

    ```bash
    # Browse available plugins
    /plugin

    # Install specific plugin
    /plugin install plugin-name@marketplace
    ```

=== "Direct Install"

    ```bash
    # Install from GitHub URL
    /plugin install https://github.com/owner/repo
    ```

!!! tip "Verify Before Installing"
    Always review the source code and documentation of third-party plugins before installation. Check for recent updates, community feedback, and security practices.

---

## Contributing Resources

Know of a great plugin resource we're missing?

- [:material-github: Open an Issue](https://github.com/talent-factory/claude-plugins/issues/new) to suggest additions
- [:material-source-pull: Submit a PR](https://github.com/talent-factory/claude-plugins/edit/main/docs/community/external-resources.md) to add it directly

---

## See Also

- [Plugin Catalog](../plugins/index.md) - Browse Talent Factory plugins
- [Plugin Development](../development/plugin-development.md) - Create your own plugins
- [Marketplace Setup](../getting-started/marketplace-setup.md) - Host your own marketplace
