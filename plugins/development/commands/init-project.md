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

Creates a new open source project with complete GitHub infrastructure and community standards.

## Usage

```bash
# Standard Git project
/init-project --git

# Python project with uv
/init-project --uv

# With project name
/init-project --git --name "my-awesome-project"

# Interactive mode
/init-project --interactive
```

## Features

- **Community Standards**: LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
- **GitHub Templates**: Issue templates, PR template, security advisories
- **Documentation**: README.md with badges, structure, and best practices
- **Git Setup**: .gitignore, .gitattributes, branch protection recommendations
- **Python Support**: uv-based project structure (optional)
- **CI/CD Ready**: GitHub Actions workflows

## Process

### 1. Determine Project Type

**With `--interactive`**:

- Ask project type: Git, Python (uv), Node.js, Go, Rust, Java
- Ask project name
- Ask license type: MIT, Apache 2.0, GPL-3.0, BSD-3-Clause
- Ask primary language

**With `--git`**:

- Standard Git project
- Detect language from existing files

**With `--uv`**:

- Check if `uv` is installed
- If not: `pip install uv --break-system-packages`
- Run `uv init`
- Extend with GitHub standards

### 2. Base Initialization

**Git Project** (`--git`):
```bash
git init
git branch -M main
git commit --allow-empty -m "Initial commit"
```

**Python Project** (`--uv`):
```bash
# Install uv if needed
command -v uv || pip install uv --break-system-packages

# Initialize project
uv init [project_name]
cd [project_name]

# Create virtual environment
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate (Windows)
```

### 3. Create Community Standards

**LICENSE** (MIT as default):
```text
MIT License

Copyright (c) [YEAR] [AUTHOR]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Standard MIT License Text]
```

**CONTRIBUTING.md**:

- Feature branch workflow
- PR process
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

### 4. Create GitHub Templates

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

### 5. Create README.md

**Structure**:
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

### 6. Create .gitignore

**Python**:
```gitignore
# Virtual Environment
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
```

**Node.js**:
```gitignore
node_modules/
npm-debug.log*
.env
dist/
build/
```

### 7. Create Initial Commits

**Initial Commit**:
```bash
git add .
git commit -m "feat: Initial open source setup

- MIT License
- Community standards (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY)
- GitHub templates (issues, PRs)
- README with badges and structure
- .gitignore for [Language]
- CI/CD workflows
"
```

### 8. Create GitHub Repository (optional)

```bash
# With gh CLI
gh repo create [name] --public --description "[description]"
gh repo edit --enable-issues --enable-discussions
gh repo edit --enable-wiki=false

# Add remote
git remote add origin https://github.com/[user]/[name].git
git push -u origin main
```

## Language-Specific Setups

### Python (uv)

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

**pyproject.toml** (extended):
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
authors = [{name = "Author", email = "email@example.com"}]
readme = "README.md"
license = {file = "LICENSE"}
requires-python = ">=3.11"

[project.urls]
Homepage = "https://github.com/user/repo"
Documentation = "https://github.com/user/repo#readme"
Repository = "https://github.com/user/repo"
Issues = "https://github.com/user/repo/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### JavaScript/TypeScript

**package.json** (extended):
```json
{
  "name": "project-name",
  "version": "0.1.0",
  "description": "Project description",
  "license": "MIT",
  "author": "Author <email@example.com>",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo"
  },
  "bugs": "https://github.com/user/repo/issues",
  "homepage": "https://github.com/user/repo#readme"
}
```

### Go

**go.mod and Structure**:
```text
project_name/
├── cmd/
│   └── main.go
├── internal/
├── pkg/
├── README.md
├── LICENSE
├── go.mod
└── .github/
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

### README Best Practices

**Good practices**:

- Badges show status at a glance
- Quick start under 5 minutes
- Screenshots/GIFs for UI projects
- Clear installation steps
- Links to detailed documentation

**Avoid**:

- Missing or outdated badges
- Missing installation instructions
- No examples
- Broken links

### Contributing Guidelines

**Essentials**:

- Branch naming: `feature/`, `fix/`, `docs/`
- PR process with review requirements
- Code style (linter, formatter)
- Test coverage requirements
- Commit message format

## Troubleshooting

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
- [uv Documentation](https://docs.astral.sh/uv/)
