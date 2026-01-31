#!/usr/bin/env python3
"""Git repository initializer with develop → main branching strategy."""

import subprocess
import sys
from pathlib import Path


def run_git(args: list[str], cwd: Path | None = None) -> tuple[bool, str]:
    """Run a git command and return success status and output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()
    except FileNotFoundError:
        return False, "Git is not installed"


def is_git_repo(path: Path) -> bool:
    """Check if path is already a git repository."""
    return (path / ".git").exists()


def init_repository(
    project_path: Path,
    use_branching: bool = True,
) -> bool:
    """Initialize git repository with develop → main strategy.

    Args:
        project_path: Path to the project directory
        use_branching: If True, use develop → main strategy. If False, only main.

    Returns:
        True if successful, False otherwise.
    """
    if is_git_repo(project_path):
        print(f"⚠️  Git repository already exists at {project_path}")
        return True

    # Initialize repository
    success, output = run_git(["init"], cwd=project_path)
    if not success:
        print(f"❌ Failed to initialize git repository: {output}")
        return False
    print("✓ Git-Repository initialisiert")

    if use_branching:
        # Create and switch to develop branch
        success, output = run_git(["checkout", "-b", "develop"], cwd=project_path)
        if not success:
            print(f"❌ Failed to create develop branch: {output}")
            return False
        print("✓ Branch 'develop' erstellt (aktiv)")
    else:
        # Just rename default branch to main
        success, output = run_git(["branch", "-M", "main"], cwd=project_path)
        if not success:
            print(f"❌ Failed to rename branch to main: {output}")
            return False
        print("✓ Branch 'main' erstellt (aktiv)")

    return True


def create_initial_commit(
    project_path: Path,
    message: str = "feat: Initial open source setup",
) -> bool:
    """Create the initial commit with all staged files.

    Args:
        project_path: Path to the project directory
        message: Commit message

    Returns:
        True if successful, False otherwise.
    """
    # Stage all files
    success, output = run_git(["add", "."], cwd=project_path)
    if not success:
        print(f"❌ Failed to stage files: {output}")
        return False

    # Check if there are files to commit
    success, output = run_git(["status", "--porcelain"], cwd=project_path)
    if not output:
        # No files to commit, create empty commit
        success, output = run_git(
            ["commit", "--allow-empty", "-m", message],
            cwd=project_path,
        )
    else:
        success, output = run_git(["commit", "-m", message], cwd=project_path)

    if not success:
        print(f"❌ Failed to create commit: {output}")
        return False
    print("✓ Initialer Commit erstellt")

    return True


def create_main_branch(project_path: Path) -> bool:
    """Create main branch from current HEAD (synchronized with develop).

    Args:
        project_path: Path to the project directory

    Returns:
        True if successful, False otherwise.
    """
    success, output = run_git(["branch", "main"], cwd=project_path)
    if not success:
        if "already exists" in output:
            print("⚠️  Branch 'main' existiert bereits")
            return True
        print(f"❌ Failed to create main branch: {output}")
        return False
    print("✓ Branch 'main' erstellt (synchron mit develop)")

    return True


def setup_remote(
    project_path: Path,
    repo_name: str,
    push_branches: bool = True,
) -> bool:
    """Setup GitHub remote and push branches.

    Args:
        project_path: Path to the project directory
        repo_name: GitHub repository name (user/repo or just repo)
        push_branches: If True, push develop and main branches

    Returns:
        True if successful, False otherwise.
    """
    # Check if gh CLI is available
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  GitHub CLI (gh) nicht verfügbar - Remote-Setup übersprungen")
        return False

    # Create repository
    result = subprocess.run(
        ["gh", "repo", "create", repo_name, "--public", "--source", str(project_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"⚠️  Repository-Erstellung fehlgeschlagen: {result.stderr}")
        return False
    print(f"✓ GitHub Repository erstellt: {repo_name}")

    if push_branches:
        # Push both branches
        success, output = run_git(
            ["push", "-u", "origin", "develop", "main"],
            cwd=project_path,
        )
        if not success:
            print(f"⚠️  Push fehlgeschlagen: {output}")
            return False
        print("✓ Branches gepusht (develop, main)")

        # Set develop as default branch
        result = subprocess.run(
            ["gh", "repo", "edit", "--default-branch", "develop"],
            cwd=project_path,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("✓ develop als Standard-Branch gesetzt")

    return True


def initialize_project(
    project_path: Path,
    use_branching: bool = True,
    commit_message: str | None = None,
    setup_github: bool = False,
    repo_name: str | None = None,
) -> bool:
    """Complete git initialization workflow.

    Args:
        project_path: Path to the project directory
        use_branching: If True, use develop → main strategy
        commit_message: Custom commit message (optional)
        setup_github: If True, create GitHub repository
        repo_name: GitHub repository name (required if setup_github is True)

    Returns:
        True if all steps successful, False otherwise.
    """
    # Step 1: Initialize repository
    if not init_repository(project_path, use_branching):
        return False

    # Step 2: Create initial commit
    message = commit_message or "feat: Initial open source setup"
    if not create_initial_commit(project_path, message):
        return False

    # Step 3: Create main branch (if using branching strategy)
    if use_branching:
        if not create_main_branch(project_path):
            return False

    # Step 4: Setup GitHub remote (optional)
    if setup_github and repo_name:
        setup_remote(project_path, repo_name)

    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Initialize git repository")
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Project path (default: current directory)",
    )
    parser.add_argument(
        "--no-branching",
        action="store_true",
        help="Only use main branch, no develop",
    )
    parser.add_argument(
        "--message",
        "-m",
        type=str,
        help="Custom commit message",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="Create GitHub repository",
    )
    parser.add_argument(
        "--repo",
        type=str,
        help="GitHub repository name",
    )

    args = parser.parse_args()

    success = initialize_project(
        project_path=args.path.resolve(),
        use_branching=not args.no_branching,
        commit_message=args.message,
        setup_github=args.github,
        repo_name=args.repo,
    )

    sys.exit(0 if success else 1)
