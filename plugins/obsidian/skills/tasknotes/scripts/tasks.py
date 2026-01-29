#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
TaskNotes CLI - Task management in Obsidian via the TaskNotes Plugin API.

Usage:
    uv run tasks.py list [--status STATUS] [--project PROJECT] [--limit N] [--scan] [--all]
    uv run tasks.py create "Title" [--project PROJECT] [--priority PRIORITY] [--status STATUS]
    uv run tasks.py update "Tasks/file.md" [--status STATUS] [--priority PRIORITY]
    uv run tasks.py delete "Tasks/file.md"
    uv run tasks.py stats
    uv run tasks.py options

Environment variables:
    TASKNOTES_API_KEY - API authentication token (optional, depends on TaskNotes settings)
    TASKNOTES_API_PORT - API port (default: 8080)
    OBSIDIAN_VAULT_PATH - Path to the Obsidian vault (optional, for .env file lookup)
"""

import argparse
import json
import os
import re
import urllib.parse
from pathlib import Path

import requests
from dotenv import load_dotenv


def find_and_load_env():
    """Search and load .env file from various possible locations."""
    possible_paths = []

    # 1. Explicit vault path via environment variable
    if vault_path := os.getenv("OBSIDIAN_VAULT_PATH"):
        possible_paths.append(Path(vault_path) / ".env")

    # 2. Current working directory
    possible_paths.append(Path.cwd() / ".env")

    # 3. Home directory
    possible_paths.append(Path.home() / ".env")

    # 4. Relative to script (legacy support)
    script_dir = Path(__file__).parent
    possible_paths.append(script_dir.parent.parent.parent.parent / ".env")

    for env_path in possible_paths:
        if env_path.exists():
            load_dotenv(env_path)
            return env_path

    return None


find_and_load_env()

API_KEY = os.getenv("TASKNOTES_API_KEY")
API_PORT = os.getenv("TASKNOTES_API_PORT", "8080")
BASE_URL = f"http://localhost:{API_PORT}/api"


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from Markdown file."""
    frontmatter_pattern = r'^---\s*\n(.*?)\n---'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    if not match:
        return {}

    yaml_content = match.group(1)
    result = {}

    # Simple YAML parser for required fields
    lines = yaml_content.split('\n')
    current_key = None
    current_list = []

    for line in lines:
        # List items
        if line.strip().startswith('- '):
            if current_key:
                item = line.strip()[2:].strip('"').strip("'")
                current_list.append(item)
            continue

        # Key-value pairs
        if ':' in line:
            # Save previous list if present
            if current_key and current_list:
                result[current_key] = current_list
                current_list = []

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            current_key = key

            if value:
                result[key] = value
                current_key = None

    # Save final list
    if current_key and current_list:
        result[current_key] = current_list

    return result


def find_all_tasks_in_vault(vault_path: Path, tag: str = "task") -> list:
    """Find all tasks in the vault by tag."""
    tasks = []

    # Search all .md files
    for md_file in vault_path.rglob("*.md"):
        # Skip .obsidian and other configuration folders
        if '.obsidian' in md_file.parts or '.trash' in str(md_file).lower():
            continue

        try:
            content = md_file.read_text(encoding='utf-8')

            # Check if tag is in frontmatter
            frontmatter = parse_frontmatter(content)
            tags = frontmatter.get('tags', [])

            # Tags can be string or list
            if isinstance(tags, str):
                tags = [tags]

            # Normalize tags (remove #)
            normalized_tags = [t.strip('#').strip() for t in tags]

            if tag in normalized_tags or f"#{tag}" in tags:
                # Get title from filename
                title = md_file.stem

                # Relative path to vault
                relative_path = md_file.relative_to(vault_path)

                task = {
                    'id': str(relative_path),
                    'title': title,
                    'status': frontmatter.get('status', 'none'),
                    'priority': frontmatter.get('priority', 'none'),
                    'projects': frontmatter.get('projects', []),
                    'due': frontmatter.get('due'),
                    'scheduled': frontmatter.get('scheduled'),
                    'path': str(relative_path)
                }
                tasks.append(task)
        except Exception:
            # Skip files with read errors
            continue

    return tasks


def get_vault_path() -> Path:
    """Determine the vault path."""
    # 1. Explicit vault path via environment variable
    if vault_path := os.getenv("OBSIDIAN_VAULT_PATH"):
        return Path(vault_path)

    # 2. Current working directory
    cwd = Path.cwd()

    # Check if we are in an Obsidian vault (.obsidian folder exists)
    if (cwd / ".obsidian").exists():
        return cwd

    # 3. Traverse upward until we find a .obsidian folder
    for parent in cwd.parents:
        if (parent / ".obsidian").exists():
            return parent

    # Fallback: current directory
    return cwd


def get_headers():
    """Create HTTP headers for API requests."""
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers


def api_request(method: str, endpoint: str, params: dict = None, data: dict = None):
    """Execute API request and return JSON response."""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.request(
            method, url, headers=get_headers(), params=params, json=data, timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "No connection to TaskNotes API. Is Obsidian running with TaskNotes API enabled?"}
    except requests.exceptions.HTTPError as e:
        try:
            return response.json()
        except Exception:
            return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


def list_tasks(args):
    """List tasks with optional filters."""
    # Use filesystem scan if --scan or --all is specified
    if args.scan or args.all:
        vault_path = get_vault_path()
        tasks = find_all_tasks_in_vault(vault_path)

        # Filter tasks
        if args.status:
            tasks = [t for t in tasks if t.get('status') == args.status]
        if args.priority:
            tasks = [t for t in tasks if t.get('priority') == args.priority]
        if args.project:
            tasks = [t for t in tasks if args.project in str(t.get('projects', []))]

        # Filter by status type if --all is not set
        if not args.all:
            # Only non-completed tasks
            tasks = [t for t in tasks if t.get('status') not in ['done', 'cancelled']]

        # Sort by scheduled/due
        tasks.sort(key=lambda t: (
            t.get('scheduled') or t.get('due') or '9999-99-99',
            t.get('status', 'none')
        ))

        # Limit results
        if args.limit:
            tasks = tasks[:args.limit]
    else:
        # Use API
        params = {}
        if args.status:
            params["status"] = args.status
        if args.project:
            params["project"] = args.project
        if args.priority:
            params["priority"] = args.priority
        if args.limit:
            params["limit"] = args.limit
        if args.overdue:
            params["overdue"] = "true"

        result = api_request("GET", "/tasks", params=params)

        if "error" in result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return

        tasks = result.get("data", {}).get("tasks", [])

    if args.table:
        # Human-readable table output
        if not tasks:
            print("No tasks found.")
            return
        print(f"{'Status':<15} {'Priority':<10} {'Title':<50} {'Project'}")
        print("-" * 100)
        for t in tasks:
            status = t.get("status", "none")
            priority = t.get("priority", "none")
            title = t.get("title", "")[:48]
            projects = ", ".join(t.get("projects", []))[:30]
            print(f"{status:<15} {priority:<10} {title:<50} {projects}")
        print(f"\nTotal: {len(tasks)} tasks")
    else:
        # JSON output for agents
        output = {
            "success": True,
            "count": len(tasks),
            "tasks": [
                {
                    "id": t.get("id"),
                    "title": t.get("title"),
                    "status": t.get("status"),
                    "priority": t.get("priority"),
                    "projects": t.get("projects", []),
                    "due": t.get("due"),
                    "scheduled": t.get("scheduled"),
                }
                for t in tasks
            ],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))


def create_task(args):
    """Create a new task."""
    data = {"title": args.title}

    if args.project:
        # Wrap project in [[ ]] if not already present
        project = args.project
        if not project.startswith("[["):
            project = f"[[{project}]]"
        data["projects"] = [project]

    if args.priority:
        data["priority"] = args.priority
    if args.status:
        data["status"] = args.status
    if args.due:
        data["due"] = args.due
    if args.scheduled:
        data["scheduled"] = args.scheduled
    if args.contexts:
        data["contexts"] = args.contexts.split(",")
    if args.time_estimate:
        data["timeEstimate"] = args.time_estimate
    if args.details:
        data["details"] = args.details

    result = api_request("POST", "/tasks", data=data)

    if args.table:
        if "error" in result:
            print(f"Error: {result['error']}")
        elif result.get("success"):
            task = result.get("data", {})
            print(f"Task created: {task.get('title')}")
            print(f"  Path: {task.get('path')}")
            print(f"  Status: {task.get('status')}")
            print(f"  Priority: {task.get('priority')}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def update_task(args):
    """Update an existing task."""
    task_id = urllib.parse.quote(args.task_id, safe="")
    data = {}

    if args.status:
        data["status"] = args.status
    if args.priority:
        data["priority"] = args.priority
    if args.title:
        data["title"] = args.title
    if args.due:
        data["due"] = args.due
    if args.scheduled:
        data["scheduled"] = args.scheduled
    if args.details:
        data["details"] = args.details

    if not data:
        print(json.dumps({"error": "No updates specified"}, ensure_ascii=False))
        return

    result = api_request("PUT", f"/tasks/{task_id}", data=data)

    if args.table:
        if "error" in result:
            print(f"Error: {result['error']}")
        elif result.get("success"):
            print(f"Task updated: {args.task_id}")
            task = result.get("data", {})
            if args.status:
                print(f"  New status: {task.get('status')}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def delete_task(args):
    """Delete a task."""
    task_id = urllib.parse.quote(args.task_id, safe="")
    result = api_request("DELETE", f"/tasks/{task_id}")

    if args.table:
        if "error" in result:
            print(f"Error: {result['error']}")
        elif result.get("success"):
            print(f"Task deleted: {args.task_id}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def get_stats(args):
    """Retrieve task statistics."""
    result = api_request("GET", "/stats")

    if args.table:
        if "error" in result:
            print(f"Error: {result['error']}")
        elif result.get("success"):
            data = result.get("data", {})
            print("Task Statistics:")
            print(f"  Total: {data.get('total', 0)}")
            print(f"  Active: {data.get('active', 0)}")
            print(f"  Completed: {data.get('completed', 0)}")
            print(f"  Overdue: {data.get('overdue', 0)}")
            print(f"  Archived: {data.get('archived', 0)}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def get_options(args):
    """Retrieve available filter options (projects, statuses, etc.)."""
    result = api_request("GET", "/filter-options")

    if args.table:
        if "error" in result:
            print(f"Error: {result['error']}")
        elif result.get("success"):
            data = result.get("data", {})
            print("Available Projects:")
            for p in data.get("projects", []):
                print(f"  - {p}")
            print("\nAvailable Statuses:")
            for s in data.get("statuses", []):
                print(f"  - {s}")
            print("\nAvailable Priorities:")
            for p in data.get("priorities", []):
                print(f"  - {p}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="TaskNotes CLI - Obsidian task management")
    parser.add_argument("--table", action="store_true", help="Human-readable output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--project", help="Filter by project")
    list_parser.add_argument("--priority", help="Filter by priority")
    list_parser.add_argument("--limit", type=int, help="Limit results")
    list_parser.add_argument("--overdue", action="store_true", help="Show only overdue tasks")
    list_parser.add_argument("--scan", action="store_true", help="Scan filesystem instead of API (finds all tasks in vault)")
    list_parser.add_argument("--all", action="store_true", help="Show all tasks including completed (implies --scan)")
    list_parser.add_argument("--table", action="store_true", help="Human-readable output")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create task")
    create_parser.add_argument("title", help="Task title")
    create_parser.add_argument("--project", help="Project/goal name")
    create_parser.add_argument("--priority", help="Task priority (see TaskNotes configuration)")
    create_parser.add_argument("--status", help="Task status (see TaskNotes configuration)")
    create_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    create_parser.add_argument("--scheduled", help="Scheduled date/time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
    create_parser.add_argument("--contexts", help="Comma-separated contexts")
    create_parser.add_argument("--time-estimate", type=int, help="Time estimate in minutes")
    create_parser.add_argument("--details", help="Task description (agent handoff context)")
    create_parser.add_argument("--table", action="store_true", help="Human-readable output")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update task")
    update_parser.add_argument("task_id", help="Task file path (e.g., Tasks/my-task.md)")
    update_parser.add_argument("--status", help="Task status (see TaskNotes configuration)")
    update_parser.add_argument("--priority", help="Task priority (see TaskNotes configuration)")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    update_parser.add_argument("--scheduled", help="Scheduled date/time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
    update_parser.add_argument("--details", help="Task description (agent handoff context)")
    update_parser.add_argument("--table", action="store_true", help="Human-readable output")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete task")
    delete_parser.add_argument("task_id", help="Task file path")
    delete_parser.add_argument("--table", action="store_true", help="Human-readable output")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Retrieve statistics")
    stats_parser.add_argument("--table", action="store_true", help="Human-readable output")

    # Options command
    options_parser = subparsers.add_parser("options", help="Retrieve filter options")
    options_parser.add_argument("--table", action="store_true", help="Human-readable output")

    args = parser.parse_args()

    commands = {
        "list": list_tasks,
        "create": create_task,
        "update": update_task,
        "delete": delete_task,
        "stats": get_stats,
        "options": get_options,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
