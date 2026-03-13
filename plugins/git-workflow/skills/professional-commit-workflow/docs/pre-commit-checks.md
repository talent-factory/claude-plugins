# Pre-Commit Checks

Automatic quality checks based on detected project type.

## Java Projects

### Maven

```bash
mvn compile          # Compilation
mvn test            # Unit tests
mvn checkstyle:check # Code style verification
```

### Gradle

```bash
./gradlew build              # Build
./gradlew test               # Tests
./gradlew checkstyleMain     # Checkstyle
```

### Spring Boot

- Automatic detection of Spring Boot projects
- Additional validation of application properties
- Bean dependency checks

## Python Projects

### Linting

```bash
ruff check .        # Fast linting
flake8 .           # Alternative linting
pylint .           # Comprehensive linting
```

### Formatting

```bash
black .            # Code formatting
isort .            # Import sorting
```

### Type Checking

```bash
mypy .             # Static type checking
```

### Tests

```bash
pytest             # Test execution
pytest --cov       # With coverage
```

### Dependencies

- **Poetry**: `poetry check`
- **pip-tools**: `pip-compile --dry-run`
- **requirements.txt**: Dependency validation

## React/Node.js Projects

### Package Manager Detection

Automatic detection of: npm, pnpm, yarn, bun

### Linting

```bash
npm run lint       # ESLint
npx tslint         # TSLint (legacy)
```

### Formatting

```bash
npx prettier --check .   # Prettier check
```

### Type Checking

```bash
tsc --noEmit       # TypeScript compiler
```

### Tests

```bash
npm test           # Jest/Vitest
npm run test:e2e   # Cypress/Playwright
```

### Build

```bash
npm run build      # Vite/Webpack/Next.js build
```

## Documentation Projects

### LaTeX

```bash
pdflatex main.tex  # Compilation
xelatex main.tex   # Alternative engine
```

### Markdown

```bash
markdownlint **/*.md       # Linting
markdown-link-check *.md   # Link validation
```

### AsciiDoc

```bash
asciidoctor *.adoc         # Rendering
```

## Check Execution

1. **Automatic project detection**: Identifies project type based on files
2. **Relevant checks**: Executes only applicable checks
3. **Error handling**: Commit is aborted on errors
4. **Skip option**: Checks can be skipped with `--no-verify`

## Error Handling

### Build Errors

- Commit is aborted
- Errors are displayed in full
- Hint regarding the root cause

### Test Errors

- Option to skip with `--skip-tests`
- Detailed test output
- Abort only on critical errors

### Linting Issues

- Automatic fixes where possible (e.g., Black, Prettier)
- Manual fixes required for complex issues
- Warning on style guide violations
