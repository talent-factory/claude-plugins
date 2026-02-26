# Handoff Best Practices

## Fundamental Principles

### 1. Write Self-Explanatory Documentation

The subsequent agent possesses **no prior context**. Compose documentation such that an individual without background knowledge can comprehend it immediately:

**Appropriate:**

> The function `validateUser()` in `src/auth/validator.ts:45` throws a TypeError because `user.roles` is undefined when the user authenticates via OAuth. The role must be extracted from the OAuth token (refer to `src/auth/oauth.ts:123`).

**Inappropriate:**

> The validation does not function for OAuth users.

### 2. Maintain Specificity

Always provide concrete file paths and line numbers:

| Inappropriate        | Appropriate                                               |
| -------------------- | --------------------------------------------------------- |
| "in the Auth module" | `src/auth/validator.ts:45-67`                             |
| "adjust the config"  | `config/database.yml:12` (change value from X to Y)       |
| "fix test"           | `tests/unit/auth.test.ts:89` (`describe` block for OAuth) |

### 3. Document Failed Attempts

**Rationale**: Prevents the subsequent agent from repeating identical errors.

**Elements to Document**:

- What approach was attempted?
- What error message was produced?
- Why did the approach fail?
- What insights were derived from this experience?

### 4. Establish Prioritization

Always order subsequent steps by priority:

```markdown
### Priority 1: [Blocking]

### Priority 2: [Important]

### Priority 3: [Nice-to-have]
```

## DO: Best Practices

### Prior to Handoff Creation

- Commit changes (when feasible)
- Verify and document Git status
- Record outstanding questions
- Copy error messages verbatim (do not paraphrase)

### Within the Documentation

- **Explain context**: Why was a particular action taken?
- **Include file paths with line numbers**: `file.py:123` or `file.py:123-145`
- **Provide code examples**: Demonstrate important patterns
- **Include screenshots/logs**: For UI issues or complex errors
- **Add links**: To relevant documentation, issues, and pull requests

### For the Subsequent Agent

- **Summary**: 2-3 sentences highlighting the most critical information
- **Initial step**: A concrete starting point
- **Warnings**: What should be avoided?

## DON'T: Common Mistakes

### Content-Related Errors

- **Vague descriptions**: "Code does not function"
- **Missing contextual information**: Symptoms only, no causes
- **Implicit assumptions**: "As discussed" (when no discussion occurred)
- **Incomplete error messages**: Only the final line

### Security Violations

- **Documenting secrets**: API keys, passwords, tokens
- **Credentials in code examples**: Including as placeholders
- **Private URLs**: Internal dashboards, admin panels

### Structural Errors

- **Excessive document length**: Maintain focus on essential elements
- **Absence of prioritization**: Treating all items as equally important
- **Missing subsequent steps**: Documenting only the current state

## Quality Checklist

### Verification Prior to Saving

```markdown
## Content

- [ ] Original task clearly described
- [ ] All relevant changes documented
- [ ] Failed attempts with rationale
- [ ] Subsequent steps prioritized
- [ ] File paths with line numbers

## Security

- [ ] No API keys or tokens
- [ ] No passwords or credentials
- [ ] No internal URLs (except Linear issues)

## Usability

- [ ] Self-explanatory without prior knowledge
- [ ] Concrete action instructions
- [ ] Summary for rapid orientation
```

## Special Situations

### For Complex Bugs

```markdown
## Symptom

[What is occurring?]

## Reproduction Steps

1. [Step 1]
2. [Step 2]
3. [Error manifests]

## Expected Behavior

[What should occur?]

## Analysis to Date

- Hypothesis A: [Description] → [Result]
- Hypothesis B: [Description] → [Result]

## Suspected Locations

- `file.py:123` - [Rationale for suspicion]
```

### For Feature Development

```markdown
## Implementation Status

| Component   | Status      | File                     |
| ----------- | ----------- | ------------------------ |
| Backend API | Complete    | `api/routes.py`          |
| Frontend UI | In Progress | `components/Feature.tsx` |
| Tests       | Pending     | -                        |

## Architectural Decisions

- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]
```

### For Team Handovers

Additional information for human developers:

```markdown
## Context for Developers

- **Deadline**: [If applicable]
- **Stakeholders**: [Who is awaiting this feature?]
- **Dependencies**: [Other teams/services]
- **Review required**: [Yes/No, by whom]
```

## Example: Before and After

### Before (Inappropriate)

> The auth does not work. Tried various approaches. Still needs to be fixed.

### After (Appropriate)

> **Problem**: OAuth login throws TypeError on `user.roles` (undefined).
>
> **Cause**: OAuth provider delivers roles in the `permissions` field, not `roles`.
>
> **Failed Attempt**: Direct mapping in `oauth.ts:45` → Broke existing email authentication.
>
> **Subsequent Step**: Implement adapter pattern in `src/auth/adapters/` to normalize both formats. Refer to `src/auth/adapters/email.ts` as reference.

## Workflow Integration

### With /compact

```bash
# 1. Prior to Compact: Create handoff
/project-management:document-handoff "Feature Name"

# 2. Execute Compact
/compact

# 3. After Compact: Load handoff
"Read .claude/handoffs/2026-01-14_feature-name.md and continue working."
```

### With Linear

```bash
# Link handoff with Linear issue
/project-management:document-handoff --linear-issue TF-123

# Handoff automatically references:
# - Issue details
# - Acceptance criteria
# - Linked issues
```

### With Git Workflow

```bash
# Prior to handoff: Commit changes
/git-workflow:commit "WIP: Feature in progress"

# Then create handoff
/project-management:document-handoff

# Handoff automatically includes:
# - Branch name
# - Recent commits
# - Uncommitted changes
```
