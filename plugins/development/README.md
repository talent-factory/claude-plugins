# Development Plugin

Expert development agents and project initialization for modern programming languages and frameworks.

## Version 1.1.0

## Commands

### init-project

Initialize a new open source project with GitHub best practices.

**Usage:**
```bash
/init-project --git              # Standard Git project
/init-project --uv               # Python project with uv
/init-project --interactive      # Interactive mode
```

**Features:**
- Community standards (LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY)
- GitHub templates (issues, PRs, workflows)
- Language-specific setup (Python, Node.js, Go, Java)
- CI/CD ready with GitHub Actions

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

## Installation

Add to your Claude Code settings:

```json
{
  "enabledPlugins": {
    "development@talent-factory": true
  }
}
```

