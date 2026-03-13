# Pull Request Template and Best Practices

## Standard PR Template

### Basic Structure

```markdown
## Description

[Brief summary of changes in 2-3 sentences]

## Changes

- Primary change 1
- Primary change 2
- Primary change 3

## Test Plan

- [ ] Manual tests performed
- [ ] Unit tests pass
- [ ] Integration tests successful
- [ ] E2E tests performed (if applicable)

## Breaking Changes

[If applicable, list breaking changes]
[Or: "None"]

## Additional Information

[Screenshots, links, further contextual information]
```

## Description Section

### What Belongs in the Description?

**Good description**:

- **What**: What changes were made?
- **Why**: Why were these changes necessary?
- **How**: How was the problem solved?

**Example**:

```markdown
## Description

This PR implements rate limiting for all API endpoints to prevent DoS attacks.
The token bucket algorithm limits requests to 100 per minute per user.
Upon exceeding the limit, HTTP 429 is returned.
```

### Providing Context

**Helpful for reviewers**:

- Ticket/issue links
- Design documents
- Previous PRs
- Discussions

**Example**:

```markdown
## Context

This change addresses #123 and implements the design from
docs/rate-limiting-spec.md. See also #456 for related discussion.
```

## Change List

### Structured Overview

**Group by categories**:

```markdown
## Changes

### Backend

- ✨ Implement rate limiting middleware
- ♻️ Improve API error handling
- 🧪 Add integration tests for rate limiting

### Frontend

- 💎 Add error display for 429 responses
- 📚 Update user documentation

### Infrastructure

- 🔧 Configure Redis for rate limit storage
```

### Quantification

**Mention measurable changes**:

```markdown
## Changes

- ✨ Add 3 new API endpoints
- 🧪 Increase test coverage from 75% to 92%
- ⚡ Improve API response time by 40%
- 🐛 Fix 5 critical bugs
```

## Test Plan

### Comprehensive Test Checklist

```markdown
## Test Plan

### Unit Tests

- [x] All existing tests pass
- [x] 15 new tests for rate limiting added
- [x] Test coverage > 90%

### Integration Tests

- [x] Rate limiting under normal traffic
- [x] 429 response upon limit exceedance
- [x] Redis failover scenario tested

### Manual Tests

- [x] API calls with various users
- [x] Boundary tests (99, 100, 101 requests)
- [x] Performance under load

### E2E Tests

- [x] Frontend displays 429 error correctly
- [x] Retry logic functions properly
- [x] User is informed about limit

### Performance Tests

- [x] Load test with 1000 concurrent users
- [x] Latency < 10ms for rate limit check
- [x] Redis memory usage acceptable
```

### Test Results

**Include concrete figures**:

```markdown
## Test Results

- ✅ 127/127 Unit Tests passed
- ✅ 45/45 Integration Tests passed
- ✅ Load Test: 10,000 req/s without errors
- ✅ Memory: 150MB Redis (acceptable)
```

## Breaking Changes

### Clear Communication

**If breaking changes are present**:

```markdown
## Breaking Changes

### API Endpoint Changes

❌ **Removed**: `GET /api/v1/users/list`

✅ **New**: `GET /api/v2/users` (with pagination)

### Migration

For migration from v1 to v2:

1. Update API base URL to `/api/v2`
2. Implement pagination handling
3. See migration guide: docs/migration-v1-v2.md

### Deprecation Timeline

- **2024-11-01**: v1 marked as deprecated
- **2024-12-01**: v1 will be removed
```

### No Breaking Changes

**Communicate explicitly**:

```markdown
## Breaking Changes

None. This PR is fully backward compatible.
```

## Additional Information

### Screenshots

**Visualize UI changes**:

```markdown
## Screenshots

### Before

![Before](https://example.com/before.png)

### After

![After](https://example.com/after.png)

### Mobile View

![Mobile](https://example.com/mobile.png)
```

### Performance Metrics

```markdown
## Performance Comparison

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| API Latency | 150ms | 90ms | 40% |
| DB Queries | 15 | 3 | 80% |
| Memory | 500MB | 350MB | 30% |
```

### Code Examples

```markdown
## Usage

```python
# Before
user = User.query.get(id)

# After
user = UserService.get_by_id(id)  # With caching
```

## PR Title Best Practices

### Clear, Concise Titles

✅ **Good**:

```text
✨ feat: Implement rate limiting for API endpoints
🐛 fix: Resolve memory leak in WebSocket connections
♻️ refactor: Split User Service into microservices
```

❌ **Poor**:

```text
updates
fix stuff
changes
PR for feature
```

### Title Format

**Format**: `<emoji> <type>: <description>`

- **Length**: 50-70 characters
- **Language**: Consistent (English)
- **Imperative**: "Implement" not "Implementing"

## Labels and Tags

### Automatic Labels

**Based on commit types**:

- `feat` → `enhancement`, `feature`
- `fix` → `bug`, `bugfix`
- `docs` → `documentation`
- `refactor` → `refactoring`
- `perf` → `performance`
- `test` → `testing`

### Additional Labels

**Add manually**:

- `needs-review` - Awaiting review
- `work-in-progress` - Not yet complete
- `breaking-change` - Breaking changes
- `high-priority` - Urgent
- `dependencies` - Dependency updates

## Reviewer Assignment

### Whom to Assign?

**Code ownership**:

- Experts for affected modules
- Team members with context
- At least 1-2 reviewers

**CODEOWNERS** (`.github/CODEOWNERS`):

```text
# Backend
/src/api/**        @backend-team @senior-dev

# Frontend
/src/components/** @frontend-team

# Docs
/docs/**          @tech-writers
```

## Review Process

### As PR Author

**Checklist before requesting review**:

- [ ] Self-review performed
- [ ] All checks (CI/CD) are green
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Screenshots added (for UI changes)
- [ ] Breaking changes documented

### Addressing Review Comments

**Workflow**:

1. **Read comments** and understand them
2. **Clarify questions** if unclear
3. **Implement changes**
4. **Commit and push**
5. **Mark comments as "Resolved"**
6. **Allow reviewer to re-review**

## Draft vs. Ready PRs

### Draft PR

**When to use**:

```bash
/git-workflow:create-pr --draft
```

**For**:

- Work in progress
- Soliciting feedback on approach
- Testing CI/CD
- Early review

**Label**: Automatically marked as "Draft"

### Ready PR

**When to use**:

- Code is complete
- Tests pass
- Ready for review and merge

**Conversion**:

```bash
gh pr ready <pr-number>
```

## PR Size

### Ideal Size

**Recommendation**:

- **150-400 lines**: Ideal for review
- **400-800 lines**: Still acceptable
- **800+**: Too large, should be split

### Splitting Overly Large PRs

**Strategies**:

1. **By features**: Each feature in its own PR
2. **By layers**: Backend, frontend, tests
3. **By refactoring**: Refactoring → Feature
4. **Stacked PRs**: PR1 → PR2 → PR3

**Example for stacked PRs**:

```text
PR #1: ♻️ refactor: User Service refactoring
PR #2: ✨ feat: Rate limiting (based on #1)
PR #3: 🧪 test: Integration tests (based on #2)
```

## Merge Strategies

### Squash and Merge

**When**: Feature branches with many small commits

**Result**: One clean commit in main

```
Squash and Merge: ✨ feat: Implement rate limiting
```

### Rebase and Merge

**When**: Branches with a clean commit history

**Result**: All commits are transferred to main

```text
✨ feat: Rate Limiting Middleware
🧪 test: Rate Limiting Tests
📚 docs: Rate Limiting Documentation
```

### Merge Commit

**When**: Feature branches that should be preserved as a unit

**Result**: Merge commit with complete history

```
Merge pull request #123 from feature/rate-limiting
```

## PR Description Templates

### Project-Specific Templates

**GitHub Template** (`.github/pull_request_template.md`):

```markdown
## Description

<!-- Brief summary -->

## Type of Change

- [ ] 🐛 Bug Fix
- [ ] ✨ New Feature
- [ ] ♻️ Refactoring
- [ ] 📚 Documentation
- [ ] 🧪 Tests

## Test Plan

<!-- Describe how you tested -->

## Checklist

- [ ] Code follows project style guide
- [ ] Self-review performed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No merge conflicts

## Screenshots

<!-- If UI changes -->

## Related Issues

Fixes #
Relates to #
```

## Best Practices Summary

### DO ✅

- Descriptive titles and descriptions
- Comprehensive test plan
- Screenshots for UI changes
- Clearly document breaking changes
- Self-review before submission
- Small, focused PRs
- Links to issues/tickets

### DON'T ❌

- Vague titles like "Updates" or "Fixes"
- PRs without description
- Enormous PRs (1000+ lines)
- Untested code
- "WIP" without draft status
- Missing documentation
- Ignoring merge conflicts

## Automation

### GitHub Actions

**Automatic labels**:

```yaml
name: PR Labeler
on: [pull_request]
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v4
```

### PR Checks

**Required checks before merge**:

- ✅ CI/CD pipeline successful
- ✅ Code coverage > 80%
- ✅ No linting errors
- ✅ At least 1 approval
- ✅ No open comments
