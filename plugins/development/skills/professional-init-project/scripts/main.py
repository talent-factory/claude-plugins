#!/usr/bin/env python3
"""Main entry point for professional-init-project skill."""

import argparse
import sys
from pathlib import Path

from generators import CommonGenerator, JavaGradleGenerator, PythonUvGenerator
from git_initializer import initialize_project


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Initialize a new open source project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --type java --name my-app
  python main.py --type uv --name my-lib
  python main.py --type git --name my-project --no-branching
        """,
    )
    parser.add_argument(
        "--type",
        "-t",
        choices=["git", "java", "uv", "python", "node", "go", "rust"],
        default="git",
        help="Project type (default: git)",
    )
    parser.add_argument(
        "--name",
        "-n",
        required=True,
        help="Project name",
    )
    parser.add_argument(
        "--path",
        "-p",
        type=Path,
        default=None,
        help="Project path (default: current directory / name)",
    )
    parser.add_argument(
        "--author",
        "-a",
        default="Author",
        help="Author name",
    )
    parser.add_argument(
        "--email",
        "-e",
        default="author@example.com",
        help="Author email",
    )
    parser.add_argument(
        "--license",
        "-l",
        choices=["mit", "apache2", "gpl3", "bsd3"],
        default="mit",
        help="License type (default: mit)",
    )
    parser.add_argument(
        "--no-branching",
        action="store_true",
        help="Only use main branch, no develop",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="Create GitHub repository after initialization",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate, don't create files",
    )

    args = parser.parse_args()

    # Determine project path
    project_path = args.path or (Path.cwd() / args.name)
    project_path = project_path.resolve()

    # Validate
    if args.validate_only:
        print(f"Would create project: {args.name}")
        print(f"  Type: {args.type}")
        print(f"  Path: {project_path}")
        print(f"  License: {args.license}")
        print(f"  Branching: {'main only' if args.no_branching else 'develop → main'}")
        return 0

    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Erstelle Projekt: {args.name}")
    print(f"   Pfad: {project_path}\n")

    # Generate project-specific files
    success = True
    project_type = args.type if args.type != "python" else "uv"

    if project_type == "java":
        generator = JavaGradleGenerator(
            project_path=project_path,
            project_name=args.name,
        )
        success = generator.generate_all()
    elif project_type == "uv":
        generator = PythonUvGenerator(
            project_path=project_path,
            project_name=args.name,
            author=args.author,
            email=args.email,
        )
        success = generator.generate_all()
    elif project_type in ["node", "go", "rust"]:
        # Warn about unsupported language types
        print(
            f"⚠️  WARNUNG: Typ '{project_type}' wird noch nicht vollständig unterstützt."
        )
        print(f"   Es werden nur Community-Standards und Git-Initialisierung erstellt.")
        print(f"   Für vollständige Unterstützung verwende: --type java oder --type uv")
        print()

    if not success:
        return 1

    # Generate common files
    common = CommonGenerator(
        project_path=project_path,
        project_name=args.name,
        author=args.author,
    )
    if not common.generate_all(license_type=args.license):
        return 1

    # Initialize git
    if not initialize_project(
        project_path=project_path,
        use_branching=not args.no_branching,
        setup_github=args.github,
        repo_name=args.name if args.github else None,
    ):
        return 1

    # Success message
    print(f"\n📁 Projekt bereit: {args.name}/")
    if args.no_branching:
        print("   Branch: main (aktiv)")
    else:
        print("   Branch: develop (aktiv)")

    # Next steps
    print("\n   Nächste Schritte:")
    if project_type == "java":
        print("   ./gradlew build")
        print("   ./gradlew test")
    elif project_type == "uv":
        print("   uv venv && source .venv/bin/activate")
        print("   uv pip install -e .")
        print("   pytest")
    else:
        print("   # Start coding!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
