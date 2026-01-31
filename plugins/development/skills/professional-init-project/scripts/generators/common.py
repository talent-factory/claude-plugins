#!/usr/bin/env python3
"""Common file generator for community standards and GitHub templates."""

from datetime import datetime
from pathlib import Path


class CommonGenerator:
    """Generates common files for all project types."""

    def __init__(self, project_path: Path, project_name: str, author: str = "Author"):
        self.project_path = project_path
        self.project_name = project_name
        self.author = author
        self.year = datetime.now().year

    def generate_all(self, license_type: str = "mit") -> bool:
        """Generate all common files.

        Args:
            license_type: License type (mit, apache2, gpl3, bsd3)

        Returns:
            True if successful, False otherwise.
        """
        try:
            self._generate_license(license_type)
            self._generate_readme()
            self._generate_contributing()
            self._generate_code_of_conduct()
            self._generate_security()
            self._generate_github_templates()
            print("✓ Community Standards erstellt")
            print("✓ GitHub Templates erstellt")
            return True
        except Exception as e:
            print(f"❌ Failed to generate common files: {e}")
            return False

    def _generate_license(self, license_type: str) -> None:
        """Generate LICENSE file."""
        licenses = {
            "mit": self._mit_license(),
            "apache2": self._apache2_license(),
            "gpl3": self._gpl3_license(),
            "bsd3": self._bsd3_license(),
        }
        content = licenses.get(license_type, self._mit_license())
        (self.project_path / "LICENSE").write_text(content)

    def _mit_license(self) -> str:
        return f"""MIT License

Copyright (c) {self.year} {self.author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

    def _apache2_license(self) -> str:
        return f"""                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

Copyright {self.year} {self.author}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

    def _gpl3_license(self) -> str:
        return f"""GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) {self.year} {self.author}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

    def _bsd3_license(self) -> str:
        return f"""BSD 3-Clause License

Copyright (c) {self.year}, {self.author}

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

    def _generate_readme(self) -> None:
        """Generate README.md file."""
        content = f"""# {self.project_name}

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A brief description of your project.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
# Installation instructions
```

## Quick Start

```bash
# Quick start example
```

## Documentation

- [API Reference](docs/api.md)
- [Contributing Guide](CONTRIBUTING.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: Questions and community
- Security: See [SECURITY.md](SECURITY.md)
"""
        (self.project_path / "README.md").write_text(content)

    def _generate_contributing(self) -> None:
        """Generate CONTRIBUTING.md file."""
        content = """# Contributing

Thank you for your interest in contributing!

## Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `./gradlew test` or `pytest`
5. Commit your changes: `git commit -m "feat: Add your feature"`
6. Push to your fork: `git push origin feature/your-feature`
7. Create a Pull Request

## Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance

## Code Style

- Follow existing code style
- Add tests for new features
- Update documentation as needed

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Ensure all tests pass
3. Request review from maintainers
4. Merge after approval

## Questions?

Open an issue or start a discussion.
"""
        (self.project_path / "CONTRIBUTING.md").write_text(content)

    def _generate_code_of_conduct(self) -> None:
        """Generate CODE_OF_CONDUCT.md file."""
        content = """# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone.

## Our Standards

Examples of behavior that contributes to a positive environment:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior:

* The use of sexualized language or imagery
* Trolling, insulting or derogatory comments
* Public or private harassment
* Publishing others' private information without permission
* Other conduct which could reasonably be considered inappropriate

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders. All complaints will be reviewed and
investigated promptly and fairly.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.1, available at
https://www.contributor-covenant.org/version/2/1/code_of_conduct.html

[homepage]: https://www.contributor-covenant.org
"""
        (self.project_path / "CODE_OF_CONDUCT.md").write_text(content)

    def _generate_security(self) -> None:
        """Generate SECURITY.md file."""
        content = f"""# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public issue
2. Email the maintainers directly or use GitHub's private vulnerability reporting
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work on a fix.

## Security Updates

Security updates will be released as patch versions and announced in:
- GitHub Security Advisories
- Release notes
"""
        (self.project_path / "SECURITY.md").write_text(content)

    def _generate_github_templates(self) -> None:
        """Generate GitHub issue and PR templates."""
        github_dir = self.project_path / ".github"
        issue_dir = github_dir / "ISSUE_TEMPLATE"
        issue_dir.mkdir(parents=True, exist_ok=True)

        # Bug report template
        bug_report = """name: Bug Report
description: Report a bug or unexpected behavior
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!

  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear description of the bug
      placeholder: What happened?
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this issue?
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: Version, OS, etc.
      placeholder: |
        - Version: 0.1.0
        - OS: macOS 14.0
    validations:
      required: false
"""
        (issue_dir / "bug_report.yml").write_text(bug_report)

        # Feature request template
        feature_request = """name: Feature Request
description: Suggest a new feature
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting a feature!

  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: What problem does this solve?
      placeholder: I'm always frustrated when...
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How would you like this to work?
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Any alternative solutions you've considered?
    validations:
      required: false
"""
        (issue_dir / "feature_request.yml").write_text(feature_request)

        # Config
        config = """blank_issues_enabled: false
contact_links:
  - name: Security Issues
    url: https://github.com/user/repo/security/advisories/new
    about: Report security vulnerabilities privately
  - name: Questions
    url: https://github.com/user/repo/discussions
    about: Ask questions and discuss ideas
"""
        (issue_dir / "config.yml").write_text(config)

        # PR template
        pr_template = """## Description

<!-- What does this PR do? -->

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist

- [ ] Tests pass locally
- [ ] Code follows project style
- [ ] Documentation updated (if needed)
- [ ] No breaking changes (or documented)

## Related Issues

<!-- Link related issues: Fixes #123 -->
"""
        (github_dir / "PULL_REQUEST_TEMPLATE.md").write_text(pr_template)
