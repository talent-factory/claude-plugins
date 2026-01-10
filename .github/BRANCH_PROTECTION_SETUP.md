# Branch Protection Setup Guide

This document provides step-by-step instructions for setting up branch protection rules on GitHub to enforce the project's contribution workflow.

## Overview

The Talent Factory Claude Plugins repository uses branch protection to:
- Ensure code quality through required reviews
- Prevent accidental commits to protected branches
- Enforce CI/CD checks before merging
- Maintain a clean and traceable history

## Branch Strategy

### Main Branch
- **Purpose:** Stable, production-ready code
- **Updates:** Only via approved Pull Requests
- **Releases:** Tagged from this branch

### Develop Branch
- **Purpose:** Integration branch for ongoing development
- **Updates:**
  - Direct commits: Maintainer (Daniel Senften) only
  - Pull Requests: All other contributors
- **Merges to Main:** Via Pull Request when ready for release

### Feature Branches
- **Naming:** `feature/description`, `fix/description`, etc.
- **Base:** Always created from `develop`
- **Merge Target:** Always merge back to `develop`

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
- ✅ Enable
- Exceptions: (leave empty to enforce for everyone)

**Restrict who can push to matching branches**
- ✅ Enable
- Allowed actors: (leave empty - no direct pushes)

**Allow force pushes**
- ⬜ Disable

**Allow deletions**
- ⬜ Disable

---

### For Develop Branch

Navigate to: **Settings → Branches → Add rule** (or edit existing rule for `develop`)

#### Branch name pattern
```
develop
```

#### Protect matching branches

**Require a pull request before merging**
- ✅ Enable
- Required approvals: `1`
- ✅ Dismiss stale pull request approvals when new commits are pushed
- ⬜ Require review from Code Owners
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

**Require signed commits** (optional)
- ⬜ Enable (based on team preference)

**Require linear history** (optional)
- ⬜ Enable or Disable (based on preference)

**Lock branch**
- ⬜ Disable

**Do not allow bypassing the above settings**
- ⬜ Disable (to allow maintainer direct commits)
- OR
- ✅ Enable with exceptions:
  - Allowed actors: `Daniel Senften` (maintainer username)

**Restrict who can push to matching branches**
- ✅ Enable
- Allowed actors:
  - `@talent-factory/maintainers` (if team exists)
  - OR individual: `Daniel Senften` (GitHub username)

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

1. **Test as maintainer:**
   ```bash
   git checkout develop
   git commit --allow-empty -m "test: direct commit to develop"
   git push origin develop
   ```
   This should succeed for the maintainer.

2. **Test PR workflow:**
   - Create a feature branch: `git checkout -b feature/test-branch`
   - Make a change and push
   - Create a PR to develop
   - Verify required checks run
   - Verify approval is required

3. **Test main branch protection:**
   - Try to push directly to main (should fail)
   - Create a PR from develop to main
   - Verify all checks are required

## Troubleshooting

### Status checks not appearing
- Ensure workflows have run at least once
- Check workflow file syntax
- Verify workflow triggers include the protected branches

### Can't push to develop as maintainer
- Check "Restrict who can push" settings
- Verify your GitHub username is listed in allowed actors
- Ensure "Do not allow bypassing" has appropriate exceptions

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
