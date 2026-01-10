# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The Talent Factory team takes the security of our Claude Code plugins seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to:

**security@talent-factory.ch**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

### What to Include

Please include the following information in your report:

- Type of vulnerability (e.g., code injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the vulnerability
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

This information will help us triage your report more quickly.

### What to Expect

After submitting a vulnerability report:

1. **Acknowledgment:** We'll acknowledge receipt within 48 hours
2. **Assessment:** We'll assess the vulnerability and determine its impact
3. **Fix Development:** We'll work on a fix and keep you updated on progress
4. **Disclosure:** We'll coordinate with you on the disclosure timeline
5. **Credit:** With your permission, we'll credit you in the security advisory

### Security Update Process

1. Security vulnerabilities are addressed with high priority
2. Patches are developed and tested in private
3. A security advisory is prepared
4. The fix is released with a new version
5. The security advisory is published
6. Users are notified to update

## Security Best Practices for Plugin Users

### Installation Security

- Only install plugins from trusted marketplaces
- Verify the repository URL matches official Talent Factory repositories
- Review plugin permissions before installation
- Keep Claude Code and all plugins up to date

### Configuration Security

- Never commit sensitive credentials in `.claude/settings.json`
- Use environment variables for sensitive configuration
- Review plugin source code before enabling in production
- Limit plugin access to only what's necessary

### Usage Security

- Be cautious when plugins request file system access
- Review generated code before execution
- Don't share API keys or tokens through plugin commands
- Use separate Claude Code instances for untrusted projects

## Plugin Security Guidelines for Contributors

If you're contributing to or developing plugins:

### Input Validation

- Always validate and sanitize user input
- Never execute arbitrary code without validation
- Use parameterized queries for database operations
- Escape output to prevent injection attacks

### File System Access

- Limit file system operations to necessary paths only
- Validate all file paths to prevent directory traversal
- Never execute files from untrusted sources
- Use secure file permissions

### External Dependencies

- Keep dependencies up to date
- Audit dependencies for known vulnerabilities
- Minimize use of external dependencies
- Pin dependency versions

### Sensitive Data

- Never log sensitive information
- Don't store credentials in plugin files
- Use secure methods for credential management
- Clear sensitive data from memory after use

### Code Review

- All code changes require review before merging
- Security-focused reviews for authentication/authorization changes
- Automated security scanning in CI/CD pipeline
- Regular security audits of plugin code

## Known Security Considerations

### Plugin Execution Model

Claude Code plugins execute with the same permissions as the Claude Code process. This means:

- Plugins can read/write files the user can access
- Plugins can execute system commands
- Plugins can access network resources
- Users should only install trusted plugins

### Marketplace Trust

- Official Talent Factory plugins are signed and verified
- Third-party plugins should be reviewed before installation
- Check plugin source code in public repositories
- Report suspicious plugins to security@talent-factory.ch

## Security Advisories

Security advisories for this project are published at:

- [GitHub Security Advisories](https://github.com/talent-factory/claude-plugins/security/advisories)
- [Talent Factory Security Page](https://talent-factory.ch/security)

Subscribe to these channels to stay informed about security updates.

## Vulnerability Disclosure Policy

We follow responsible disclosure practices:

- 90-day disclosure timeline for vulnerabilities
- Earlier disclosure if actively exploited in the wild
- Coordinated disclosure with affected parties
- Public acknowledgment of security researchers
- CVE assignment for significant vulnerabilities

## Bug Bounty Program

Currently, we do not have a formal bug bounty program. However, we greatly appreciate security research and will:

- Acknowledge your contribution publicly (with your permission)
- Provide swag/merchandise for significant findings
- Consider your contributions for future programs

## Contact

- **Security Issues:** security@talent-factory.ch
- **General Support:** support@talent-factory.ch
- **Website:** https://talent-factory.ch

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Claude Code Security Documentation](https://docs.claude.com/security)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

**Last Updated:** January 2026
**Maintained by:** Talent Factory GmbH Security Team
