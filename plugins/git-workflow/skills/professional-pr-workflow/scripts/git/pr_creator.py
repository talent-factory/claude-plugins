#!/usr/bin/env python3
"""PR creation via GitHub CLI"""
import subprocess

class PRCreator:
    def __init__(self, draft=False, target='main'):
        self.draft = draft
        self.target = target
        
    def create(self):
        # Push branch
        if not self._push():
            return False
        # Create PR
        return self._create_pr()
        
    def _push(self):
        branch = subprocess.run(['git', 'branch', '--show-current'],
                              capture_output=True, text=True).stdout.strip()
        try:
            subprocess.run(['git', 'push', '-u', 'origin', branch], check=True)
            print(f"✓ Branch gepusht: origin/{branch}")
            return True
        except:
            print("✗ Push fehlgeschlagen")
            return False
            
    def _create_pr(self):
        cmd = ['gh', 'pr', 'create', '--base', self.target, '--fill']
        if self.draft:
            cmd.append('--draft')
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✓ PR erstellt")
            print(result.stdout)
            return True
        except:
            print("✗ PR-Erstellung fehlgeschlagen")
            return False
