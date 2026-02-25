# Agent & Plugin Routing

Comprehensive guide to the automatic agent and plugin selection logic in implement-task.

## Overview

Phase 4 (Agent & Plugin Resolution) automatically determines the optimal combination of agents and plugins for each task. This eliminates manual agent selection and ensures consistent quality across implementations.

```
Context Analysis Results (Phase 3)
    ↓
Agent Resolution Algorithm
    ├── 1. Explicit Recommendation (from task file)
    ├── 2. Technology Stack Match
    ├── 3. Label-Based Match
    └── 4. Default (no specific agent)
    ↓
Plugin Dependency Resolution
    ↓
Implementation Phase (Phase 7)
```

## Agent Resolution Algorithm

### Priority 1: Explicit Agent Recommendation

If the task file contains an agent recommendation (created by `/create-plan`), this takes highest priority:

```markdown
## Agent Recommendation

**Recommended Agent**: `java-developer`

**Rationale**:
Spring Boot REST controller with service layer logic.
Enterprise Java pattern expertise required.
```

**Parsing**:

```python
# Extract from task file
agent_recommendation = parse_section("Agent Recommendation")
if agent_recommendation:
    resolved_agent = agent_recommendation.agent
    # → Skip further resolution
```

### Priority 2: Technology Stack Detection

Based on the technology profile from context analysis:

```python
def resolve_by_tech_stack(tech_profile):
    mapping = {
        # Java ecosystem
        ("Java", "Spring Boot"):    "java-developer",
        ("Java", "Gradle"):         "java-developer",
        ("Kotlin", "Spring Boot"):  "java-developer",

        # Python ecosystem
        ("Python", "Django"):       "python-expert",
        ("Python", "FastAPI"):      "python-expert",
        ("Python", "Flask"):        "python-expert",
        ("Python", None):           "python-expert",

        # Frontend ecosystem
        ("TypeScript", "React"):    "frontend-developer",
        ("JavaScript", "React"):    "frontend-developer",
        ("TypeScript", "Angular"):  "frontend-developer",
        ("TypeScript", "Vue"):      "frontend-developer",

        # Documentation
        ("Markdown", None):         "markdown-syntax-formatter",
    }

    key = (tech_profile.primary_language, tech_profile.framework)
    return mapping.get(key, mapping.get((tech_profile.primary_language, None)))
```

### Priority 3: Label-Based Matching

If technology detection yields no result, use task labels:

| Task Labels | Resolved Agent |
| --- | --- |
| `java`, `spring`, `backend` | `java-developer` |
| `python`, `django`, `fastapi` | `python-expert` |
| `frontend`, `react`, `ui`, `component` | `frontend-developer` |
| `docs`, `documentation`, `readme` | `markdown-syntax-formatter` |
| `ai`, `llm`, `ml`, `machine-learning` | `ai-engineer` |
| `agent`, `multi-agent`, `orchestration` | `agent-expert` |
| `review`, `audit`, `security` | `code-reviewer` |

### Priority 4: Default (No Specific Agent)

If no agent can be resolved, the implementation proceeds without a specialized agent. The general implementation methodology applies, guided by the context analysis results.

## Available Agents

### From `code-quality` Plugin

#### `@code-reviewer`

**Expertise**: Code quality, security analysis, performance review, best practice validation.

**Used in**:
- Phase 8 (Quality Gate): Automated review of all changes
- Phase 4: Proactive assignment for security-critical tasks

**Cross-Plugin Reference**: `@code-quality:code-reviewer`

#### `@python-expert`

**Expertise**: Python development (Django, FastAPI), data science, async programming, PEP 8 compliance.

**Used in**: Phase 7 (Implementation) for Python tasks.

**Cross-Plugin Reference**: `@code-quality:python-expert`

#### `@frontend-developer`

**Expertise**: React, TypeScript, frontend architecture, component design, responsive development.

**Used in**: Phase 7 (Implementation) for frontend tasks.

**Cross-Plugin Reference**: `@code-quality:frontend-developer`

### From `development` Plugin

#### `@java-developer`

**Expertise**: Java/Spring Boot, enterprise patterns, Gradle Kotlin DSL, JPA/Hibernate, JUnit 5.

**Used in**: Phase 7 (Implementation) for Java tasks.

**Cross-Plugin Reference**: `@development:java-developer`

### From `education` Plugin

#### `@markdown-syntax-formatter`

**Expertise**: Markdown formatting (CommonMark), documentation structure, best practice Markdown.

**Used in**: Phase 7 (Implementation) for documentation tasks.

**Cross-Plugin Reference**: `@education:markdown-syntax-formatter`

### From Agent Mapping (Not Plugin-Bound)

#### `@ai-engineer`

**Expertise**: LLM integration, ML pipelines, vector databases, prompt engineering.

**Note**: Referenced in agent-mapping but may not have a dedicated agent file. Serves as a role descriptor for context-aware implementation.

#### `@agent-expert`

**Expertise**: AI agent development, multi-agent systems, agent orchestration.

**Note**: Referenced in agent-mapping but may not have a dedicated agent file.

## Plugin Dependency Resolution

After agent resolution, determine which plugins and commands are needed:

### Always Required

| Plugin | Command | Phase | Purpose |
| --- | --- | --- | --- |
| `git-workflow` | `/git-workflow:create-pr` | 5b | Draft PR creation |
| `git-workflow` | `/git-workflow:commit` | 7, 8 | Standardized commits |

### Conditionally Required

| Plugin | Command / Agent | Condition | Phase |
| --- | --- | --- | --- |
| `superpowers` (obra) | `/superpowers:brainstorm` | Installed AND not `--skip-brainstorm` | 3 |
| `code-quality` | `@code-reviewer` | Not `--skip-quality-gate` | 8 |
| `code-quality` | `/ruff-check` | Python project detected | 8 |
| `code-quality` | `@python-expert` | Python resolved as agent | 7 |
| `code-quality` | `@frontend-developer` | Frontend resolved as agent | 7 |
| `development` | `@java-developer` | Java resolved as agent | 7 |
| `education` | `@markdown-syntax-formatter` | Docs resolved as agent | 7 |

### Availability Check

Before invoking a plugin command, verify availability:

```python
def check_plugin_availability(plugin_name, command_name):
    """
    Check if a plugin command is available in the current session.
    Fallback gracefully if not available.
    """
    # Attempt invocation; if not available, use fallback
    try:
        invoke(f"/{plugin_name}:{command_name}")
    except PluginNotAvailable:
        log_info(f"Plugin '{plugin_name}' not available. Using fallback.")
        return False
    return True
```

**Graceful Degradation**:

| Missing Plugin | Fallback Behavior |
| --- | --- |
| `superpowers` | Built-in context analysis (5-step process) |
| `code-quality` | Basic `git diff` review, no specialized linting |
| `development` | General implementation without Java agent |
| `education` | Standard Markdown without formatter agent |
| `git-workflow` | Manual `gh` CLI commands |

## Multi-Agent Workflows

For complex tasks that span multiple domains, multiple agents may be resolved:

### Example: Full-Stack Feature

```yaml
Task: "Add user profile page with REST API"

Resolved Agents:
  - java-developer    # Backend API
  - frontend-developer # Frontend UI

Workflow:
  1. java-developer implements REST endpoint
  2. frontend-developer implements UI component
  3. code-reviewer reviews all changes
```

### Example: AI Feature with Backend

```yaml
Task: "Integrate Claude API for content generation"

Resolved Agents:
  - ai-engineer       # LLM integration
  - java-developer    # Service layer

Workflow:
  1. ai-engineer designs prompt templates
  2. java-developer implements service integration
  3. code-reviewer reviews security aspects
```

## Resolution Output

The resolution phase produces a structured plan:

```yaml
resolution_result:
  primary_agent: "java-developer"
  secondary_agents: []
  plugins:
    brainstorm: "superpowers:brainstorm"  # or "built-in"
    implementation: "development:java-developer"
    commits: "git-workflow:commit"
    review: "code-quality:code-reviewer"
    linting: null  # Not Python
    pr: "git-workflow:create-pr"
  flags:
    skip_brainstorm: false
    skip_quality_gate: false
```

This resolution result is used throughout the remaining phases.

## Extending the Routing

### Adding a New Agent

1. Create agent file in the appropriate plugin
2. Add entry to the resolution mapping:

```python
# In technology stack mapping
("NewLanguage", "NewFramework"): "new-agent",

# In label mapping
"new-label": "new-agent",
```

3. Add plugin dependency entry
4. Update this documentation

### Custom Agent Overrides

Users can override agent resolution by specifying in the task file:

```markdown
## Agent Recommendation

**Recommended Agent**: `custom-agent`
**Override**: true

**Rationale**: Custom agent required for project-specific patterns.
```

The `Override: true` flag ensures the explicit recommendation is used even if technology detection suggests a different agent.

## See Also

- [context-analysis.md](./context-analysis.md) - Context analysis that feeds into routing
- [quality-gate.md](./quality-gate.md) - Quality gate using resolved agents
- [workflow.md](./workflow.md) - Complete workflow documentation
- [../../references/create-plan/agent-mapping.md](../create-plan/agent-mapping.md) - Agent mapping from create-plan
