#!/usr/bin/env python3
"""Branch management for PR workflow"""
import subprocess

class BranchManager:
    PROTECTED = ['main', 'master', 'develop']
    
    def __init__(self):
        self.current = self._get_current_branch()
        
    def _get_current_branch(self):
        return subprocess.run(['git', 'branch', '--show-current'], 
                            capture_output=True, text=True).stdout.strip()
    
    def ensure_feature_branch(self):
        if self.current in self.PROTECTED:
            print(f"⚠️  Auf geschütztem Branch: {self.current}")
            # Create new feature branch
            return self._create_feature_branch()
        print(f"✓ Auf Feature-Branch: {self.current}")
        return True
        
    def _create_feature_branch(self):
        from datetime import date
        branch = f"feature/changes-{date.today()}"
        try:
            subprocess.run(['git', 'checkout', '-b', branch], check=True)
            print(f"✓ Branch erstellt: {branch}")
            return True
        except:
            return False
            
    def has_commits(self):
        result = subprocess.run(['git', 'log', '-1'], capture_output=True)
        return result.returncode == 0
