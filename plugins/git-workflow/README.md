# Git Workflow Plugin

Professional git commands for commits, pull requests, and branch management with pre-commit validation.

## Commands

### `/commit`
Create professional git commits following conventional commit format with pre-commit validation.

**Features:**
- Conventional commit format (`type(scope): subject`)
- Pre-commit validation checks
- Interactive mode for commit message generation
- Support for breaking changes and issue references

**Usage:**
```
/commit
```

Claude will guide you through creating a proper commit message.

### `/create-pr`
Create pull requests with comprehensive descriptions and proper branch management.

**Features:**
- PR template with all necessary sections
- Branch status verification
- Related issue linking
- Breaking changes documentation
- Reviewer suggestions

**Usage:**
```
/create-pr
```

Claude will help you generate a complete PR description.

## Installation

This plugin is part of the Talent Factory marketplace. See the main repository README for installation instructions.

## Best Practices

- Always run `/commit` instead of direct git commits
- Use `/create-pr` for all pull requests to maintain consistency
- Follow the conventional commit format
- Keep PRs focused and small (< 400 lines)

## Examples

### Creating a Feature Commit
```
/commit

User: I've added OAuth2 authentication with Google and GitHub providers
Claude: [Generates commit message following conventional format]

feat(auth): add OAuth2 login support

- Implement OAuth2 authentication flow
- Add Google and GitHub providers
- Update user model with OAuth fields

Closes #123
```

### Creating a Pull Request
```
/create-pr

User: I want to create a PR for the authentication feature
Claude: [Analyzes branch and generates comprehensive PR description]
```

## Requirements

- Git installed and configured
- Working in a git repository
- GitHub CLI (`gh`) optional but recommended for `/create-pr`

## Support

For issues or questions, please open an issue in the main [claude-plugins](https://github.com/talent-factory/claude-plugins) repository.

## License

MIT
