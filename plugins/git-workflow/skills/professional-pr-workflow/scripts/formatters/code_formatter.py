#!/usr/bin/env python3
"""Code formatting orchestrator"""
import subprocess
import os

class CodeFormatter:
    def format_all(self):
        print("\n" + "=" * 60)
        print("  Code-Formatierung")
        print("=" * 60)
        
        # JavaScript/TypeScript
        if os.path.exists('package.json'):
            self._run_formatter(['npx', 'biome', 'format', '--write', '.'], 'Biome')
            
        # Python
        if any(os.path.exists(f) for f in ['pyproject.toml', 'requirements.txt']):
            self._run_formatter(['black', '.'], 'Black')
            self._run_formatter(['isort', '.'], 'isort')
            
    def _run_formatter(self, cmd, name):
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ {name}: Formatierung erfolgreich")
        except:
            print(f"⚠️  {name}: Nicht verfügbar oder Fehler")
