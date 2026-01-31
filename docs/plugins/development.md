# Development Plugin

Expert development agents and project initialization with Git branching strategy, Java/Gradle Kotlin DSL, and Python/uv support.

## Version 1.2.1

This plugin provides specialized agents for Java development and commands for initializing open source projects with GitHub best practices and professional Git branching.

---

## Commands

### `/init-project`

Initialize new open source projects with GitHub best practices and Git branching strategy.

**Features:**

- **Git Branching**: develop → main strategy (Standard)
- **Java Support**: Gradle Kotlin DSL with Java 21 toolchain
- **Python Support**: uv-based project structure
- Complete project structure with community standards
- LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
- GitHub templates (issues, PRs, workflows)
- CI/CD ready with GitHub Actions

**Usage:**

```bash
/init-project --git              # Standard Git project
/init-project --java             # Java project with Gradle (Kotlin DSL)
/init-project --uv               # Python project with uv
/init-project --interactive      # Interactive mode
/init-project --name "project"   # With project name
/init-project --with-skills      # Skill-based workflow (recommended)
/init-project --no-branching     # Only main branch, no develop
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
| Git | `--git` | Standard Git repository with develop/main branching |
| Java | `--java` | Java with Gradle Kotlin DSL, Java 21, JUnit 5 |
| Python | `--uv` | Python with uv package manager |
| Node.js | `--node` | Node.js/TypeScript project |
| Go | `--go` | Go project structure |

---

## Skills

### professional-init-project

Skill-based project initialization with enhanced automation.

**Activation:**

- Via command: `/init-project --with-skills`
- Direct: Use scripts in `skills/professional-init-project/scripts/`

**Features:**

- Automatic project type detection
- Git branching strategy (develop → main)
- Template-based file generation
- Gradle wrapper setup for Java projects
- Python/uv configuration with Ruff

**Usage:**

```bash
/init-project --with-skills --java --name "my-app"
```

---

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

---

## Installation

```json
{
  "enabledPlugins": {
    "development@talent-factory": true
  }
}
```

---

## Use Cases

### Initialize Java Project with Gradle

```bash
# Create new Java project
/init-project --java --name "my-app"

# Claude:
# - Creates Gradle Kotlin DSL project
# - Configures Java 21 toolchain
# - Sets up JUnit 5 tests
# - Creates develop and main branches
# - Adds community standards
```

### Initialize Open Source Project

```bash
# Create new Python project
/init-project --uv --name "my-library"

# Claude:
# - Creates uv-based Python project
# - Adds community standards
# - Sets up GitHub templates
# - Configures CI/CD workflows
# - Uses develop → main branching
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

---

## Project Structure

```
development/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── init-project.md
├── agents/
│   └── java-developer.md
├── skills/
│   └── professional-init-project/
│       ├── SKILL.md
│       ├── README.md
│       ├── scripts/
│       │   ├── main.py
│       │   ├── git_initializer.py
│       │   └── generators/
│       ├── templates/
│       └── config/
└── README.md
```

---

## Best Practices

### Git Branching Strategy

- **develop**: Active development, default branch
- **main**: Stable releases, protected
- **feature/xxx**: New features, branch from develop
- **fix/xxx**: Bug fixes, branch from develop

### Project Initialization

1. **Choose appropriate license** - MIT for maximum adoption
2. **Complete community standards** - All files present
3. **Set up CI/CD early** - Automated testing from start
4. **Document thoroughly** - README with quick start
5. **Use develop → main** - Professional branching strategy

### Java Development

1. **Use LTS versions** - Java 17, 21, or 25
2. **Prefer Gradle Kotlin DSL** - Modern, type-safe build configuration
3. **Handle errors properly** - Try-with-resources
4. **Test comprehensively** - Parameterized tests
5. **Document APIs** - Complete Javadoc

---

## Changelog

### Version 1.2.1 (2026-01-31)

- **Fix**: Java-Projekte verwenden jetzt IMMER Gradle Kotlin DSL (nicht Maven)
- **Fix**: Initialer Commit verwendet jetzt `/git-workflow:commit`
- **Improved**: Klarere Schritt-für-Schritt-Anweisungen im Skill

### Version 1.2.0 (2026-01-31)

- **New**: `--java` parameter for Java/Gradle Kotlin DSL projects
- **New**: `--with-skills` parameter for skill-based workflow
- **New**: `--no-branching` parameter to opt-out of develop/main strategy
- **New**: professional-init-project skill
- **Changed**: Git branching now uses develop → main by default
- **Changed**: Java projects use Gradle Kotlin DSL instead of Maven

### Version 1.1.0 (2026-01-28)

- Added `/init-project` command (moved from core plugin)
- Enhanced command with English documentation

### Version 1.0.0 (2026-01-28)

- Initial release
- Added java-developer agent (moved from code-quality plugin)

---

## Related Plugins

- **[Code Quality](code-quality.md)** - Python and Frontend expert agents
- **[Core Utilities](core.md)** - Plugin development and validation
- **[Git Workflow](git-workflow.md)** - Commit and PR automation

---

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) file for details.

---

**Made with care by Talent Factory GmbH**
