#!/usr/bin/env python3
"""Python/uv project generator."""

import subprocess
from pathlib import Path


class PythonUvGenerator:
    """Generates Python project with uv package manager."""

    def __init__(
        self,
        project_path: Path,
        project_name: str,
        author: str = "Author",
        email: str = "author@example.com",
        python_version: str = "3.12",
    ):
        self.project_path = project_path
        self.project_name = project_name
        self.package_name = project_name.replace("-", "_").lower()
        self.author = author
        self.email = email
        self.python_version = python_version

    def generate_all(self) -> bool:
        """Generate all Python/uv files.

        Returns:
            True if successful, False otherwise.
        """
        try:
            # Try using uv init first
            if self._try_uv_init():
                self._extend_pyproject()
                self._generate_gitignore()
                self._create_test_structure()
                print("✓ Projektstruktur generiert (Python/uv)")
                return True

            # Fallback: manual creation
            self._create_directories()
            self._generate_pyproject()
            self._generate_gitignore()
            self._generate_init_py()
            self._create_test_structure()
            print("✓ Projektstruktur generiert (Python/uv)")
            return True
        except Exception as e:
            print(f"❌ Failed to generate Python project: {e}")
            return False

    def _try_uv_init(self) -> bool:
        """Try to initialize project using uv."""
        try:
            # Check if uv is available
            subprocess.run(["uv", "--version"], capture_output=True, check=True)

            # Initialize with uv in the project directory
            result = subprocess.run(
                ["uv", "init", "--name", self.project_name, str(self.project_path)],
                cwd=self.project_path.parent,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _create_directories(self) -> None:
        """Create project directory structure."""
        dirs = [
            f"src/{self.package_name}",
            "tests",
            "docs",
        ]
        for dir_path in dirs:
            (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)

    def _generate_pyproject(self) -> None:
        """Generate pyproject.toml file."""
        content = f"""[project]
name = "{self.project_name}"
version = "0.1.0"
description = "A brief description of your project"
authors = [
    {{ name = "{self.author}", email = "{self.email}" }}
]
readme = "README.md"
license = {{ file = "LICENSE" }}
requires-python = ">={self.python_version}"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: {self.python_version}",
]

[project.urls]
Homepage = "https://github.com/user/{self.project_name}"
Documentation = "https://github.com/user/{self.project_name}#readme"
Repository = "https://github.com/user/{self.project_name}"
Issues = "https://github.com/user/{self.project_name}/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{self.package_name}"]

[tool.ruff]
line-length = 100
target-version = "py{self.python_version.replace(".", "")}"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.mypy]
python_version = "{self.python_version}"
strict = true
"""
        (self.project_path / "pyproject.toml").write_text(content)

    def _extend_pyproject(self) -> None:
        """Extend existing pyproject.toml with additional configuration."""
        pyproject_path = self.project_path / "pyproject.toml"
        if not pyproject_path.exists():
            return

        content = pyproject_path.read_text()

        # Add ruff configuration if not present
        if "[tool.ruff]" not in content:
            content += f"""
[tool.ruff]
line-length = 100
target-version = "py{self.python_version.replace(".", "")}"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
"""

        # Add pytest configuration if not present
        if "[tool.pytest.ini_options]" not in content:
            content += """
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
"""

        pyproject_path.write_text(content)

    def _generate_gitignore(self) -> None:
        """Generate .gitignore for Python."""
        content = """# Virtual Environment
.venv/
venv/
env/
.python-version

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg
*.egg-info/
dist/
build/
eggs/
.eggs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# mypy
.mypy_cache/

# ruff
.ruff_cache/

# Local configuration
.env
.env.local
*.local
"""
        (self.project_path / ".gitignore").write_text(content)

    def _generate_init_py(self) -> None:
        """Generate __init__.py file."""
        content = f'''"""
{self.project_name}

A brief description of your project.
"""

__version__ = "0.1.0"
'''
        init_path = self.project_path / f"src/{self.package_name}/__init__.py"
        init_path.write_text(content)

    def _create_test_structure(self) -> None:
        """Create test directory and sample test."""
        tests_dir = self.project_path / "tests"
        tests_dir.mkdir(exist_ok=True)

        # Create __init__.py
        (tests_dir / "__init__.py").write_text("")

        # Create sample test
        test_content = f'''"""Tests for {self.package_name}."""

import {self.package_name}


def test_version():
    """Test that version is defined."""
    assert hasattr({self.package_name}, "__version__")
    assert isinstance({self.package_name}.__version__, str)
'''
        (tests_dir / f"test_{self.package_name}.py").write_text(test_content)
