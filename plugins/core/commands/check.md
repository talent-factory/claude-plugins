---
description: Run project checks and fix errors without committing
category: code-analysis-testing
allowed-tools: Bash, Edit, Read
---

# Run Project Validation

Execute project validation checks and resolve all errors found.

## Process

1. **Detect package manager** (for JavaScript/TypeScript projects):
   - npm: Look for package-lock.json
   - pnpm: Look for pnpm-lock.yaml
   - yarn: Look for yarn.lock
   - bun: Look for bun.lockb

2. **Check available scripts**:
   - Read package.json to find check/validation scripts
   - Common script names: `check`, `validate`, `verify`, `test`, `lint`

3. **Execute the appropriate check command**:
   - JavaScript/TypeScript:
     - npm: `npm run check` or `npm test`
     - pnpm: `pnpm check` or `pnpm test`
     - yarn: `yarn check` or `yarn test`
     - bun: `bun check` or `bun test`

   - Other languages:
     - Python: `pytest`, `flake8`, `mypy`, or `make check`
     - Go: `go test ./...` or `golangci-lint run`
     - Rust: `cargo check` or `cargo test`
     - Ruby: `rubocop` or `rake test`

4. **Fix errors**:
   - Analyze error output
   - Fix code issues, syntax errors, or test failures
   - Re-run checks after each fix

5. **Important constraints**:
   - Do NOT commit code
   - Do NOT change version numbers
   - Only fix errors to make checks pass

If no check script exists, run the most appropriate validation for the project type.
