#!/usr/bin/env python3
"""Base validator class for pre-commit checks."""

import subprocess
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple


class ValidationResult:
    """Result of a validation check."""

    def __init__(self, name: str, passed: bool, message: str = "", details: str = ""):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details

    def __repr__(self) -> str:
        status = "✓" if self.passed else "✗"
        return f"{status} {self.name}: {self.message}"


class BaseValidator(ABC):
    """Base class for project validators."""

    def __init__(self, project_root: str, skip_tests: bool = False):
        self.project_root = project_root
        self.skip_tests = skip_tests
        self.results: List[ValidationResult] = []

    @abstractmethod
    def detect(self) -> bool:
        """Detect if this validator applies to the project."""
        pass

    @abstractmethod
    def validate(self) -> List[ValidationResult]:
        """Run all validation checks."""
        pass

    def run_command(
        self,
        cmd: List[str],
        check_name: str,
        success_message: str = "Erfolgreich",
        error_message: str = "Fehler gefunden"
    ) -> ValidationResult:
        """
        Run a shell command and return ValidationResult.

        Args:
            cmd: Command to run as list
            check_name: Name of the check
            success_message: Message on success
            error_message: Message on error

        Returns:
            ValidationResult with command output
        """
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes max
            )

            if result.returncode == 0:
                return ValidationResult(
                    name=check_name,
                    passed=True,
                    message=success_message,
                    details=result.stdout
                )
            else:
                return ValidationResult(
                    name=check_name,
                    passed=False,
                    message=error_message,
                    details=result.stderr or result.stdout
                )

        except subprocess.TimeoutExpired:
            return ValidationResult(
                name=check_name,
                passed=False,
                message="Timeout (>5min)",
                details="Command exceeded 5 minute timeout"
            )
        except FileNotFoundError:
            return ValidationResult(
                name=check_name,
                passed=False,
                message="Tool nicht gefunden",
                details=f"Command '{cmd[0]}' not found in PATH"
            )
        except Exception as e:
            return ValidationResult(
                name=check_name,
                passed=False,
                message="Unerwarteter Fehler",
                details=str(e)
            )

    def tool_exists(self, tool: str) -> bool:
        """Check if a tool exists in PATH."""
        try:
            subprocess.run(
                ["which", tool],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def file_exists(self, filename: str) -> bool:
        """Check if file exists in project root."""
        import os
        return os.path.isfile(os.path.join(self.project_root, filename))

    def get_summary(self) -> Tuple[int, int]:
        """Get summary of validation results (passed, total)."""
        if not self.results:
            return 0, 0
        passed = sum(1 for r in self.results if r.passed)
        return passed, len(self.results)
