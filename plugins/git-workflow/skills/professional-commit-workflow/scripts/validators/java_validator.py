#!/usr/bin/env python3
"""Java project validator (Maven, Gradle, Spring Boot)."""

from typing import List
from .base_validator import BaseValidator, ValidationResult


class JavaValidator(BaseValidator):
    """Validator for Java projects."""

    def detect(self) -> bool:
        """Detect if this is a Java project."""
        return (
            self.file_exists("pom.xml") or
            self.file_exists("build.gradle") or
            self.file_exists("build.gradle.kts")
        )

    def validate(self) -> List[ValidationResult]:
        """Run Java-specific validation checks."""
        self.results = []

        # Detect build tool
        is_maven = self.file_exists("pom.xml")
        is_gradle = self.file_exists("build.gradle") or self.file_exists("build.gradle.kts")

        if is_maven:
            self._validate_maven()
        elif is_gradle:
            self._validate_gradle()

        return self.results

    def _validate_maven(self):
        """Run Maven-specific checks."""
        # 1. Compile
        result = self.run_command(
            ["mvn", "compile", "-q"],
            check_name="Maven Compile",
            success_message="Kompilierung erfolgreich",
            error_message="Kompilierungsfehler gefunden"
        )
        self.results.append(result)

        # 2. Tests (unless skipped)
        if not self.skip_tests:
            result = self.run_command(
                ["mvn", "test", "-q"],
                check_name="Maven Test",
                success_message="Alle Tests bestanden",
                error_message="Test-Fehler gefunden"
            )
            self.results.append(result)

        # 3. Checkstyle (if configured)
        if self._has_checkstyle_maven():
            result = self.run_command(
                ["mvn", "checkstyle:check", "-q"],
                check_name="Checkstyle",
                success_message="Code-Style konform",
                error_message="Style-Verstöße gefunden"
            )
            self.results.append(result)

        # 4. SpotBugs (if configured)
        if self._has_spotbugs_maven():
            result = self.run_command(
                ["mvn", "spotbugs:check", "-q"],
                check_name="SpotBugs",
                success_message="Keine Bugs gefunden",
                error_message="Potenzielle Bugs gefunden"
            )
            self.results.append(result)

    def _validate_gradle(self):
        """Run Gradle-specific checks."""
        # Detect Gradle wrapper
        gradle_cmd = "./gradlew" if self.file_exists("gradlew") else "gradle"

        # 1. Build (includes compile + checks)
        result = self.run_command(
            [gradle_cmd, "build", "-x", "test", "--quiet"],
            check_name="Gradle Build",
            success_message="Build erfolgreich",
            error_message="Build-Fehler gefunden"
        )
        self.results.append(result)

        # 2. Tests (unless skipped)
        if not self.skip_tests:
            result = self.run_command(
                [gradle_cmd, "test", "--quiet"],
                check_name="Gradle Test",
                success_message="Alle Tests bestanden",
                error_message="Test-Fehler gefunden"
            )
            self.results.append(result)

        # 3. Checkstyle (if configured)
        if self._has_checkstyle_gradle():
            result = self.run_command(
                [gradle_cmd, "checkstyleMain", "--quiet"],
                check_name="Checkstyle",
                success_message="Code-Style konform",
                error_message="Style-Verstöße gefunden"
            )
            self.results.append(result)

    def _has_checkstyle_maven(self) -> bool:
        """Check if Checkstyle is configured in Maven."""
        import os
        pom_path = os.path.join(self.project_root, "pom.xml")
        try:
            with open(pom_path, 'r') as f:
                return 'maven-checkstyle-plugin' in f.read()
        except:
            return False

    def _has_spotbugs_maven(self) -> bool:
        """Check if SpotBugs is configured in Maven."""
        import os
        pom_path = os.path.join(self.project_root, "pom.xml")
        try:
            with open(pom_path, 'r') as f:
                return 'spotbugs-maven-plugin' in f.read()
        except:
            return False

    def _has_checkstyle_gradle(self) -> bool:
        """Check if Checkstyle is configured in Gradle."""
        import os
        for build_file in ["build.gradle", "build.gradle.kts"]:
            build_path = os.path.join(self.project_root, build_file)
            if os.path.exists(build_path):
                try:
                    with open(build_path, 'r') as f:
                        content = f.read()
                        if 'checkstyle' in content or "'checkstyle'" in content:
                            return True
                except:
                    pass
        return False
