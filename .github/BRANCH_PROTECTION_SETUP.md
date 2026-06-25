# Branch Protection Setup Guide

This document provides step-by-step instructions for setting up branch protection rules on GitHub to enforce the project's contribution workflow.

## Overview

The Talent Factory Claude Plugins repository uses branch protection to:
- Ensure code quality through required reviews
- Prevent accidental commits to protected branches
- Enforce CI/CD checks before merging
- Maintain a clean and traceable history

### Solo-Maintainer vs. Team Setup

**Solo-Maintainer (Repository Owner only):**
- ✅ Disable "Do not allow bypassing the above settings" on main
- ✅ Allows owner to approve and merge own PRs (e.g., release PRs)
- ✅ Maintains protection against accidental direct pushes
- ✅ Full flexibility for trusted repository owner

**Team Setup (Multiple maintainers):**
- ✅ Enable "Do not allow bypassing the above settings"
- ✅ Enforces rules for all team members, including admins
- ✅ Add "Allow specified actors to bypass" for emergency situations
- ✅ Ensures proper peer review process

## Branch Strategy

This repository uses **trunk-based development**: `main` is the single long-lived branch. There is no `develop` branch (retired June 2026 — see `CHANGELOG.md`).

### Main Branch
- **Purpose:** Stable, production-ready code and the live marketplace source
- **Updates:** Only via approved Pull Requests from short-lived branches
- **Releases:** Tagged from this branch

### Feature Branches
- **Naming:** `feature/description`, `fix/description`, `docs/description`, `refactor/description`
- **Base:** Always created from `main`
- **Merge Target:** Always merge back to `main`

## GitHub Branch Protection Settings

### For Main Branch

Navigate to: **Settings → Branches → Add rule** (or edit existing rule for `main`)

#### Branch name pattern
```
main
```

#### Protect matching branches

**Require a pull request before merging**
- ✅ Enable
- Required approvals: `1`
- ✅ Dismiss stale pull request approvals when new commits are pushed
- ✅ Require review from Code Owners (optional, if CODEOWNERS file exists)
- ⬜ Restrict who can dismiss pull request reviews
- ⬜ Allow specified actors to bypass required pull requests

**Require status checks to pass before merging**
- ✅ Enable
- ✅ Require branches to be up to date before merging
- Required status checks:
  - ✅ `Validate Plugin Structure`
  - ✅ `Validate Documentation`
  - ✅ `Security Scan`
  - ✅ `Test Plugin Loading`
  - ✅ `Validate Pull Request`

**Require conversation resolution before merging**
- ✅ Enable

**Require signed commits** (optional but recommended)
- ⬜ Enable (based on team preference)

**Require linear history** (optional)
- ✅ Enable (prevents merge commits, enforces rebase or squash)

**Require deployments to succeed before merging** (if applicable)
- ⬜ Enable

**Lock branch**
- ⬜ Disable (we want to allow PRs)

**Do not allow bypassing the above settings**
- ⬜ **Disable** (empfohlen für Solo-Maintainer/Repository Owner)
  - Erlaubt Admins, eigene PRs zu genehmigen und zu mergen
  - Schützt weiterhin vor versehentlichen direkten Pushes
  - Volle Kontrolle für Repository Owner
- ✅ **Enable** (nur für Teams mit mehreren Admins)
  - Erzwingt Regeln für alle, inkl. Admins
  - Requires: "Allow specified actors to bypass" für Notfälle

**Restrict who can push to matching branches**
- ✅ Enable
- Allowed actors: (leave empty - no direct pushes)

**Allow force pushes**
- ⬜ Disable

**Allow deletions**
- ⬜ Disable

---

## Setting Up Required Status Checks

Before enabling required status checks, ensure your workflows are running correctly:

1. **Commit and push workflows** to the repository
2. **Create a test PR** to verify workflows run
3. **Check the Actions tab** to see workflow results
4. **Add status check names** exactly as they appear in GitHub Actions

Common status check names from our workflows:
- `Validate Plugin Structure` (from validate-plugins.yml)
- `Validate Documentation` (from validate-plugins.yml)
- `Security Scan` (from validate-plugins.yml)
- `Test Plugin Loading` (from validate-plugins.yml)
- `Validation Summary` (from validate-plugins.yml)
- `Validate Pull Request` (from branch-protection.yml)

## Repository Settings

### General Settings

**Settings → General**

**Pull Requests**
- ⬜ Allow merge commits (optional, based on preference)
- ✅ Allow squash merging (recommended)
  - Default commit message: `Pull request title`
- ✅ Allow rebase merging (recommended)
- ✅ Always suggest updating pull request branches
- ✅ Automatically delete head branches

**Archives**
- ⬜ Do not include Git LFS objects in archives

### Collaborators & Teams

**Settings → Collaborators and teams**

Add team members with appropriate permissions:
- **Maintainers:** Write access (can merge PRs, but still need approvals)
- **Contributors:** Read access (can fork, submit PRs)

**Recommended team structure:**
```
@talent-factory/maintainers
  - Daniel Senften (Admin)

@talent-factory/contributors
  - (External contributors - no direct access)
```

### Code Security and Analysis

**Settings → Code security and analysis**

**Dependency graph**
- ✅ Enable

**Dependabot alerts**
- ✅ Enable

**Dependabot security updates**
- ✅ Enable

**Secret scanning**
- ✅ Enable (if available in your plan)

**Code scanning** (GitHub Advanced Security)
- ✅ Enable CodeQL analysis (if available)

## CODEOWNERS File (Optional)

Create a `.github/CODEOWNERS` file to automatically request reviews:

```
# Default owners for everything
* @talent-factory/maintainers

# Plugin-specific owners
/plugins/git-workflow/ @talent-factory/git-experts
/plugins/education/ @talent-factory/education-team

# Infrastructure and CI/CD
/.github/ @talent-factory/maintainers
/docs/ @talent-factory/maintainers
```

## Labels Setup

Create the following labels for better organization:

### Type Labels
- `bug` - Something isn't working (red)
- `enhancement` - New feature or request (blue)
- `documentation` - Documentation improvements (cyan)
- `maintenance` - Maintenance and chores (gray)

### Plugin Labels
- `plugin:git-workflow` - Git workflow plugin (purple)
- `plugin:project-management` - Project management plugin (purple)
- `plugin:code-quality` - Code quality plugin (purple)
- `plugin:education` - Education plugin (purple)
- `plugin:tf-core` - TF core utilities plugin (purple)

### Size Labels
- `size/xs` - Extra small PR (<10 lines)
- `size/s` - Small PR (10-100 lines)
- `size/m` - Medium PR (100-500 lines)
- `size/l` - Large PR (500-1000 lines)
- `size/xl` - Extra large PR (>1000 lines)

### Status Labels
- `stale` - No recent activity
- `blocked` - Blocked by other work
- `work-in-progress` - Work in progress
- `first-time-contributor` - First contribution

### Priority Labels
- `priority:critical` - Critical issue
- `priority:high` - High priority
- `priority:medium` - Medium priority
- `priority:low` - Low priority

## Verification

After setting up branch protection:

1. **Test direct-push protection:**
   - Try to push directly to `main` (should fail — blocked by branch protection and the `branch-protection` workflow)

2. **Test PR workflow:**
   - Create a feature branch: `git checkout -b feature/test-branch`
   - Make a change and push
   - Create a PR to `main`
   - Verify required checks run before merge is allowed

## Troubleshooting

### Status checks not appearing
- Ensure workflows have run at least once
- Check workflow file syntax
- Verify workflow triggers include the protected branches

### Can't merge own PR as solo maintainer
- Ensure "Do not allow bypassing the above settings" is **disabled** on `main`
- With `enforce_admins: false`, the repository owner can approve and merge their own PRs

### PRs blocked incorrectly
- Check which status check is failing
- Review GitHub Actions logs
- Temporarily disable problematic checks if needed

## Maintenance

Regularly review and update:
- Branch protection rules as project grows
- Required status checks as workflows change
- Team members and permissions
- Labels and issue templates

---

**Last Updated:** January 2026
**Maintained by:** Daniel Senften, Talent Factory GmbH

For questions or issues with branch protection, please contact:
- GitHub: @talent-factory
- Email: support@talent-factory.ch
