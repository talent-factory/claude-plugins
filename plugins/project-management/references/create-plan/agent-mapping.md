# Agent Mapping Guide

Comprehensive guide to assigning tasks to AI agents based on expertise and task type.

## Overview

AI agents possess specialized capabilities for specific task types. This document defines:

- Available agents and their areas of expertise
- Task type to agent mapping
- When to utilize each agent
- Multi-agent workflows

## Available Agents

### code-reviewer

**Expertise**:

- Code quality assessment
- Security analysis
- Performance review
- Best practice validation

**Usage**:

```yaml
Task: "Code Review for Dark Mode Feature"
Agent: code-reviewer
Rationale: |
  Proactive code quality assessment following implementation.
  Examines security issues, performance problems, and
  best practice violations.
```

**Typical Tasks**:

- Pull request reviews
- Security audits
- Code quality checks
- Refactoring validation

**When to Use**:

- After feature implementation
- Before merge to main branch
- For security-critical changes
- For performance-critical code

### java-developer

**Expertise**:

- Java/Spring Boot development
- Enterprise Java patterns
- JVM optimization
- Maven/Gradle build management

**Usage**:

```yaml
Task: "REST API Endpoint for User Management"
Agent: java-developer
Rationale: |
  Spring Boot REST controller with DTO mapping,
  service layer logic, and repository integration.
  Enterprise Java pattern expertise required.
```

**Typical Tasks**:

- REST API development
- Service layer implementation
- Repository/database access
- Spring Boot configuration
- JPA/Hibernate entities
- Maven/Gradle build scripts

**When to Use**:

- Backend development in Java
- Spring Boot features
- Database integration (JPA)
- Enterprise patterns (DI, AOP)

### python-expert

**Expertise**:

- Python development (Django, FastAPI)
- Data science libraries (NumPy, Pandas)
- Async programming (asyncio)
- Python best practices (PEP 8)

**Usage**:

```yaml
Task: "FastAPI Endpoint for ML Model Inference"
Agent: python-expert
Rationale: |
  FastAPI async endpoint with Pydantic validation,
  ML model integration, and error handling.
  Python asyncio expertise required.
```

**Typical Tasks**:

- Django/FastAPI development
- Data processing scripts
- ML pipeline implementation
- Python package development
- Async/await code
- Unit tests (pytest)

**When to Use**:

- Backend development in Python
- Data science/ML tasks
- Scripting/automation
- API development (FastAPI/Django)

### ai-engineer

**Expertise**:

- LLM integration (OpenAI, Anthropic)
- ML pipeline development
- Vector databases (Pinecone, Weaviate)
- Prompt engineering

**Usage**:

```yaml
Task: "LLM-Powered Content Generation"
Agent: ai-engineer
Rationale: |
  Integration of Claude API for content generation
  with prompt templating, token management, and
  response parsing. LLM expertise required.
```

**Typical Tasks**:

- LLM integration
- RAG (Retrieval-Augmented Generation)
- Vector database setup
- ML model training/fine-tuning
- Prompt engineering
- AI feature development

**When to Use**:

- LLM integration (ChatGPT, Claude, etc.)
- ML feature development
- Vector search/embeddings
- AI pipeline implementation

### agent-expert

**Expertise**:

- AI agent development
- Multi-agent systems
- Agent orchestration
- Tool integration for agents

**Usage**:

```yaml
Task: "Multi-Agent Workflow for Code Review"
Agent: agent-expert
Rationale: |
  Orchestration of multiple agents (code-reviewer,
  test-runner, security-scanner) with workflow logic
  and result aggregation. Agent expertise required.
```

**Typical Tasks**:

- Agent development
- Multi-agent workflows
- Agent tool integration
- Agent orchestration
- Custom agent creation

**When to Use**:

- Agent development tasks
- Multi-agent systems
- Agent workflow orchestration
- Tool integration for agents

### markdown-syntax-formatter

**Expertise**:

- Markdown formatting (CommonMark)
- Documentation structure
- Best practice Markdown

**Usage**:

```yaml
Task: "Create README.md for Feature X"
Agent: markdown-syntax-formatter
Rationale: |
  Professional Markdown documentation with
  CommonMark compliance, correct formatting,
  and best practice structure.
```

**Typical Tasks**:

- README.md creation
- Documentation formatting
- Markdown linting
- CommonMark conversion

**When to Use**:

- Documentation tasks
- README creation
- Markdown file formatting
- Documentation structure

### Additional Agents (Extensible)

The list is continuously expanded. New agents are added when new areas of expertise are identified:

**Potential Future Agents**:

- `react-developer` - React/TypeScript frontend
- `devops-engineer` - CI/CD, infrastructure
- `database-expert` - Database design, optimization
- `security-specialist` - Security audits, penetration testing
- `test-automator` - Test automation, E2E tests
- `ui-ux-designer` - UI/UX design, accessibility

## Task Type to Agent Mapping

### Backend Development

**Java Backend**:

```yaml
Task-Types:
  - REST API endpoints
  - Service layer logic
  - Repository/database access
  - Spring Boot configuration

Agent: java-developer
```

**Python Backend**:

```yaml
Task-Types:
  - Django/FastAPI endpoints
  - Data processing
  - Async handlers
  - Python scripts

Agent: python-expert
```

### Frontend Development

**React/TypeScript**:

```yaml
Task-Types:
  - React components
  - State management (Redux, Context)
  - TypeScript interfaces
  - Frontend testing

Agent: react-developer (future)
Fallback: java-developer (TypeScript)
```

### AI/ML Features

**LLM Integration**:

```yaml
Task-Types:
  - ChatGPT/Claude integration
  - Prompt engineering
  - RAG implementation
  - Vector database setup

Agent: ai-engineer
```

**ML Pipeline**:

```yaml
Task-Types:
  - Model training
  - Data preprocessing
  - Feature engineering
  - Model deployment

Agent: ai-engineer
```

### DevOps/Infrastructure

**CI/CD**:

```yaml
Task-Types:
  - GitHub Actions workflows
  - Docker configuration
  - Kubernetes manifests
  - Terraform scripts

Agent: devops-engineer (future)
Fallback: java-developer or python-expert
```

### Testing

**Unit Tests**:

```yaml
Task-Types:
  - Component tests
  - Function tests
  - Mock setup

Agent: Matching developer agent
  - Java: java-developer
  - Python: python-expert
  - React: react-developer
```

**E2E Tests**:

```yaml
Task-Types:
  - Cypress tests
  - Playwright tests
  - User flow tests

Agent: test-automator (future)
Fallback: react-developer
```

### Documentation

**Code Documentation**:

```yaml
Task-Types:
  - JavaDoc/JSDoc
  - Code comments
  - Architecture docs

Agent: markdown-syntax-formatter
```

**User Documentation**:

```yaml
Task-Types:
  - User guides
  - Tutorials
  - FAQ

Agent: markdown-syntax-formatter
```

### Security

**Security Audits**:

```yaml
Task-Types:
  - OWASP Top 10 check
  - Dependency audit
  - Code security review

Agent: security-specialist (future)
Fallback: code-reviewer
```

### Code Review

**Quality Review**:

```yaml
Task-Types:
  - Code quality check
  - Best practice review
  - Performance analysis

Agent: code-reviewer
```

## Multi-Agent Workflows

Certain tasks require multiple agents in sequence or in parallel.

### Example 1: Feature Development

**Workflow**:

```yaml
Feature: "User Authentication"

Tasks:
  1. Implementation (Sequential):
     - "Backend API" → java-developer
     - "Frontend Components" → react-developer
     - "Integration" → java-developer + react-developer

  2. Testing (Parallel):
     - "Backend Unit Tests" → java-developer
     - "Frontend Unit Tests" → react-developer
     - "E2E Tests" → test-automator

  3. Documentation (Sequential):
     - "API Docs" → markdown-syntax-formatter
     - "User Guide" → markdown-syntax-formatter

  4. Review (Final):
     - "Code Review" → code-reviewer
```

### Example 2: AI Feature Development

**Workflow**:

```yaml
Feature: "AI-Powered Content Generation"

Tasks:
  1. LLM Integration (Sequential):
     - "Claude API Integration" → ai-engineer
     - "Prompt Templates" → ai-engineer
     - "Response Parsing" → ai-engineer

  2. Backend Integration (Sequential):
     - "REST Endpoint" → java-developer
     - "Service Layer" → java-developer
     - "Caching" → java-developer

  3. Testing (Parallel):
     - "Unit Tests" → java-developer
     - "Integration Tests" → ai-engineer
     - "E2E Tests" → test-automator

  4. Review:
     - "Code Review" → code-reviewer
     - "AI Review" → ai-engineer (prompt quality)
```

## Agent Recommendation Algorithm

```typescript
function recommendAgent(task: Task): Agent {
  // 1. Check Task-Type
  if (task.type === "rest-api" && task.language === "java") {
    return "java-developer";
  }

  if (task.type === "rest-api" && task.language === "python") {
    return "python-expert";
  }

  if (task.type === "llm-integration") {
    return "ai-engineer";
  }

  if (task.type === "agent-development") {
    return "agent-expert";
  }

  if (task.type === "documentation") {
    return "markdown-syntax-formatter";
  }

  if (task.type === "code-review") {
    return "code-reviewer";
  }

  // 2. Check Technology Stack
  if (task.technologies.includes("spring-boot")) {
    return "java-developer";
  }

  if (
    task.technologies.includes("django") ||
    task.technologies.includes("fastapi")
  ) {
    return "python-expert";
  }

  if (task.technologies.includes("react")) {
    return "react-developer";
  }

  // 3. Check Keywords
  const keywords = task.description.toLowerCase();

  if (
    keywords.includes("llm") ||
    keywords.includes("openai") ||
    keywords.includes("claude")
  ) {
    return "ai-engineer";
  }

  if (keywords.includes("agent") || keywords.includes("multi-agent")) {
    return "agent-expert";
  }

  // 4. Fallback: No recommendation
  return null;
}
```

## Storing in Linear Issue

Agent recommendations are stored in the issue description as a dedicated section:

```markdown
## Agent Recommendation

**Recommended Agent**: `java-developer`

**Rationale**:
Spring Boot REST controller with service layer logic.
Enterprise Java pattern expertise required.

**Alternative Agents**:

- `python-expert` (if Python rewrite is desired)

**Multi-Agent Workflow**:

1. `java-developer` - Implementation
2. `code-reviewer` - Quality review
```

## Custom Agent Integration

When adding new agents, the mapping logic must be updated:

### 1. Define Agent

```yaml
# .claude/agents/new-agent.md
---
name: new-agent
description: Description of the agent
color: blue
category: development
model: sonnet
---
# New Agent
...
```

### 2. Update Mapping

```typescript
// In create-plan command
const agentMapping = {
  ...existingMappings,

  "new-task-type": {
    agent: "new-agent",
    rationale: "Expertise in X required",
  },
};
```

### 3. Update Documentation

- Extend `agent-mapping.md`
- Document new task types
- Add usage examples

## Best Practices

### DO

**Select Appropriate Agent**:

- Agent expertise matches task requirements
- Document rationale
- Mention alternative agents

**Use Multi-Agent for Complex Tasks**:

- Large tasks require multiple agents
- Sequential vs. parallel workflows
- Document coordination

**Include Agent Recommendation in Issues**:

- Always in issue description
- Clearly formatted
- Provide rationale

### DON'T

**Assign Wrong Agent**:

- Java task to python-expert
- LLM integration to java-developer

**Omit Agent Recommendation**:

- Every task should have a recommendation
- Even when "obvious"

**Use Too Many Agents**:

- Keep it simple
- Only when truly necessary

## Common Errors

### Agent Mismatch

**Problem**: Task and agent do not align

**Example**:

```yaml
Task: "Implement FastAPI REST Endpoint"
Agent: java-developer # Incorrect
```

**Solution**:

```yaml
Task: "Implement FastAPI REST Endpoint"
Agent: python-expert # Correct
```

### Missing Multi-Agent Planning

**Problem**: Large task without multi-agent workflow

**Example**:

```yaml
Task: "Complete E-Commerce Feature (21 SP)"
Agent: java-developer # Incorrect
```

**Solution**: Decompose task and use multi-agent workflow:

```yaml
Tasks:
  - "Backend API" (5 SP) → java-developer
  - "Frontend UI" (5 SP) → react-developer
  - "Payment Integration" (8 SP) → java-developer
  - "Testing" (3 SP) → test-automator
  - "Code Review" (2 SP) → code-reviewer
```

### Missing Agent Rationale

**Problem**: No justification for agent selection

**Incorrect**:

```markdown
## Agent Recommendation

**Agent**: java-developer
```

**Correct**:

```markdown
## Agent Recommendation

**Agent**: `java-developer`

**Rationale**:
Spring Boot REST API with JPA repositories.
Enterprise Java pattern expertise required.
```

## Checklist: Agent Recommendation

Before creating a task:

- [ ] **Agent identified**: Appropriate agent for task type?
- [ ] **Rationale documented**: Why this agent?
- [ ] **Alternative considered**: Are there other suitable agents?
- [ ] **Multi-agent evaluated**: Is multi-agent workflow necessary?
- [ ] **Documented in issue**: Agent recommendation in description?

---

**See also**:

- [task-breakdown.md](task-breakdown.md) - Task breakdown strategies
- [linear-integration.md](linear-integration.md) - Linear integration details
- [best-practices.md](best-practices.md) - General best practices
