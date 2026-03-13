# Resolution Strategies for Merge Conflicts

## Strategy Overview

The `/git-workflow:resolve-conflicts` command supports three strategies:

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `smart` | Semantic analysis and intelligent merging | Default, best results |
| `ours` | Retain our version on conflicts | Feature branch takes precedence |
| `theirs` | Retain their version on conflicts | Target branch takes precedence |

## Smart Strategy: Decision Tree

The smart strategy analyzes each conflict individually and selects the optimal resolution. The decision tree comprises 5 levels:

### Level 1: Generated Files

**Detection**: Lock files, build artifacts, generated types

```
uv.lock, bun.lockb, package-lock.json, yarn.lock
*.generated.ts, *.generated.py
```

**Strategy**: `checkout --theirs` + regeneration

**Rationale**: Generated files are derived from source files. After resolving all source conflicts, they are regenerated, thereby correctly reflecting both sides.

### Level 2: Additive Changes

**Detection**: Both sides add new elements without modifying existing ones

Typical cases:
- **Import blocks**: New imports on both sides
- **Route registrations**: New API endpoints
- **Configuration lists**: New dependencies, new plugins
- **Export lists**: New modules exported

**Strategy**: Union (merge both sides)

```python
# Conflict in __init__.py
<<<<<<< HEAD
from .auth import router as auth_router
from .email import router as email_router
=======
from .auth import router as auth_router
from .campaigns import router as campaign_router
>>>>>>> origin/develop

# Resolution: Union
from .auth import router as auth_router
from .campaigns import router as campaign_router
from .email import router as email_router
```

**Sorting**: Sort imports and lists alphabetically for consistency.

### Level 3: Same Location Modified

**Detection**: Both sides modify the same code block

**Strategy**: Context analysis

1. **Function signature changed**: Compare both signatures, choose compatible version
2. **Function body changed**: Understand logic from both sides, merge if possible
3. **Conflicting logic**: Prioritize our version (`ours`), as the feature branch represents active work

```python
# Conflict: Both modify the same function
<<<<<<< HEAD
def send_email(to: str, subject: str, template: str) -> SendResult:
    """With template support."""
    rendered = render_template(template)
    return provider.send(to, subject, rendered)
=======
def send_email(to: str, subject: str, body: str, priority: int = 0) -> SendResult:
    """With priority support."""
    return provider.send(to, subject, body, priority=priority)
>>>>>>> origin/develop

# Resolution: Merge features
def send_email(
    to: str,
    subject: str,
    template: str,
    priority: int = 0,
) -> SendResult:
    """With template and priority support."""
    rendered = render_template(template)
    return provider.send(to, subject, rendered, priority=priority)
```

### Level 4: Structural Changes

**Detection**: One side has altered the file structure (split class, renamed module, refactored API)

**Strategy**: Manual intervention recommended

- Present both versions to the user
- Explain what structural changes were made
- Present options:
  1. Retain our structure, integrate their functionality
  2. Adopt their structure, integrate our functionality
  3. User decides manually

### Level 5: Architectural Conflicts

**Detection**: Fundamental design decisions diverge

Examples:
- Synchronous vs. asynchronous code
- Different data models
- Different dependency injection patterns

**Strategy**: **HALT** - Always consult the user

These conflicts cannot be resolved automatically, as they require architectural decisions.

## File Type-Specific Strategies

### Python Files (`.py`)

| Conflict Type | Strategy | Details |
|---------------|----------|---------|
| Import block | Union + isort | Alphabetical, grouped by stdlib/third-party/local |
| `__init__.py` exports | Union | Retain all exports |
| `__all__` list | Union + sort | Merge entries |
| Function signatures | Smart merge | Parameters from both sides |
| Type hints | Retain newer/more complete | Union types if necessary |
| Decorators | Retain both | Verify ordering |

### TypeScript/JavaScript Files (`.ts`, `.tsx`, `.js`, `.jsx`)

| Conflict Type | Strategy | Details |
|---------------|----------|---------|
| Import block | Union + sort | Merge named imports |
| Interface extension | Union | Properties from both sides |
| Type definitions | Union type | `TypeA \| TypeB` if necessary |
| JSX components | Context analysis | Merge props and children |
| Barrel exports (`index.ts`) | Union | Retain all re-exports |

### JSON/YAML Files

| Conflict Type | Strategy | Details |
|---------------|----------|---------|
| `dependencies` | Union, higher version | Retain both dependencies |
| `devDependencies` | Union, higher version | Retain both devDeps |
| `scripts` | Union | Retain both scripts |
| Configuration values | Target version | Target branch configuration |
| Array values | Union + deduplicate | Retain unique values |

### Alembic Migrations

| Conflict Type | Strategy | Details |
|---------------|----------|---------|
| `down_revision` | Linearize chain | Correctly link revisions |
| Multiple heads | Merge migration | `alembic merge heads` |
| Same table modified | Verify ordering | Consider dependencies |

**Alembic special handling**:

```bash
# Detect multiple heads
alembic heads

# If multiple heads: Create merge migration
alembic merge heads -m "merge_migrations"

# Validate chain
alembic history --verbose
```

### Lock Files

| File | Strategy | Regeneration |
|------|----------|--------------|
| `uv.lock` | `--theirs` + regenerate | `uv lock` |
| `bun.lockb` | `--theirs` + regenerate | `bun install` |
| `package-lock.json` | `--theirs` + regenerate | `npm install` |
| `yarn.lock` | `--theirs` + regenerate | `yarn install` |
| `Gemfile.lock` | `--theirs` + regenerate | `bundle install` |

## Ours Strategy

**Usage**: `--strategy ours`

For each conflict, our version (HEAD) is retained:

```bash
git checkout --ours <file>
git add <file>
```

**Use cases**:
- Feature branch takes precedence and target changes are irrelevant
- Deliberate decision to disregard target changes
- Rapid resolution when conflicts are purely cosmetic

**Risks**:
- Target changes are lost
- New features/fixes from the target are not integrated
- May lead to regressions

## Theirs Strategy

**Usage**: `--strategy theirs`

For each conflict, the target version is retained:

```bash
git checkout --theirs <file>
git add <file>
```

**Use cases**:
- Target branch (e.g., develop) takes precedence
- Own changes should be overwritten
- Rebase-like behavior desired

**Risks**:
- Own changes are lost
- Feature work may need to be repeated

## Strategy Selection: Recommendation

```
Merge conflict detected
    │
    ├── Lock file?
    │   └── YES → theirs + regenerate
    │
    ├── Generated file?
    │   └── YES → theirs + regenerate
    │
    ├── Only additive changes?
    │   └── YES → Union (retain both)
    │
    ├── Same location modified?
    │   ├── Compatible changes? → Smart merge
    │   └── Incompatible? → Ours (prioritize feature)
    │
    ├── Structural change?
    │   └── YES → Consult user
    │
    └── Architectural conflict?
        └── YES → HALT, user decides
```

**Rule of thumb**: When in doubt, use `smart`. Only select `ours`/`theirs` when it is clear that one side should take complete precedence.
