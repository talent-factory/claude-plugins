# Development Plugin

Expert development agents and project initialization for modern programming languages and frameworks.

## Version 1.2.0

---

## Commands

### init-project

Initialize a new open source project with GitHub best practices and professional Git branching.

**Usage:**
```bash
/init-project --git              # Standard Git project
/init-project --java             # Java project with Gradle (Kotlin DSL)
/init-project --uv               # Python project with uv
/init-project --interactive      # Interactive mode
/init-project --with-skills      # Skill-based workflow (recommended)
/init-project --no-branching     # Only main branch, no develop
```

**Features:**
- **Git Branching**: develop → main strategy (Standard)
- **Java Support**: Gradle Kotlin DSL with Java 21 toolchain
- **Python Support**: uv-based project structure
- Community standards (LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY)
- GitHub templates (issues, PRs, workflows)
- CI/CD ready with GitHub Actions

---

## Skills

### professional-init-project

Skill-based project initialization with enhanced automation.

**Usage:**
```bash
/init-project --with-skills --java --name "my-app"
```

**Features:**
- Automatic project type detection
- Git branching strategy (develop → main)
- Template-based file generation
- Gradle wrapper setup for Java projects

---

## Agents

### java-developer

Master modern Java with Streams, Concurrency, and JVM optimization.

**Expertise:**
- Modern Java features (Java 17/21/25 LTS)
- Spring Boot and reactive programming
- Virtual Threads and Structured Concurrency
- Performance tuning and JVM optimization
- Enterprise patterns and best practices

**Use when:**
- Implementing Java applications with modern features
- Optimizing performance for large-scale data processing
- Building reactive APIs with Spring WebFlux
- Handling concurrent programming challenges
- Refactoring legacy code to modern standards

---

## Installation

Add to your Claude Code settings:

```json
{
  "enabledPlugins": {
    "development@talent-factory": true
  }
}
```

---

## Changelog

### 1.2.0

- **New**: `--java` parameter for Java/Gradle Kotlin DSL projects
- **New**: `--with-skills` parameter for skill-based workflow
- **New**: `--no-branching` parameter to opt-out of develop/main strategy
- **New**: professional-init-project skill
- **Changed**: Git branching now uses develop → main by default
- **Changed**: Java projects use Gradle Kotlin DSL instead of Maven

### 1.1.0

- Initial release with init-project command
- java-developer agent

---

## Related Plugins

- **[Git Workflow](../git-workflow/README.md)** - Professional commit and PR automation
- **[Code Quality](../code-quality/README.md)** - Python and Frontend expert agents

---

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE)

---

**Made with care by Talent Factory GmbH**
