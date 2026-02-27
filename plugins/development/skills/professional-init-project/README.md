# Professional Init-Project Skill

Initializes open-source projects with GitHub best practices and a professional Git branching strategy.

## Version 1.0.0

---

## Features

- **Git Branching**: develop → main strategy as default
- **Java/Gradle**: Kotlin DSL with Java 21 toolchain
- **Python/uv**: Modern Python project management
- **Community Standards**: LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY
- **GitHub Templates**: Issue templates, PR template, workflows

---

## Usage

### Via Command

```bash
/development:init-project --with-skills --java --name "my-app"
```

### Direct Script Execution

```bash
cd plugins/development/skills/professional-init-project
python scripts/main.py --type java --name my-app
```

### Options

| Option | Description |
|--------|-------------|
| `--type` | Project type: git, java, uv, node, go, rust |
| `--name` | Project name (kebab-case recommended) |
| `--no-branching` | Main branch only, no develop |
| `--license` | License type: mit, apache2, gpl3, bsd3 |

---

## Project Types

### Java (`--type java`)

- Gradle Kotlin DSL (build.gradle.kts)
- Java 21 toolchain
- JUnit 5 test framework
- Gradle wrapper included

### Python (`--type uv`)

- uv package manager
- pyproject.toml with Ruff configuration
- pytest test framework
- src layout

### Git (`--type git`)

- Minimal setup
- Language detection from existing files
- Appropriate .gitignore

---

## Git Branching Strategy

```
develop (default, active development)
    │
    ├── feature/xyz
    ├── fix/abc
    │
    └── → main (stable releases)
```

- **develop**: Default branch for development
- **main**: Stable, tested releases only
- **feature/**: New features
- **fix/**: Bug fixes

---

## Directory Structure

```
professional-init-project/
├── SKILL.md              # Skill definition
├── README.md             # This file
├── scripts/
│   ├── main.py           # Entry point
│   ├── git_initializer.py
│   └── generators/
│       ├── java_gradle.py
│       ├── python_uv.py
│       └── common.py
├── templates/
│   ├── java/
│   ├── python/
│   └── common/
├── config/
│   └── project_types.json
└── docs/
    ├── branching-strategy.md
    └── troubleshooting.md
```

---

## Configuration

### project_types.json

```json
{
  "java": {
    "build_tool": "gradle-kotlin",
    "java_version": 21,
    "test_framework": "junit5",
    "gradle_version": "8.12"
  },
  "python": {
    "package_manager": "uv",
    "python_version": "3.12",
    "test_framework": "pytest"
  }
}
```

---

## Example Output

```
✓ Git repository initialized
✓ Branch 'develop' created (active)
✓ Project structure generated (Java/Gradle)
✓ Community standards created
✓ GitHub templates created
✓ Initial commit created
✓ Branch 'main' created (in sync with develop)

📁 Project ready: my-app/
   Branch: develop (active)
   Next step: ./gradlew build
```

---

## Related

- [/development:init-project](../../commands/init-project.md) - Command documentation
- [java-developer Agent](../../agents/java-developer.md) - Java development support

---

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE)

---

**Made with care by Talent Factory GmbH**
