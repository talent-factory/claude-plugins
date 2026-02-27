---
description: Initialize a new open source project with GitHub best practices
allowed-tools:
  - Bash
  - Write
  - Read
  - Edit
  - Glob
---

# Initialize Open Source Project

Creates a new open source project with complete GitHub infrastructure, community standards, and professional Git branching strategy.

## Usage

```bash
# Standard Git project
/development:init-project --git

# Java project with Gradle (Kotlin DSL)
/development:init-project --java

# Python project with uv
/development:init-project --uv

# With project name
/development:init-project --git --name "my-awesome-project"

# Interactive mode
/development:init-project --interactive

# Using skill-based workflow (recommended)
/development:init-project --with-skills

# Without develop/main branching (only main)
/development:init-project --git --no-branching
```

## Features

- **Git Branching**: develop → main strategy (Standard)
- **Community Standards**: LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
- **GitHub Templates**: Issue templates, PR template, security advisories
- **Documentation**: README.md with badges, structure, and best practices
- **Git Setup**: .gitignore, .gitattributes, branch protection recommendations
- **Java Support**: Gradle Kotlin DSL with Java 21 toolchain
- **Python Support**: uv-based project structure
- **CI/CD Ready**: GitHub Actions workflows

## Workflow

### With `--with-skills` Option

When `--with-skills` is used, the **professional-init-project skill** is activated.

**IMPORTANT RULES (for --with-skills AND standard workflow):**

1. **Java projects ALWAYS use Gradle Kotlin DSL** - NEVER Maven!
2. **Initial commit MUST be made via `/git-workflow:commit`** - NEVER use `git commit` directly!
3. **Git branching: develop -> main** is the default

**Skill execution:**
- Invoke the `development:professional-init-project` skill
- The skill guides through all steps of project initialization
- At the end, `/git-workflow:commit` is invoked for the initial commit

**Skill-Details**: Siehe [professional-init-project SKILL.md](../skills/professional-init-project/SKILL.md)

### Standard Workflow (ohne `--with-skills`)

### 1. Determine Project Type

**With `--interactive`**:

- Ask project type: Git, Java (Gradle), Python (uv), Node.js, Go, Rust
- Ask project name
- Ask license type: MIT, Apache 2.0, GPL-3.0, BSD-3-Clause
- Ask primary language

**With `--git`**:

- Standard Git project
- Detect language from existing files

**With `--java`**:

- Java project with Gradle Kotlin DSL
- Java 21 toolchain configuration
- JUnit 5 test setup

**With `--uv`**:

- Check if `uv` is installed
- If not: `pip install uv --break-system-packages`
- Run `uv init`
- Extend with GitHub standards

### 2. Git Initialization (Standard: develop → main)

**Standard Branching** (default):
```bash
# Initialize repository
git init

# Create and switch to develop branch
git checkout -b develop

# ... create project files ...

# Initial commit on develop - IMPORTANT: Use /git-workflow:commit!
/git-workflow:commit

# Create main branch from develop (synchronized)
git branch main

# Stay on develop for further development
```

**Without Branching** (`--no-branching`):
```bash
git init
git branch -M main
# Use /git-workflow:commit for the initial commit!
/git-workflow:commit
```

### 3. Java Project (`--java`)

**Gradle Initialization**:
```bash
# Create Gradle wrapper (if gradle available)
gradle wrapper --gradle-version 8.12

# Or download wrapper manually
```

**build.gradle.kts**:
```kotlin
plugins {
    java
    application
}

group = "com.example"
version = "0.1.0"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.11.4"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

application {
    mainClass = "com.example.App"
}

tasks.test {
    useJUnitPlatform()
    testLogging {
        events("passed", "skipped", "failed")
    }
}
```

**settings.gradle.kts**:
```kotlin
rootProject.name = "project-name"
```

**Project Structure**:
```text
project-name/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/App.java
│   │   └── resources/
│   └── test/
│       ├── java/
│       │   └── com/example/AppTest.java
│       └── resources/
├── .gitignore
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── SECURITY.md
```

**.gitignore** (Java/Gradle):
```gitignore
# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar

# IDE
.idea/
*.iml
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
```

### 4. Python Project (`--uv`)

```bash
# Install uv if needed
command -v uv || pip install uv --break-system-packages

# Initialize project
uv init [project_name]
cd [project_name]

# Create virtual environment
uv venv
source .venv/bin/activate
```

**Project Structure**:
```text
project_name/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
├── src/
│   └── project_name/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── docs/
├── .gitignore
├── pyproject.toml
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── SECURITY.md
```

### 5. Create Community Standards

**LICENSE** (MIT as default):
```text
MIT License

Copyright (c) [YEAR] [AUTHOR]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...

[Standard MIT License Text]
```

**CONTRIBUTING.md**:

- Feature branch workflow (feature/, fix/, docs/)
- PR process with review requirements
- Code standards
- Testing requirements

**CODE_OF_CONDUCT.md**:

- Contributor Covenant 2.1
- Contact information
- Enforcement guidelines

**SECURITY.md**:

- Supported versions
- Reporting process
- Security advisories link

### 6. Create GitHub Templates

**.github/ISSUE_TEMPLATE/**:

- `bug_report.yml` - Structured bug report form
- `feature_request.yml` - Feature request with prioritization
- `documentation.yml` - Documentation issues
- `config.yml` - Links to discussions/security

**.github/PULL_REQUEST_TEMPLATE.md**:

- Description
- Change type (feature, fix, docs, etc.)
- Testing checklist
- Breaking changes

**.github/workflows/** (optional):

- `ci.yml` - Base CI/CD pipeline
- `lint.yml` - Code quality checks

### 7. Create README.md

```markdown
# [Project Name]

[Badges: License, Platform, CI Status, etc.]

[1-2 sentence description]

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

[Language-specific installation]

## Quick Start

[Minimal example]

## Documentation

- [Link to Docs]
- [Link to API Reference]

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[License Type] - See [LICENSE](LICENSE)

## Support

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: Questions and community
- Security: See [SECURITY.md](SECURITY.md)
```

### 8. Create Initial Commit

**IMPORTANT: ALWAYS use `/git-workflow:commit` for the initial commit!**

```bash
# Stage all files
git add .

# Create commit using the professional commit workflow
/git-workflow:commit

# After commit: Create main branch (synchronized with develop)
git branch main
```

The `/git-workflow:commit` command will:
- Run pre-commit checks (if relevant)
- Use Emoji Conventional Commit format
- Generate a professional commit message

### 9. Create GitHub Repository (optional)

```bash
# With gh CLI
gh repo create [name] --public --description "[description]"
gh repo edit --enable-issues --enable-discussions
gh repo edit --enable-wiki=false

# Push both branches
git push -u origin develop main

# Set develop as default branch
gh repo edit --default-branch develop
```

## Best Practices

### License Selection

| License | Use Case | Commercial Use | Copyleft |
|---------|----------|----------------|----------|
| **MIT** | Permissive, maximum freedom | Yes | No |
| **Apache 2.0** | Permissive + patent grant | Yes | No |
| **GPL-3.0** | Strong copyleft | Yes (with restrictions) | Yes |
| **BSD-3-Clause** | Permissive + name protection | Yes | No |

**Recommendation**: MIT for maximum adoption, Apache 2.0 for patent protection

### Git Branching Strategy

- **develop**: Active development, default branch
- **main**: Stable releases, protected
- **feature/xxx**: New features, branch from develop
- **fix/xxx**: Bug fixes, branch from develop

### README Best Practices

- Badges show status at a glance
- Quick start under 5 minutes
- Screenshots/GIFs for UI projects
- Clear installation steps
- Links to detailed documentation

## Troubleshooting

**Gradle not found**:
```bash
# macOS
brew install gradle

# Or use wrapper (recommended)
# The command will create the wrapper for you
```

**uv not found**:
```bash
pip install uv --break-system-packages
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**gh CLI not available**:
```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# Windows
winget install GitHub.cli
```

**Git not configured**:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Related Commands

- `/git-workflow:commit` - Create professional commits
- `/git-workflow:create-pr` - Create pull requests with template
- `/core:run-ci` - Run CI checks

## References

- [GitHub Community Standards](https://docs.github.com/en/communities)
- [Contributor Covenant](https://www.contributor-covenant.org/)
- [Choose a License](https://choosealicense.com/)
- [Gradle Kotlin DSL](https://docs.gradle.org/current/userguide/kotlin_dsl.html)
- [uv Documentation](https://docs.astral.sh/uv/)
