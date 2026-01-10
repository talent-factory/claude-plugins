# Create Pull Request Command

Create a professional pull request with proper description and branch management.

## Context

You are helping create a pull request following best practices for code review and collaboration.

## Prerequisites

1. **Branch Status**
   - Working on a feature branch
   - All changes committed
   - Branch pushed to remote

2. **Code Quality**
   - All tests passing
   - Linters satisfied
   - No merge conflicts

## PR Template Structure

### Title Format
```
[TYPE] Brief description of changes
```

Types: `FEAT`, `FIX`, `DOCS`, `REFACTOR`, `PERF`, `TEST`, `CHORE`

### Description Template

```markdown
## Summary
Brief overview of what this PR does

## Changes
- List of key changes
- Another change
- And another

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
Describe the tests you ran and their results:
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots or GIFs demonstrating the changes

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged

## Related Issues
Closes #123
Relates to #456

## Breaking Changes
List any breaking changes and migration steps if applicable

## Additional Notes
Any additional context or notes for reviewers
```

## Workflow

1. **Verify Branch State**
   ```bash
   git status
   git log origin/main..HEAD --oneline
   git push
   ```

2. **Generate PR Description**
   - Analyze commits in the branch
   - Extract key changes
   - Identify related issues
   - Check for breaking changes

3. **Create PR**
   ```bash
   # Using GitHub CLI
   gh pr create --title "FEAT: Add user authentication" --body "$(cat pr-body.md)"
   
   # Or open browser
   gh pr create --web
   ```

## Best Practices

1. **Title**
   - Clear and descriptive
   - 50 characters or less
   - Prefix with type

2. **Description**
   - Explain the "why" not just the "what"
   - Include screenshots for UI changes
   - Link to related issues
   - Mention breaking changes prominently

3. **Size**
   - Keep PRs focused and small
   - Aim for < 400 lines of code
   - Split large features into multiple PRs

4. **Reviewers**
   - Assign appropriate reviewers
   - Add labels for categorization
   - Set project/milestone if applicable

## Interactive Mode

Ask the user:
1. What is the main purpose of this PR?
2. What commits should be included?
3. Are there related issues to link?
4. Are there breaking changes?
5. Who should review this?

Then generate the PR title and description for approval.
