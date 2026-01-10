#!/usr/bin/env python3
"""Python project validator (Ruff, Black, pytest, mypy)."""

from typing import List
from .base_validator import BaseValidator, ValidationResult


class PythonValidator(BaseValidator):
    """Validator for Python projects."""

    def detect(self) -> bool:
        """Detect if this is a Python project."""
        return (
            self.file_exists("pyproject.toml") or
            self.file_exists("requirements.txt") or
            self.file_exists("setup.py") or
            self.file_exists("Pipfile")
        )

    def validate(self) -> List[ValidationResult]:
        """Run Python-specific validation checks."""
        self.results = []

        # 1. Ruff linting (fast)
        if self.tool_exists("ruff"):
            result = self.run_command(
                ["ruff", "check", "."],
                check_name="Ruff Linting",
                success_message="Keine Linting-Fehler",
                error_message="Linting-Fehler gefunden"
            )
            self.results.append(result)

        # 2. Black formatting check
        if self.tool_exists("black"):
            result = self.run_command(
                ["black", "--check", "."],
                check_name="Black Formatting",
                success_message="Code korrekt formatiert",
                error_message="Formatierungs-Fehler gefunden"
            )
            self.results.append(result)

        # 3. isort import sorting
        if self.tool_exists("isort"):
            result = self.run_command(
                ["isort", "--check-only", "."],
                check_name="isort Import Sorting",
                success_message="Imports korrekt sortiert",
                error_message="Import-Reihenfolge inkorrekt"
            )
            self.results.append(result)

        # 4. mypy type checking (if configured)
        if self.tool_exists("mypy") and self._has_mypy_config():
            result = self.run_command(
                ["mypy", "."],
                check_name="mypy Type Checking",
                success_message="Keine Type-Fehler",
                error_message="Type-Fehler gefunden"
            )
            self.results.append(result)

        # 5. pytest (unless skipped)
        if not self.skip_tests and self.tool_exists("pytest"):
            result = self.run_command(
                ["pytest", "-v", "--tb=short"],
                check_name="pytest",
                success_message="Alle Tests bestanden",
                error_message="Test-Fehler gefunden"
            )
            self.results.append(result)

        # Warn if no validation tools found
        if not self.results:
            self.results.append(
                ValidationResult(
                    name="Python Tools",
                    passed=False,
                    message="Keine Validierungs-Tools gefunden",
                    details="Installiere ruff, black, pytest für Pre-Commit-Checks"
                )
            )

        return self.results

    def _has_mypy_config(self) -> bool:
        """Check if mypy is configured."""
        import os

        # Check for mypy.ini
        if os.path.exists(os.path.join(self.project_root, "mypy.ini")):
            return True

        # Check for [tool.mypy] in pyproject.toml
        pyproject_path = os.path.join(self.project_root, "pyproject.toml")
        if os.path.exists(pyproject_path):
            try:
                with open(pyproject_path, 'r') as f:
                    return '[tool.mypy]' in f.read()
            except:
                pass

        return False
