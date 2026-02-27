# Development Plugin

Expert development agents and project initialization for modern programming languages and frameworks.

## Version 1.3.1

---

## Commands

### init-project

Initialize a new open source project with GitHub best practices and professional Git branching.

**Usage:**
```bash
/development:init-project --git              # Standard Git project
/development:init-project --java             # Java project with Gradle (Kotlin DSL)
/development:init-project --uv               # Python project with uv
/development:init-project --interactive      # Interactive mode
/development:init-project --with-skills      # Skill-based workflow (recommended)
/development:init-project --no-branching     # Only main branch, no develop
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
/development:init-project --with-skills --java --name "my-app"
```

**Features:**
- Automatic project type detection
- Git branching strategy (develop → main)
- Template-based file generation
- Gradle wrapper setup for Java projects

### update-documents

Synchronize documentation between CLAUDE.md, README.md, and docs/.

**Usage:**
```
"Synchronize my documentation"
"Check if docs are in sync"
"Update README from CLAUDE.md"
```

**Features:**
- Automatic sync status analysis
- CLAUDE.md as technical source of truth
- Configurable sync rules via JSON
- Whitespace-tolerant comparison
- Section-based synchronization

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

### 1.3.0

- **New**: `update-documents` skill for documentation synchronization
- **New**: Configurable sync rules between CLAUDE.md, README.md, and docs/
- **New**: Automatic sync status analysis with visual indicators

### 1.2.1

- **Fix**: Java projects now always use Gradle Kotlin DSL (not Maven)
- **Fix**: Initial commit now uses `/git-workflow:commit`
- **Improved**: Clearer step-by-step instructions in skill

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
