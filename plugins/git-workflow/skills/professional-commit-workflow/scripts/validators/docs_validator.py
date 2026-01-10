#!/usr/bin/env python3
"""Documentation project validator (LaTeX, Markdown, AsciiDoc)."""

import os
from typing import List, Optional
from .base_validator import BaseValidator, ValidationResult


class DocsValidator(BaseValidator):
    """Validator for documentation projects."""

    def detect(self) -> bool:
        """Detect if this is a documentation project."""
        # Check for LaTeX files
        if self._has_files_with_extension(".tex"):
            return True

        # Check for Markdown files (but not just README)
        md_files = self._count_files_with_extension(".md")
        if md_files > 2:  # More than just README and LICENSE
            return True

        # Check for AsciiDoc files
        if self._has_files_with_extension(".adoc"):
            return True

        return False

    def validate(self) -> List[ValidationResult]:
        """Run documentation-specific validation checks."""
        self.results = []

        # 1. LaTeX compilation
        if self._has_files_with_extension(".tex"):
            self._validate_latex()

        # 2. Markdown linting
        if self._has_files_with_extension(".md"):
            self._validate_markdown()

        # 3. AsciiDoc rendering
        if self._has_files_with_extension(".adoc"):
            self._validate_asciidoc()

        return self.results

    def _validate_latex(self):
        """Validate LaTeX documents."""
        # Find main .tex file (usually main.tex or the first one)
        main_tex = self._find_main_latex_file()

        if not main_tex:
            self.results.append(
                ValidationResult(
                    name="LaTeX",
                    passed=False,
                    message="Keine LaTeX-Hauptdatei gefunden",
                    details="Erwarte main.tex oder ähnliche Datei"
                )
            )
            return

        # Try pdflatex
        if self.tool_exists("pdflatex"):
            result = self.run_command(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", main_tex],
                check_name="LaTeX Compile (pdflatex)",
                success_message="Kompilierung erfolgreich",
                error_message="Kompilierungs-Fehler gefunden"
            )
            self.results.append(result)
        # Try xelatex as fallback
        elif self.tool_exists("xelatex"):
            result = self.run_command(
                ["xelatex", "-interaction=nonstopmode", "-halt-on-error", main_tex],
                check_name="LaTeX Compile (xelatex)",
                success_message="Kompilierung erfolgreich",
                error_message="Kompilierungs-Fehler gefunden"
            )
            self.results.append(result)
        else:
            self.results.append(
                ValidationResult(
                    name="LaTeX",
                    passed=False,
                    message="LaTeX nicht installiert",
                    details="Installiere pdflatex oder xelatex"
                )
            )

    def _validate_markdown(self):
        """Validate Markdown documents."""
        # markdownlint
        if self.tool_exists("markdownlint"):
            result = self.run_command(
                ["markdownlint", "**/*.md", "--ignore", "node_modules"],
                check_name="markdownlint",
                success_message="Keine Markdown-Fehler",
                error_message="Markdown-Lint-Fehler gefunden"
            )
            self.results.append(result)

        # markdown-link-check (if available)
        if self.tool_exists("markdown-link-check"):
            # Only check README to avoid too many external requests
            if self.file_exists("README.md"):
                result = self.run_command(
                    ["markdown-link-check", "README.md"],
                    check_name="Link Check",
                    success_message="Alle Links gültig",
                    error_message="Kaputte Links gefunden"
                )
                self.results.append(result)

    def _validate_asciidoc(self):
        """Validate AsciiDoc documents."""
        if self.tool_exists("asciidoctor"):
            # Find all .adoc files
            adoc_files = self._find_files_with_extension(".adoc")

            for adoc_file in adoc_files[:5]:  # Limit to first 5 files
                result = self.run_command(
                    ["asciidoctor", "--backend=html5", "-o", "/dev/null", adoc_file],
                    check_name=f"AsciiDoc ({os.path.basename(adoc_file)})",
                    success_message="Rendering erfolgreich",
                    error_message="Rendering-Fehler gefunden"
                )
                self.results.append(result)
        else:
            self.results.append(
                ValidationResult(
                    name="AsciiDoc",
                    passed=False,
                    message="asciidoctor nicht installiert",
                    details="Installiere asciidoctor für AsciiDoc-Validierung"
                )
            )

    def _has_files_with_extension(self, ext: str) -> bool:
        """Check if directory contains files with given extension."""
        for root, _, files in os.walk(self.project_root):
            # Skip common ignore directories
            if any(ignore in root for ignore in ['.git', 'node_modules', '__pycache__', 'venv']):
                continue
            for file in files:
                if file.endswith(ext):
                    return True
        return False

    def _count_files_with_extension(self, ext: str) -> int:
        """Count files with given extension."""
        count = 0
        for root, _, files in os.walk(self.project_root):
            if any(ignore in root for ignore in ['.git', 'node_modules', '__pycache__', 'venv']):
                continue
            count += sum(1 for file in files if file.endswith(ext))
        return count

    def _find_files_with_extension(self, ext: str) -> List[str]:
        """Find all files with given extension."""
        result = []
        for root, _, files in os.walk(self.project_root):
            if any(ignore in root for ignore in ['.git', 'node_modules', '__pycache__', 'venv']):
                continue
            for file in files:
                if file.endswith(ext):
                    result.append(os.path.join(root, file))
        return result

    def _find_main_latex_file(self) -> Optional[str]:
        """Find main LaTeX file."""
        # Common main file names
        candidates = ["main.tex", "document.tex", "thesis.tex", "paper.tex"]

        for candidate in candidates:
            if self.file_exists(candidate):
                return candidate

        # Fallback: return first .tex file found
        tex_files = self._find_files_with_extension(".tex")
        return tex_files[0] if tex_files else None
