# Quality Gate

Comprehensive guide to the automated quality gate phase in implement-task.

## Overview

The quality gate (Phase 8) ensures code quality, security, and consistency **before** the PR is finalized for review. It acts as an automated first reviewer, catching issues early and reducing review cycles.

```
Implementation Complete (Phase 7)
    ↓
Quality Gate (Phase 8)
    ├── Step 1: Automated Code Review
    ├── Step 2: Language-Specific Linting
    ├── Step 3: Acceptance Criteria Verification
    └── Step 4: Commit Standardization
    ↓
All Passed? → PR Finalization (Phase 9)
    or
Issues Found? → Fix → Re-run Quality Gate
```

## Step 1: Automated Code Review

### Invoking the Code Reviewer

The `@code-reviewer` agent from the `code-quality` plugin is invoked on all changes:

```bash
# Generate diff for review
git diff main...HEAD
```

### Review Checklist

The code reviewer evaluates against these categories:

#### Fundamental Quality

- [ ] Code is simple and readable
- [ ] Functions and variables are descriptively named
- [ ] No code duplication
- [ ] Complex logic is appropriately commented
- [ ] Consistent code formatting and style

#### Security

- [ ] No exposed secrets or API keys
- [ ] Input validation implemented
- [ ] Protection against common vulnerabilities (SQL injection, XSS, etc.)
- [ ] Secure authentication and authorization

#### Robustness

- [ ] Proper error handling
- [ ] Graceful degradation on failure
- [ ] Appropriate logging strategies
- [ ] Resource management (memory leaks, database connections)

#### Maintainability

- [ ] Modular, testable code
- [ ] Good test coverage (unit, integration, end-to-end)
- [ ] Documentation for complex algorithms
- [ ] Adherence to project conventions

#### Performance

- [ ] Algorithm efficiency considered
- [ ] Database queries optimized
- [ ] Caching strategies where appropriate
- [ ] Memory and CPU consumption reasonable

### Review Output

The code reviewer produces categorized feedback:

**Critical Issues** (must be resolved):
- Security vulnerabilities
- Functional errors
- Performance problems

**Warnings** (should be resolved):
- Code quality issues
- Maintainability concerns
- Minor security considerations

**Suggestions** (for consideration):
- Optimization opportunities
- Best practice recommendations
- Refactoring suggestions

### Handling Review Results

```python
def handle_review_results(review):
    if review.critical_issues:
        # MUST fix before proceeding
        for issue in review.critical_issues:
            fix_issue(issue)
        # Re-run review after fixes
        return rerun_review()

    if review.warnings:
        # SHOULD fix, but can proceed with user approval
        present_warnings_to_user()
        if user_approves_proceeding():
            return proceed_to_linting()
        else:
            fix_warnings()
            return rerun_review()

    # No issues or only suggestions
    return proceed_to_linting()
```

## Step 2: Language-Specific Linting

Based on the technology stack detected in Phase 3, run appropriate linting tools:

### Python Projects

```bash
# Via code-quality plugin
/code-quality:ruff-check

# Ruff checks include:
# - PEP 8 compliance
# - Import sorting
# - Type annotation suggestions
# - Common Python anti-patterns
# - Security issues (bandit rules)
```

**Auto-fix**: Ruff can automatically fix many issues:

```bash
# If ruff-check reports fixable issues
ruff check --fix .
ruff format .
```

### JavaScript / TypeScript Projects

```bash
# Use project-configured linter
npx eslint . --ext .ts,.tsx,.js,.jsx
# or
npx biome check .
```

### Java Projects

```bash
# Gradle-based projects
./gradlew check
./gradlew spotbugsMain  # If SpotBugs is configured

# Checkstyle (if configured)
./gradlew checkstyleMain
```

### Other Languages

| Language | Linting Tool | Command |
| --- | --- | --- |
| Go | `go vet`, `golangci-lint` | `golangci-lint run` |
| Rust | `clippy` | `cargo clippy` |
| C# | `.NET analyzers` | `dotnet build /p:TreatWarningsAsErrors=true` |
| Ruby | `rubocop` | `rubocop` |

### Linting Failure Handling

```python
def handle_linting_results(results):
    if results.errors:
        # Fix automatically where possible
        auto_fix_count = auto_fix_linting_issues(results)

        remaining = results.errors - auto_fix_count
        if remaining > 0:
            # Present remaining issues to user
            present_linting_issues(remaining)
            # User decides: fix manually or proceed
    else:
        proceed_to_acceptance_check()
```

## Step 3: Acceptance Criteria Verification

Systematically verify each acceptance criterion from the task file:

### Verification Process

```
For each acceptance criterion:
    1. Is it implemented?
       → Check: Code changes address the criterion
    2. Is it tested?
       → Check: Test file covers the criterion
    3. Does the test pass?
       → Check: Run test suite, verify green
```

### Example Verification

```yaml
Task: "Add user login with Google OAuth"

Acceptance Criteria:
  - "User can click 'Sign in with Google' button"
    → Implementation: LoginPage.tsx contains GoogleSignInButton
    → Test: LoginPage.test.tsx has "renders Google sign-in button"
    → Result: PASS

  - "OAuth flow redirects to Google consent screen"
    → Implementation: AuthService.java has googleOAuthRedirect()
    → Test: AuthServiceTest.java has "redirects to Google"
    → Result: PASS

  - "Successful login creates user session"
    → Implementation: SessionService.java has createSession()
    → Test: SessionServiceTest.java has "creates session after OAuth"
    → Result: PASS

Verification: ALL CRITERIA MET ✓
```

### Handling Unmet Criteria

```python
def verify_acceptance_criteria(task, changes):
    results = []
    for criterion in task.acceptance_criteria:
        implemented = check_implementation(criterion, changes)
        tested = check_test_coverage(criterion)
        passing = run_relevant_tests(criterion)

        results.append({
            "criterion": criterion,
            "implemented": implemented,
            "tested": tested,
            "passing": passing
        })

    unmet = [r for r in results if not all([r["implemented"], r["tested"], r["passing"]])]

    if unmet:
        # Present unmet criteria to user
        for r in unmet:
            if not r["implemented"]:
                warn(f"Criterion not implemented: {r['criterion']}")
            elif not r["tested"]:
                warn(f"Criterion not tested: {r['criterion']}")
            elif not r["passing"]:
                warn(f"Test failing for: {r['criterion']}")

        # User decides: fix now or proceed
        return ask_user_decision(unmet)

    return all_criteria_met()
```

## Step 4: Commit Standardization

Ensure all commits follow the project's Emoji Conventional Commits format.

### Using `/git-workflow:commit`

The `git-workflow` plugin ensures standardized commits:

```bash
# Instead of manual git commit
/git-workflow:commit
```

This produces commits in the format:

```
<emoji> <type>: <description>

[optional body]
```

### Commit Review

Before finalization, review the commit history:

```bash
# Review commits on this branch
git log main..HEAD --oneline
```

**Expected Pattern**:

```
✨ feat: Add GoogleSignInButton component
🧪 test: Add LoginPage integration tests
✨ feat: Implement OAuth redirect in AuthService
🧪 test: Add AuthService unit tests
📚 docs: Update API documentation for OAuth endpoints
```

**Anti-Pattern** (flag for cleanup):

```
fix stuff
WIP
more changes
another try
```

### Interactive Rebase (if needed)

If commits do not follow conventions, suggest interactive cleanup:

```bash
# Squash and reformat commits
git rebase -i main
```

## Quality Gate Configuration

### Skip Quality Gate

For urgent fixes or trivial changes:

```bash
/implement-task task-001 --skip-quality-gate
```

**When to skip**:

- Hotfix for production issue (time-critical)
- Trivial typo fix
- Configuration-only change
- User explicitly requests it

**When NOT to skip**:

- New feature implementation
- Security-related changes
- Public API modifications
- Database schema changes

### Partial Quality Gate

Individual steps can be customized based on project needs:

```yaml
# Future: Quality gate configuration in task file
quality_gate:
  code_review: true
  linting: true
  acceptance_verification: true
  commit_standardization: true
```

## Quality Gate Checklist

Before proceeding to Phase 9 (PR Finalization):

- [ ] **Code Review**: No critical issues remaining
- [ ] **Linting**: All language-specific checks passed
- [ ] **Acceptance Criteria**: All criteria implemented, tested, and passing
- [ ] **Commits**: Following Emoji Conventional Commits format
- [ ] **No Secrets**: No credentials, API keys, or tokens in code
- [ ] **Tests Passing**: All test suites green

## Metrics and Reporting

After the quality gate completes, a summary is generated:

```
╔══════════════════════════════════════════════╗
║  Quality Gate Summary: task-001              ║
╠══════════════════════════════════════════════╣
║                                              ║
║  Code Review:                                ║
║  ├── Critical:   0 issues                    ║
║  ├── Warnings:   2 issues (resolved)         ║
║  └── Suggestions: 1 (noted for future)       ║
║                                              ║
║  Linting:                                    ║
║  ├── Errors:     0                           ║
║  └── Auto-fixed: 3 issues                    ║
║                                              ║
║  Acceptance Criteria: 5/5 verified           ║
║  Commits: 4 (all follow conventions)         ║
║                                              ║
║  Result: PASSED ✓                            ║
╚══════════════════════════════════════════════╝
```

## See Also

- [context-analysis.md](./context-analysis.md) - Pre-implementation analysis
- [agent-routing.md](./agent-routing.md) - Agent selection that feeds into review
- [best-practices.md](./best-practices.md) - Commit and PR standards
- [workflow.md](./workflow.md) - Complete workflow documentation
