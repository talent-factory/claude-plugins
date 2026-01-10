#!/usr/bin/env python3
"""Professional PR Workflow - Main Orchestrator"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from git.branch_manager import BranchManager
from git.pr_creator import PRCreator
from formatters.code_formatter import CodeFormatter


def main():
    parser = argparse.ArgumentParser(description='Professional PR Workflow')
    parser.add_argument('--draft', action='store_true', help='Create draft PR')
    parser.add_argument('--no-format', action='store_true', help='Skip code formatting')
    parser.add_argument('--single-commit', action='store_true', help='Single commit for all changes')
    parser.add_argument('--target', default='main', help='Target branch (default: main)')

    args = parser.parse_args()

    print("=" * 60)
    print("  Professional PR Workflow")
    print("=" * 60)

    # 1. Branch Management
    branch_mgr = BranchManager()
    if not branch_mgr.ensure_feature_branch():
        return 1

    # 2. Commit Integration
    if not branch_mgr.has_commits():
        print("\n⚠️  Keine Commits gefunden")
        print("Rufe professional-commit-workflow auf...")
        # Nutzer muss commit-workflow manuell aufrufen
        return 1

    # 3. Code Formatting
    if not args.no_format:
        formatter = CodeFormatter()
        formatter.format_all()

    # 4. Create PR
    pr_creator = PRCreator(draft=args.draft, target=args.target)
    if not pr_creator.create():
        return 1

    print("\n✅ PR-Workflow erfolgreich abgeschlossen")
    return 0


if __name__ == '__main__':
    sys.exit(main())
