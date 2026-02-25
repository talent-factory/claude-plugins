# Context Analysis (Brainstorm)

Comprehensive guide to the pre-implementation context analysis phase, including Superpowers integration and built-in fallback.

## Overview

The context analysis phase ensures deep understanding of the codebase and task requirements **before** any code is written. This systematic approach replaces ad-hoc exploration and reduces implementation errors.

```
Task Data (Phase 2)
    ↓
Context Analysis (Phase 3)
    ├── Superpowers Brainstorm (if available)
    └── Built-in Analysis (fallback)
    ↓
Implementation Strategy
    ↓
Agent & Plugin Resolution (Phase 4)
```

## Superpowers Integration

### What is Superpowers?

[Superpowers](https://github.com/obra/superpowers) is an agentic skills framework by Jesse Vincent (obra), officially available in the Anthropic Claude Code plugin marketplace. It provides structured development methodologies including Socratic brainstorming.

### Installation

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### How `/superpowers:brainstorm` Works

The brainstorm command initiates an interactive design session:

1. **Requirement Refinement**: Asks targeted questions about the task
2. **Edge Case Exploration**: Probes for scenarios not covered in the task description
3. **Technology Alternatives**: Explores different implementation approaches
4. **Constraint Capture**: Identifies limitations and dependencies
5. **Design Validation**: Presents a refined design for user approval

### When to Use Superpowers

| Scenario | Recommendation |
| --- | --- |
| Complex feature with unclear requirements | Strongly recommended |
| Simple bug fix with clear reproduction steps | Skip (`--skip-brainstorm`) |
| Refactoring with well-defined scope | Optional |
| New module or service creation | Strongly recommended |
| Documentation task | Skip |

### Invoking Superpowers in implement-task

```bash
# Automatic: implement-task detects Superpowers availability
/implement-task task-001
# → Phase 3 invokes /superpowers:brainstorm automatically

# Skip brainstorm for simple tasks
/implement-task task-001 --skip-brainstorm
```

## Built-in Context Analysis (Fallback)

When Superpowers is not installed, implement-task performs its own context analysis through five systematic steps.

### Step 1: Technology Stack Detection

Scan the project root and common directories for technology indicators:

```
Detection Matrix:

File                    → Technology Stack
────────────────────────────────────────────
package.json            → Node.js / JavaScript / TypeScript
tsconfig.json           → TypeScript
pom.xml                 → Java (Maven)
build.gradle.kts        → Java / Kotlin (Gradle)
requirements.txt        → Python
pyproject.toml          → Python (modern)
Cargo.toml              → Rust
go.mod                  → Go
*.csproj                → C# / .NET
Gemfile                 → Ruby
composer.json           → PHP
```

**Framework Detection** (deeper analysis):

```
Indicator                       → Framework
────────────────────────────────────────────────
src/main/java/**/*Controller*   → Spring Boot
@SpringBootApplication          → Spring Boot
django.conf.settings            → Django
fastapi import                  → FastAPI
react-dom in package.json       → React
angular.json                    → Angular
vue in package.json             → Vue.js
next.config.*                   → Next.js
```

**Output**: A structured technology profile:

```yaml
tech_profile:
  primary_language: "Java"
  framework: "Spring Boot"
  build_tool: "Gradle (Kotlin DSL)"
  test_framework: "JUnit 5"
  additional:
    - "Docker"
    - "PostgreSQL"
```

### Step 2: Affected Code Analysis

Derive affected files from the task description and acceptance criteria:

**Keyword Extraction**:

1. Parse task title, description, and acceptance criteria for:
   - Class names, function names, file names
   - Module or package references
   - API endpoint paths
   - Database table or entity names

2. Search the codebase using Grep and Glob:

```bash
# Example: Task mentions "UserService" and "/api/users"
Grep: "UserService" → src/main/java/.../UserService.java
Grep: "/api/users"  → src/main/java/.../UserController.java
Glob: "**/User*.java" → Find all user-related files
```

**Output**: List of affected files with relevance score:

```yaml
affected_files:
  - path: "src/main/java/com/example/service/UserService.java"
    relevance: "direct"  # Directly mentioned in task
  - path: "src/main/java/com/example/controller/UserController.java"
    relevance: "direct"
  - path: "src/main/java/com/example/model/User.java"
    relevance: "related"  # Same domain
  - path: "src/test/java/com/example/service/UserServiceTest.java"
    relevance: "test"  # Existing test file
```

### Step 3: Architecture Pattern Recognition

Analyze the project structure to understand conventions:

**Directory Structure Analysis**:

```
src/
├── main/java/com/example/
│   ├── controller/     → MVC pattern, REST controllers
│   ├── service/        → Service layer
│   ├── repository/     → Data access layer
│   ├── model/          → Domain entities
│   └── config/         → Configuration classes
└── test/
    └── java/com/example/
        ├── controller/  → Controller tests
        └── service/     → Service tests

→ Detected: Layered Architecture (Controller → Service → Repository)
```

**Convention Extraction**:

- Naming patterns (camelCase, snake_case, PascalCase)
- Import organization
- Documentation style (JavaDoc, docstrings, JSDoc)
- Configuration approach (annotations, YAML, properties)

**Output**: Architecture profile for implementation guidance.

### Step 4: Dependency Impact Assessment

Analyze how the task relates to other parts of the system:

**Internal Dependencies**:

- Which services/modules call the affected code?
- Which interfaces must remain stable?
- Are there shared utilities that might be affected?

**Task Dependencies** (Filesystem provider):

```markdown
# From task file:
## Dependencies
- **Requires**: task-001, task-003  ← Must be completed
- **Blocks**: task-005              ← Will be unblocked by this task
```

**External Dependencies**:

- API contracts with other services
- Database schema dependencies
- Configuration requirements

### Step 5: Implementation Strategy

Synthesize all analysis results into a concrete plan:

```yaml
implementation_strategy:
  approach: "Extend existing UserService with new method"
  steps:
    1: "Add new method signature to UserService interface"
    2: "Implement method in UserServiceImpl"
    3: "Add REST endpoint in UserController"
    4: "Write unit tests for service method"
    5: "Write integration test for endpoint"
  patterns_to_follow:
    - "Use @Transactional for service methods (existing pattern)"
    - "Return ResponseEntity<> from controllers (existing pattern)"
    - "Use @MockBean for service mocking in tests (existing pattern)"
  risks:
    - "Database migration may be needed if schema changes"
    - "Existing tests may need updating if shared fixtures change"
```

This strategy is captured as a TodoWrite checklist for Phase 7 (Implementation).

## Context Analysis Checklist

Before proceeding to Phase 4:

- [ ] Technology stack identified
- [ ] Affected files located
- [ ] Architecture patterns understood
- [ ] Dependencies assessed
- [ ] Implementation strategy defined
- [ ] TodoWrite checklist created

## Skipping Context Analysis

Use `--skip-brainstorm` when:

- Task is a simple, well-defined bug fix
- Task only involves configuration changes
- Task is purely documentation
- The developer already has deep context

```bash
/implement-task task-001 --skip-brainstorm
# → Jumps directly to Phase 4 (Agent Resolution)
```

## See Also

- [workflow.md](./workflow.md) - Complete workflow documentation
- [agent-routing.md](./agent-routing.md) - How agents are selected based on analysis
- [best-practices.md](./best-practices.md) - Implementation best practices
