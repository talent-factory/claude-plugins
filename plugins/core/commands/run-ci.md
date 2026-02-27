---
description: Run CI checks and fix all errors until all tests pass
allowed-tools:
  - Bash
  - Edit
  - Read
  - Glob
---

# Run CI Checks

Execute CI checks for the project and fix all errors until all tests pass.

## Usage

```bash
# Run CI checks
/core:run-ci
```

## Process

1. **Detect CI system**:
   - Check for CI configuration files:
     - `.github/workflows/*.yml` (GitHub Actions)
     - `.gitlab-ci.yml` (GitLab CI)
     - `.circleci/config.yml` (CircleCI)
     - `Jenkinsfile` (Jenkins)
     - `.travis.yml` (Travis CI)
     - `bitbucket-pipelines.yml` (Bitbucket)

2. **Detect build system**:
   - JavaScript/TypeScript: package.json scripts
   - Python: Makefile, tox.ini, setup.py, pyproject.toml
   - Go: Makefile, go.mod
   - Rust: Cargo.toml
   - Java: pom.xml, build.gradle
   - Other: Search for common CI scripts

3. **Execute CI commands**:
   - Check for CI scripts: `ci`, `test`, `check`, `validate`, `verify`
   - Common script locations:
     - `./scripts/ci.sh`, `./ci.sh`, `./run-tests.sh`
     - Package manager scripts (npm/yarn/pnpm run test)
     - Make targets (make test, make ci)
   - Activate virtual environments if needed (Python, Ruby, etc.)

4. **Fix errors**:
   - Analyze error output
   - Fix code issues, test failures, or configuration problems
   - Re-run CI checks after each fix

5. **Common CI tasks**:
   - Linting/formatting
   - Type checking
   - Unit tests
   - Integration tests
   - Build verification
   - Documentation generation

## Examples

**JavaScript/TypeScript**:
```bash
npm test           # Standard tests
npm run ci         # Full CI pipeline
npm run lint       # Linting
npm run type-check # TypeScript type checking
```

**Python**:
```bash
make test          # Makefile-based
pytest             # Direct test execution
tox                # Multi-environment testing
ruff check .       # Linting
mypy .             # Type checking
```

**Go**:
```bash
go test ./...      # All tests
make test          # Makefile-based
go vet ./...       # Code analysis
golangci-lint run  # Linting
```

**Rust**:
```bash
cargo test         # Tests
cargo check        # Check compilation
cargo clippy       # Linting
cargo fmt --check  # Check formatting
```

**Java**:
```bash
mvn test           # Maven tests
gradle test        # Gradle tests
mvn verify         # Full verification
```

## Workflow

1. **Detection**: Identify CI system and build tools
2. **Execution**: Run relevant CI checks
3. **Analysis**: On failures, analyze error output
4. **Fix**: Resolve identified problems
5. **Iteration**: Repeat until all checks pass

**Important**: Continue fixing problems and re-running CI checks until all tests pass successfully.
