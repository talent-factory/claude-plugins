#!/usr/bin/env python3
"""
Professional Commit Workflow - Main Orchestration Script

Automates the complete git commit workflow with quality checks and
conventional commit messages.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from project_detector import ProjectDetector
from git_analyzer import GitAnalyzer
from commit_message import CommitMessageGenerator
from utils import (
    print_header, print_success, print_error, print_warning,
    print_info, confirm, format_file_list
)
from validators import (
    JavaValidator, PythonValidator, ReactValidator, DocsValidator
)


class CommitWorkflow:
    """Main workflow orchestrator."""

    def __init__(
        self,
        no_verify: bool = False,
        skip_tests: bool = False,
        force_push: bool = False,
        validate_only: bool = False
    ):
        self.no_verify = no_verify
        self.skip_tests = skip_tests
        self.force_push = force_push
        self.validate_only = validate_only

        try:
            self.git_analyzer = GitAnalyzer()
            self.project_root = self.git_analyzer.project_root
        except RuntimeError as e:
            print_error(f"Fehler: {e}")
            sys.exit(1)

        self.project_detector = ProjectDetector(self.project_root)
        self.commit_generator = CommitMessageGenerator()

    def run(self) -> int:
        """Execute complete commit workflow."""
        print_header("Professional Commit Workflow")

        # Step 1: Detect project types
        project_types = self.project_detector.detect_all()
        if project_types:
            print_success(f"Projekt-Typen erkannt: {', '.join(project_types)}")
        else:
            print_warning("Kein spezifischer Projekt-Typ erkannt")

        # Step 2: Analyze git status
        if not self._analyze_git_status():
            return 1

        # Step 3: Run pre-commit validations (unless --no-verify)
        if not self.no_verify:
            if not self._run_validations(project_types):
                print_error("\n❌ Pre-Commit-Checks fehlgeschlagen")
                print_info("Behebe die Fehler oder verwende --no-verify zum Überspringen")
                return 1
        else:
            print_warning("Pre-Commit-Checks übersprungen (--no-verify)")

        # If validate-only mode, stop here
        if self.validate_only:
            print_success("\n✅ Alle Validierungen bestanden")
            return 0

        # Step 4: Analyze diff and suggest atomic commits
        self._analyze_diff()

        # Step 5: Generate commit message
        commit_message = self._generate_commit_message()
        if not commit_message:
            return 1

        # Step 6: Create commit
        if not self._create_commit(commit_message):
            return 1

        # Step 7: Offer to push
        if not self._offer_push():
            return 1

        print_success("\n✅ Commit-Workflow erfolgreich abgeschlossen")
        return 0

    def _analyze_git_status(self) -> bool:
        """Analyze and handle git status."""
        print_header("Git-Status Analyse")

        status = self.git_analyzer.get_status()

        # Check for staged changes
        if not status['staged']:
            print_info("Keine gestakten Änderungen gefunden")

            # Check for unstaged changes
            if status['modified'] or status['untracked']:
                print_info(f"Nicht gestakte Änderungen: {len(status['modified']) + len(status['untracked'])} Dateien")

                if confirm("Alle Änderungen automatisch hinzufügen?"):
                    success, message = self.git_analyzer.auto_stage_all()
                    if success:
                        print_success(message)
                    else:
                        print_error(message)
                        return False
                else:
                    print_info("Bitte stage Änderungen manuell mit: git add <files>")
                    return False
            else:
                print_error("Keine Änderungen gefunden")
                return False

        print_success(f"{len(status['staged'])} Dateien bereit zum Commit")
        print(format_file_list(status['staged'][:10]))

        return True

    def _run_validations(self, project_types: List[str]) -> bool:
        """Run pre-commit validations for detected project types."""
        print_header("Pre-Commit-Validierung")

        validators = []

        # Initialize validators based on detected types
        if 'java' in project_types:
            validators.append(JavaValidator(self.project_root, self.skip_tests))

        if 'python' in project_types:
            validators.append(PythonValidator(self.project_root, self.skip_tests))

        if 'react' in project_types:
            validators.append(ReactValidator(self.project_root, self.skip_tests))

        if 'docs' in project_types:
            validators.append(DocsValidator(self.project_root, self.skip_tests))

        if not validators:
            print_info("Keine projektspezifischen Validierungen gefunden")
            return True

        # Run all validators
        all_passed = True
        total_passed = 0
        total_checks = 0

        for validator in validators:
            results = validator.validate()
            passed, total = validator.get_summary()
            total_passed += passed
            total_checks += total

            for result in results:
                if result.passed:
                    print_success(f"{result.name}: {result.message}")
                else:
                    print_error(f"{result.name}: {result.message}")
                    if result.details:
                        # Print first few lines of error details
                        lines = result.details.split('\n')[:5]
                        for line in lines:
                            if line.strip():
                                print(f"    {line}")
                    all_passed = False

        # Print summary
        print(f"\nValidierungs-Ergebnis: {total_passed}/{total_checks} Checks bestanden")

        return all_passed

    def _analyze_diff(self):
        """Analyze diff and suggest atomic commits if needed."""
        print_header("Diff-Analyse")

        diff_info = self.git_analyzer.analyze_diff()

        print_info(f"Dateien geändert: {diff_info['files_changed']}")
        print_info(f"Einfügungen: +{diff_info['insertions']}")
        print_info(f"Löschungen: -{diff_info['deletions']}")

        # Check for multiple logical changes
        if self.git_analyzer.detect_multiple_changes():
            print_warning("\n⚠️  Mehrere logische Änderungen erkannt")
            print_info("Erwäge Aufteilung in atomare Commits:")
            for suggestion in self.git_analyzer.suggest_split_commits():
                print(f"  - {suggestion}")
            print()

    def _generate_commit_message(self) -> Optional[str]:
        """Generate commit message."""
        print_header("Commit-Nachricht")

        message = self.commit_generator.generate()
        print_info(f"Generiert: {message}")

        if not confirm("Commit-Nachricht verwenden?"):
            custom_message = input("Eigene Nachricht eingeben: ").strip()
            if not custom_message:
                print_error("Keine Commit-Nachricht angegeben")
                return None
            message = custom_message

        return message

    def _create_commit(self, message: str) -> bool:
        """Create git commit."""
        print_header("Commit erstellen")

        try:
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.project_root,
                check=True,
                capture_output=True,
                text=True
            )
            print_success(f"Commit erstellt: {message}")
            return True

        except subprocess.CalledProcessError as e:
            print_error(f"Commit fehlgeschlagen: {e.stderr}")
            return False

    def _offer_push(self) -> bool:
        """Offer to push to remote."""
        print_header("Push zum Remote")

        # Get current branch
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            branch = result.stdout.strip()

            if self.force_push:
                if confirm(f"⚠️  Force Push zu '{branch}'?", default=False):
                    self._execute_push(branch, force=True)
            else:
                if confirm(f"Push zu '{branch}'?"):
                    self._execute_push(branch, force=False)

            return True

        except subprocess.CalledProcessError as e:
            print_error(f"Branch-Erkennung fehlgeschlagen: {e}")
            return False

    def _execute_push(self, branch: str, force: bool = False):
        """Execute git push."""
        try:
            cmd = ["git", "push", "origin", branch]
            if force:
                cmd.append("--force")

            subprocess.run(cmd, cwd=self.project_root, check=True)
            print_success(f"Push zu '{branch}' erfolgreich")

        except subprocess.CalledProcessError as e:
            print_error(f"Push fehlgeschlagen: {e}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Professional Git Commit Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s                    # Standard-Commit-Workflow
  %(prog)s --no-verify        # Checks überspringen
  %(prog)s --skip-tests       # Nur Tests überspringen
  %(prog)s --validate-only    # Nur Validierung, kein Commit
  %(prog)s --force-push       # Mit Force-Push
        """
    )

    parser.add_argument(
        '--no-verify',
        action='store_true',
        help='Überspringt alle Pre-Commit-Checks'
    )
    parser.add_argument(
        '--skip-tests',
        action='store_true',
        help='Überspringt nur Tests (Linting/Build läuft weiter)'
    )
    parser.add_argument(
        '--force-push',
        action='store_true',
        help='Führt Force-Push aus (⚠️  Vorsicht!)'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Führt nur Validierung aus, erstellt keinen Commit'
    )

    args = parser.parse_args()

    workflow = CommitWorkflow(
        no_verify=args.no_verify,
        skip_tests=args.skip_tests,
        force_push=args.force_push,
        validate_only=args.validate_only
    )

    return workflow.run()


if __name__ == '__main__':
    sys.exit(main())
