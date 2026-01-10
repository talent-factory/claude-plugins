#!/usr/bin/env python3
"""React/Node.js project validator (ESLint, Prettier, TypeScript)."""

import json
import os
from typing import List, Optional
from .base_validator import BaseValidator, ValidationResult


class ReactValidator(BaseValidator):
    """Validator for React/Node.js projects."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.package_manager: Optional[str] = None

    def detect(self) -> bool:
        """Detect if this is a React/Node.js project."""
        if not self.file_exists("package.json"):
            return False

        # Check if it's a React project
        package_json_path = os.path.join(self.project_root, "package.json")
        try:
            with open(package_json_path, 'r') as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                return any(key in deps for key in ['react', 'next', 'vue', 'svelte'])
        except:
            return False

    def validate(self) -> List[ValidationResult]:
        """Run React/Node.js-specific validation checks."""
        self.results = []

        # Detect package manager
        self._detect_package_manager()

        # 1. ESLint
        if self._has_eslint():
            result = self.run_command(
                [self.package_manager, "run", "lint"] if self.package_manager != "npx"
                else ["npx", "eslint", "."],
                check_name="ESLint",
                success_message="Keine Linting-Fehler",
                error_message="Linting-Fehler gefunden"
            )
            self.results.append(result)

        # 2. Prettier check
        if self.tool_exists("prettier"):
            result = self.run_command(
                ["npx", "prettier", "--check", "."],
                check_name="Prettier",
                success_message="Code korrekt formatiert",
                error_message="Formatierungs-Fehler gefunden"
            )
            self.results.append(result)

        # 3. TypeScript type checking
        if self.file_exists("tsconfig.json"):
            result = self.run_command(
                ["npx", "tsc", "--noEmit"],
                check_name="TypeScript",
                success_message="Keine Type-Fehler",
                error_message="Type-Fehler gefunden"
            )
            self.results.append(result)

        # 4. Tests (unless skipped)
        if not self.skip_tests and self._has_test_script():
            result = self.run_command(
                [self.package_manager, "run", "test", "--", "--run"],
                check_name="Tests",
                success_message="Alle Tests bestanden",
                error_message="Test-Fehler gefunden"
            )
            self.results.append(result)

        # 5. Build (to verify production readiness)
        if self._has_build_script():
            result = self.run_command(
                [self.package_manager, "run", "build"],
                check_name="Build",
                success_message="Build erfolgreich",
                error_message="Build-Fehler gefunden"
            )
            self.results.append(result)

        return self.results

    def _detect_package_manager(self):
        """Detect which package manager is used."""
        if self.file_exists("pnpm-lock.yaml"):
            self.package_manager = "pnpm"
        elif self.file_exists("yarn.lock"):
            self.package_manager = "yarn"
        elif self.file_exists("bun.lockb"):
            self.package_manager = "bun"
        else:
            self.package_manager = "npm"

    def _has_eslint(self) -> bool:
        """Check if ESLint is configured."""
        return (
            self.file_exists(".eslintrc.js") or
            self.file_exists(".eslintrc.json") or
            self.file_exists(".eslintrc.yml") or
            self.file_exists("eslint.config.js") or
            self._has_script("lint")
        )

    def _has_script(self, script_name: str) -> bool:
        """Check if package.json has a specific script."""
        package_json_path = os.path.join(self.project_root, "package.json")
        try:
            with open(package_json_path, 'r') as f:
                data = json.load(f)
                return script_name in data.get('scripts', {})
        except:
            return False

    def _has_test_script(self) -> bool:
        """Check if package.json has a test script."""
        return self._has_script("test")

    def _has_build_script(self) -> bool:
        """Check if package.json has a build script."""
        return self._has_script("build")
