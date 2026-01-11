#!/usr/bin/env python3
"""Generate emoji conventional commit messages."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional, List


class CommitMessageGenerator:
    """Generate conventional commit messages with emojis."""

    def __init__(self, config_path: Optional[str] = None):
        if config_path is None:
            script_dir = Path(__file__).parent.parent
            config_path = script_dir / "config" / "commit_types.json"

        self.commit_types = self._load_commit_types(config_path)
        self.project_root = self._get_project_root()

    def _load_commit_types(self, config_path: Path) -> Dict:
        """Load commit types from JSON config."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to default commit types
            return {
                "feat": {"emoji": "✨", "description": "Neue Funktionalität"},
                "fix": {"emoji": "🐛", "description": "Fehlerbehebung"},
                "docs": {"emoji": "📚", "description": "Dokumentation"},
                "style": {"emoji": "💎", "description": "Code-Formatierung"},
                "refactor": {"emoji": "♻️", "description": "Code-Umstrukturierung"},
                "perf": {"emoji": "⚡", "description": "Performance-Verbesserungen"},
                "test": {"emoji": "🧪", "description": "Tests"},
                "chore": {"emoji": "🔧", "description": "Wartung"},
                "ci": {"emoji": "🚀", "description": "CI/CD"},
                "security": {"emoji": "🔒", "description": "Sicherheit"},
            }

    def _get_project_root(self) -> str:
        """Get git project root."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return os.getcwd()

    def detect_commit_type(self) -> str:
        """Detect commit type from staged changes."""
        try:
            # Get list of staged files
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            files = result.stdout.strip().split('\n')

            # Get diff stats
            diff_result = subprocess.run(
                ["git", "diff", "--cached", "--stat"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            diff_stat = diff_result.stdout

            # Detection logic
            if any('test' in f.lower() for f in files):
                return 'test'

            if any(f.endswith('.md') or f.endswith('.txt') or 'doc' in f.lower() for f in files):
                if all(f.endswith(('.md', '.txt', '.adoc', '.rst')) for f in files if f):
                    return 'docs'

            if '.github/workflows' in ' '.join(files) or '.gitlab-ci' in ' '.join(files):
                return 'ci'

            if 'security' in diff_stat.lower() or 'vulnerability' in diff_stat.lower():
                return 'security'

            # Check commit message keywords in diff
            diff_content = subprocess.run(
                ["git", "diff", "--cached"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            ).stdout.lower()

            if 'fix' in diff_content or 'bug' in diff_content:
                return 'fix'

            if 'refactor' in diff_content:
                return 'refactor'

            # Default to feat for new functionality
            return 'feat'

        except subprocess.CalledProcessError:
            return 'chore'

    def generate_description(self) -> str:
        """Generate commit description from staged changes."""
        try:
            # Get commit stats
            result = subprocess.run(
                ["git", "diff", "--cached", "--stat"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            stat = result.stdout.strip()

            if not stat:
                return "Änderungen commiten"

            # Get list of modified files
            files_result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            files = [f for f in files_result.stdout.strip().split('\n') if f]

            if len(files) == 1:
                # Single file - use filename
                filename = os.path.basename(files[0])
                return f"{filename} aktualisiert"

            # Multiple files - use directory or generic description
            common_dir = self._get_common_directory(files)
            if common_dir and common_dir != '.':
                return f"{common_dir}/ Komponenten aktualisiert"

            return f"{len(files)} Dateien aktualisiert"

        except subprocess.CalledProcessError:
            return "Änderungen commiten"

    def _get_common_directory(self, files: List[str]) -> Optional[str]:
        """Get common directory from file list."""
        if not files:
            return None

        dirs = [os.path.dirname(f) for f in files]
        if not dirs:
            return None

        # Find common prefix
        common = os.path.commonprefix(dirs)
        if common and common != '.':
            return common.split('/')[-1]  # Return last component

        return None

    def format_commit_message(self, commit_type: str, description: str) -> str:
        """Format final commit message."""
        type_info = self.commit_types.get(commit_type, self.commit_types['chore'])
        emoji = type_info['emoji']

        # Ensure imperative form
        description = self._to_imperative(description)

        # Ensure first letter is capitalized
        description = description[0].upper() + description[1:] if description else description

        return f"{emoji} {commit_type}: {description}"

    def _to_imperative(self, text: str) -> str:
        """Convert text to imperative form (basic rules)."""
        # Common patterns to fix
        replacements = {
            'hinzugefügt': 'hinzufügen',
            'aktualisiert': 'aktualisieren',
            'behoben': 'beheben',
            'korrigiert': 'korrigieren',
            'entfernt': 'entfernen',
            'gelöscht': 'löschen',
            'implementiert': 'implementieren',
            'erstellt': 'erstellen',
        }

        text_lower = text.lower()
        for past, imperative in replacements.items():
            if past in text_lower:
                # Replace while preserving case of first letter
                if text[0].isupper():
                    return text_lower.replace(past, imperative).capitalize()
                else:
                    return text_lower.replace(past, imperative)

        return text

    def generate(self, commit_type: Optional[str] = None, description: Optional[str] = None) -> str:
        """Generate complete commit message."""
        if commit_type is None:
            commit_type = self.detect_commit_type()

        if description is None:
            description = self.generate_description()

        return self.format_commit_message(commit_type, description)


def main():
    """CLI interface for commit message generator."""
    parser = argparse.ArgumentParser(description='Generate emoji conventional commit messages')
    parser.add_argument('--type', help='Commit type (feat, fix, docs, etc.)')
    parser.add_argument('--description', help='Commit description')
    parser.add_argument('--generate', action='store_true', help='Auto-generate message')
    parser.add_argument('--output', action='store_true', help='Output generated message only')

    args = parser.parse_args()

    generator = CommitMessageGenerator()

    if args.generate or args.output:
        message = generator.generate(args.type, args.description)
        print(message)
    else:
        # Interactive mode
        commit_type = args.type or generator.detect_commit_type()
        print(f"Erkannter Commit-Typ: {commit_type}")

        description = args.description or generator.generate_description()
        print(f"Generierte Beschreibung: {description}")

        message = generator.format_commit_message(commit_type, description)
        print(f"\nCommit-Nachricht:\n{message}")


if __name__ == '__main__':
    main()
