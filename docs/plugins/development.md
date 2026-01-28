# Development Plugin

Expert development agents and project initialization for modern programming languages and frameworks.

## Version 1.1.0

This plugin provides specialized agents for Java development and commands for initializing open source projects with GitHub best practices.

## Commands

### `/init-project`

Initialize new open source projects with GitHub best practices.

**Features:**

- Complete project structure with community standards
- LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
- GitHub templates (issues, PRs, workflows)
- Language-specific setup (Python, Node.js, Go, Java)
- CI/CD ready with GitHub Actions

**Usage:**

```bash
/init-project --git              # Standard Git project
/init-project --uv               # Python project with uv
/init-project --interactive      # Interactive mode
/init-project --name "project"   # With project name
```

**Created Files:**

- CODE_OF_CONDUCT.md - Contributor Covenant 2.1
- CONTRIBUTING.md - Contribution guidelines
- SECURITY.md - Security policy
- LICENSE - MIT license (default)
- README.md - Project documentation
- .github/workflows/ - CI/CD pipelines
- .github/ISSUE_TEMPLATE/ - Issue templates
- .github/PULL_REQUEST_TEMPLATE.md - PR template

**Supported Project Types:**

| Type | Flag | Description |
|------|------|-------------|
| Git | `--git` | Standard Git repository |
| Python | `--uv` | Python with uv package manager |
| Node.js | `--node` | Node.js/TypeScript project |
| Go | `--go` | Go project structure |

## Agents

See [Skills & Agents Activation Guide](../reference/skills-agents-activation.md) for detailed activation instructions.

### Java Developer

Expert for modern Java with Streams, Concurrency, and JVM optimization.

**Activation:**

- Automatic: Java/Spring Boot questions, performance optimization
- Manual: "Use java-developer to optimize this code"

**Expertise:**

- Modern Java features (Java 17/21/25 LTS)
- Streams and functional programming
- Virtual Threads and Structured Concurrency
- Spring Boot and reactive programming
- JVM performance tuning
- Enterprise patterns and best practices

**Use proactively for:**

- Java performance tuning
- Concurrent programming challenges
- Complex enterprise solutions
- Spring Boot applications
- JVM optimization
- Legacy code modernization

**Specializations:**

- Virtual Threads (Java 21+)
- Stream API optimization
- CompletableFuture patterns
- Spring WebFlux
- JMH benchmarking
- Records and sealed classes

**Quality Standards:**

- Google Java Style Guide or project standards
- Javadoc for all public APIs
- JUnit 5 with parameterized tests
- Try-with-resources for error handling
- OWASP security guidelines

## Installation

```json
{
  "enabledPlugins": {
    "development@talent-factory": true
  }
}
```

## Use Cases

### Initialize Open Source Project

```bash
# Create new Python project
/init-project --uv --name "my-library"

# Claude:
# - Creates uv-based Python project
# - Adds community standards
# - Sets up GitHub templates
# - Configures CI/CD workflows
```

### Java Development

```bash
# Claude (with java-developer agent):
# - Reviews Spring Boot code proactively
# - Suggests Virtual Threads for concurrency
# - Optimizes Stream operations
# - Improves JVM performance
```

### Performance Optimization

```bash
# Ask about performance
User: "The application is slow processing large datasets"

# Claude (with java-developer):
# - Analyzes data processing code
# - Suggests Stream-based optimizations
# - Recommends parallel processing
# - Creates JMH benchmarks
```

### Reactive Programming

```bash
# Ask about reactive patterns
User: "Implement a REST endpoint with reactive database"

# Claude (with java-developer):
# - Uses Spring WebFlux
# - Implements R2DBC for database
# - Applies backpressure patterns
# - Handles errors reactively
```

## Project Structure

```
development/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── init-project.md
├── agents/
│   └── java-developer.md
└── README.md
```

## Workflow Examples

### Example 1: New Open Source Library

```bash
# 1. Initialize project
/init-project --uv --name "my-library"

# 2. Claude creates:
# - pyproject.toml with metadata
# - src/my_library/ package structure
# - tests/ directory
# - All community standards
# - GitHub Actions CI

# 3. Start development
# Claude (with python-expert from code-quality):
# - Writes idiomatic Python
# - Adds type hints
# - Creates comprehensive tests
```

### Example 2: Java Microservice

```bash
# Working with java-developer proactively

User: "Create a Spring Boot service with Virtual Threads"

# Claude (with java-developer):
# - Creates Spring Boot 3.x project
# - Configures Virtual Threads
# - Implements reactive patterns
# - Adds JUnit 5 tests
# - Includes JMH benchmarks
```

## Best Practices

### Project Initialization

1. **Choose appropriate license** - MIT for maximum adoption
2. **Complete community standards** - All files present
3. **Set up CI/CD early** - Automated testing from start
4. **Document thoroughly** - README with quick start

### Java Development

1. **Use LTS versions** - Java 17, 21, or 25
2. **Prefer immutability** - Records for data classes
3. **Handle errors properly** - Try-with-resources
4. **Test comprehensively** - Parameterized tests
5. **Document APIs** - Complete Javadoc

## Changelog

### Version 1.1.0 (2026-01-28)

- Added `/init-project` command (moved from core plugin)
- Enhanced command with English documentation

### Version 1.0.0 (2026-01-28)

- Initial release
- Added java-developer agent (moved from code-quality plugin)

## Related Plugins

- **[Code Quality](code-quality.md)** - Python and Frontend expert agents
- **[Core Utilities](core.md)** - Plugin development and validation
- **[Git Workflow](git-workflow.md)** - Commit and PR automation

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) file for details.

---

**Made with care by Talent Factory GmbH**
