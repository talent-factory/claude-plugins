#!/usr/bin/env python3
"""Detect project type based on files and structure."""

import os
from pathlib import Path
from typing import List, Optional


class ProjectDetector:
    """Detect project type for validation."""

    def __init__(self, project_root: Optional[str] = None):
        self.project_root = project_root or os.getcwd()

    def detect_all(self) -> List[str]:
        """Detect all applicable project types."""
        project_types = []

        if self.is_java():
            project_types.append('java')

        if self.is_python():
            project_types.append('python')

        if self.is_react():
            project_types.append('react')

        if self.is_docs():
            project_types.append('docs')

        return project_types

    def is_java(self) -> bool:
        """Check if this is a Java project."""
        indicators = [
            'pom.xml',
            'build.gradle',
            'build.gradle.kts',
            'gradlew',
        ]
        return any(self._file_exists(ind) for ind in indicators)

    def is_python(self) -> bool:
        """Check if this is a Python project."""
        indicators = [
            'pyproject.toml',
            'requirements.txt',
            'setup.py',
            'Pipfile',
            'poetry.lock',
        ]
        return any(self._file_exists(ind) for ind in indicators)

    def is_react(self) -> bool:
        """Check if this is a React/Node.js project."""
        if not self._file_exists('package.json'):
            return False

        # Check package.json for React/Vue/Svelte
        try:
            import json
            package_json = Path(self.project_root) / 'package.json'
            with open(package_json) as f:
                data = json.load(f)
                deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                return any(key in deps for key in ['react', 'next', 'vue', 'svelte', 'angular'])
        except:
            return False

    def is_docs(self) -> bool:
        """Check if this is a documentation project."""
        # Count documentation files
        tex_count = len(list(Path(self.project_root).glob('**/*.tex')))
        md_count = len(list(Path(self.project_root).glob('**/*.md')))
        adoc_count = len(list(Path(self.project_root).glob('**/*.adoc')))

        # Consider it a docs project if:
        # - Has LaTeX files, OR
        # - Has more than 2 markdown files (not just README/LICENSE), OR
        # - Has AsciiDoc files
        return tex_count > 0 or md_count > 2 or adoc_count > 0

    def get_primary_type(self) -> Optional[str]:
        """Get the primary/dominant project type."""
        types = self.detect_all()
        if not types:
            return None

        # Priority order: react > java > python > docs
        priority = ['react', 'java', 'python', 'docs']
        for ptype in priority:
            if ptype in types:
                return ptype

        return types[0]

    def _file_exists(self, filename: str) -> bool:
        """Check if file exists in project root."""
        return os.path.isfile(os.path.join(self.project_root, filename))


def main():
    """CLI interface for project detector."""
    import sys

    detector = ProjectDetector()
    types = detector.detect_all()

    if not types:
        print("No project type detected")
        sys.exit(1)

    print(f"Detected project types: {', '.join(types)}")
    print(f"Primary type: {detector.get_primary_type()}")


if __name__ == '__main__':
    main()
