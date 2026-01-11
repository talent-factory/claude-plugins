#!/usr/bin/env python3
"""Analyze git repository status and staged changes."""

import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class GitAnalyzer:
    """Analyze git repository for commit preparation."""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = project_root or self._get_git_root()

    def _get_git_root(self) -> str:
        """Get git repository root."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            raise RuntimeError("Not a git repository")

    def get_status(self) -> Dict[str, List[str]]:
        """Get comprehensive git status."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            status = {
                'staged': [],
                'modified': [],
                'untracked': [],
                'deleted': [],
            }

            for line in result.stdout.split('\n'):
                if not line:
                    continue

                code = line[:2]
                filepath = line[3:]

                if code[0] in ['M', 'A', 'D', 'R', 'C']:
                    status['staged'].append(filepath)
                if code[1] == 'M':
                    status['modified'].append(filepath)
                elif code[1] == 'D':
                    status['deleted'].append(filepath)
                elif code == '??':
                    status['untracked'].append(filepath)

            return status

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git status failed: {e}")

    def has_staged_changes(self) -> bool:
        """Check if there are staged changes."""
        status = self.get_status()
        return len(status['staged']) > 0

    def has_unstaged_changes(self) -> bool:
        """Check if there are unstaged changes."""
        status = self.get_status()
        return len(status['modified']) > 0 or len(status['deleted']) > 0

    def analyze_diff(self, staged_only: bool = True) -> Dict:
        """Analyze git diff for commit insights."""
        cmd = ["git", "diff", "--cached"] if staged_only else ["git", "diff"]

        try:
            # Get diff stats
            result = subprocess.run(
                cmd + ["--stat"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            stat_output = result.stdout

            # Get full diff
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            diff_output = result.stdout

            # Parse stats
            files_changed = 0
            insertions = 0
            deletions = 0

            if stat_output:
                last_line = stat_output.strip().split('\n')[-1]
                parts = last_line.split(',')
                for part in parts:
                    if 'file' in part:
                        files_changed = int(part.split()[0])
                    elif 'insertion' in part:
                        insertions = int(part.split()[0])
                    elif 'deletion' in part:
                        deletions = int(part.split()[0])

            return {
                'files_changed': files_changed,
                'insertions': insertions,
                'deletions': deletions,
                'stat': stat_output,
                'diff': diff_output,
            }

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git diff failed: {e}")

    def detect_multiple_changes(self) -> bool:
        """Detect if multiple logical changes are in one commit."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            files = [f for f in result.stdout.split('\n') if f]

            if len(files) > 10:
                return True

            # Check if files are in different top-level directories
            directories = set()
            for filepath in files:
                parts = Path(filepath).parts
                if len(parts) > 1:
                    directories.add(parts[0])

            # If changes span more than 3 top-level directories, might be multiple changes
            if len(directories) > 3:
                return True

            return False

        except subprocess.CalledProcessError:
            return False

    def suggest_split_commits(self) -> List[str]:
        """Suggest how to split commits if multiple changes detected."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            files = [f for f in result.stdout.split('\n') if f]

            # Group by top-level directory
            groups = {}
            for filepath in files:
                parts = Path(filepath).parts
                top_dir = parts[0] if len(parts) > 1 else '.'
                if top_dir not in groups:
                    groups[top_dir] = []
                groups[top_dir].append(filepath)

            suggestions = []
            for directory, file_list in groups.items():
                suggestions.append(f"{directory}/: {len(file_list)} files")

            return suggestions

        except subprocess.CalledProcessError:
            return []

    def get_recent_commits(self, count: int = 5) -> List[str]:
        """Get recent commit messages for context."""
        try:
            result = subprocess.run(
                ["git", "log", f"-{count}", "--oneline"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n')
        except subprocess.CalledProcessError:
            return []

    def auto_stage_all(self) -> Tuple[bool, str]:
        """Auto-stage all modified files."""
        try:
            status = self.get_status()

            if not status['modified'] and not status['untracked']:
                return False, "Keine Änderungen zum Hinzufügen"

            subprocess.run(
                ["git", "add", "-A"],
                cwd=self.project_root,
                check=True
            )

            total = len(status['modified']) + len(status['untracked'])
            return True, f"{total} Dateien zum Staging hinzugefügt"

        except subprocess.CalledProcessError as e:
            return False, f"Git add fehlgeschlagen: {e}"


def main():
    """CLI interface for git analyzer."""
    parser = argparse.ArgumentParser(description='Analyze git repository')
    parser.add_argument('--analyze-staging', action='store_true', help='Analyze staging status')
    parser.add_argument('--analyze-diff', action='store_true', help='Analyze diff')
    parser.add_argument('--check-multiple', action='store_true', help='Check for multiple changes')

    args = parser.parse_args()

    try:
        analyzer = GitAnalyzer()

        if args.analyze_staging:
            status = analyzer.get_status()
            print(f"Staged: {len(status['staged'])} files")
            print(f"Modified: {len(status['modified'])} files")
            print(f"Untracked: {len(status['untracked'])} files")

        if args.analyze_diff:
            diff_info = analyzer.analyze_diff()
            print(f"\nDiff Stats:")
            print(f"  Files changed: {diff_info['files_changed']}")
            print(f"  Insertions: +{diff_info['insertions']}")
            print(f"  Deletions: -{diff_info['deletions']}")

        if args.check_multiple:
            if analyzer.detect_multiple_changes():
                print("\n⚠️  Multiple logical changes detected")
                print("Consider splitting into atomic commits:")
                for suggestion in analyzer.suggest_split_commits():
                    print(f"  - {suggestion}")

    except RuntimeError as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
