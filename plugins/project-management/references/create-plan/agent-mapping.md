# Agent Mapping Guide

Umfassender Guide zur Zuordnung von Tasks zu KI-Agenten basierend auf Expertise und Task-Typ.

## Übersicht

KI-Agenten haben spezialisierte Fähigkeiten für bestimmte Task-Typen. Dieses Dokument definiert:

- Verfügbare Agenten und ihre Expertise
- Task-Typ → Agent Mapping
- Wann welcher Agent verwendet werden sollte
- Multi-Agent-Workflows

## Verfügbare Agenten

### code-reviewer

**Expertise**:
- Code-Qualitätsprüfung
- Security-Analyse
- Performance-Review
- Best-Practice Validation

**Verwendung**:
```yaml
Task: "Code Review für Dark Mode Feature"
Agent: code-reviewer
Rationale: |
  Proaktive Code-Qualitätsprüfung nach Implementation.
  Prüft auf Security Issues, Performance-Probleme und
  Best-Practice Violations.
```

**Typische Tasks**:
- Pull Request Reviews
- Security Audits
- Code-Qualitäts-Checks
- Refactoring-Validation

**Wann verwenden**:
- ✅ Nach Feature-Implementation
- ✅ Vor Merge in Main Branch
- ✅ Bei Security-kritischen Änderungen
- ✅ Bei Performance-kritischem Code

### java-developer

**Expertise**:
- Java/Spring Boot Development
- Enterprise Java Patterns
- JVM-Optimierung
- Maven/Gradle Build-Management

**Verwendung**:
```yaml
Task: "REST API Endpoint für User-Verwaltung"
Agent: java-developer
Rationale: |
  Spring Boot REST Controller mit DTO-Mapping,
  Service-Layer-Logic und Repository-Integration.
  Expertise in Enterprise Java Patterns erforderlich.
```

**Typische Tasks**:
- REST API Development
- Service-Layer Implementation
- Repository/Database Access
- Spring Boot Configuration
- JPA/Hibernate Entities
- Maven/Gradle Build-Scripts

**Wann verwenden**:
- ✅ Backend-Development in Java
- ✅ Spring Boot Features
- ✅ Database-Integration (JPA)
- ✅ Enterprise Patterns (DI, AOP)

### python-expert

**Expertise**:
- Python Development (Django, FastAPI)
- Data Science Libraries (NumPy, Pandas)
- Async Programming (asyncio)
- Python Best Practices (PEP 8)

**Verwendung**:
```yaml
Task: "FastAPI Endpoint für ML-Model Inference"
Agent: python-expert
Rationale: |
  FastAPI async endpoint mit Pydantic-Validation,
  ML-Model-Integration und Error-Handling.
  Python asyncio expertise erforderlich.
```

**Typische Tasks**:
- Django/FastAPI Development
- Data Processing Scripts
- ML-Pipeline Implementation
- Python-Package Development
- Async/Await Code
- Unit Tests (pytest)

**Wann verwenden**:
- ✅ Backend-Development in Python
- ✅ Data Science/ML Tasks
- ✅ Scripting/Automation
- ✅ API Development (FastAPI/Django)

### ai-engineer

**Expertise**:
- LLM-Integration (OpenAI, Anthropic)
- ML-Pipeline Development
- Vector Databases (Pinecone, Weaviate)
- Prompt Engineering

**Verwendung**:
```yaml
Task: "LLM-gestützte Content-Generierung"
Agent: ai-engineer
Rationale: |
  Integration von Claude API für Content-Generierung
  mit Prompt-Templating, Token-Management und
  Response-Parsing. LLM-Expertise erforderlich.
```

**Typische Tasks**:
- LLM-Integration
- RAG (Retrieval-Augmented Generation)
- Vector Database Setup
- ML-Model Training/Fine-Tuning
- Prompt Engineering
- AI-Feature Development

**Wann verwenden**:
- ✅ LLM-Integration (ChatGPT, Claude, etc.)
- ✅ ML-Feature Development
- ✅ Vector Search/Embeddings
- ✅ AI-Pipeline Implementation

### agent-expert

**Expertise**:
- KI-Agenten-Entwicklung
- Multi-Agent-Systemen
- Agent-Orchestration
- Tool-Integration für Agenten

**Verwendung**:
```yaml
Task: "Multi-Agent Workflow für Code-Review"
Agent: agent-expert
Rationale: |
  Orchestrierung mehrerer Agenten (code-reviewer,
  test-runner, security-scanner) mit Workflow-Logic
  und Result-Aggregation. Agent-Expertise erforderlich.
```

**Typische Tasks**:
- Agent-Development
- Multi-Agent-Workflows
- Agent-Tool-Integration
- Agent-Orchestration
- Custom Agent Creation

**Wann verwenden**:
- ✅ Agent-Development Tasks
- ✅ Multi-Agent-Systeme
- ✅ Agent-Workflow-Orchestration
- ✅ Tool-Integration für Agenten

### markdown-syntax-formatter

**Expertise**:
- Markdown-Formatierung (CommonMark)
- Documentation-Struktur
- Best-Practice Markdown

**Verwendung**:
```yaml
Task: "README.md für Feature X erstellen"
Agent: markdown-syntax-formatter
Rationale: |
  Professionelle Markdown-Dokumentation mit
  CommonMark-Compliance, korrekter Formatierung
  und Best-Practice-Struktur.
```

**Typische Tasks**:
- README.md Creation
- Documentation Formatting
- Markdown-Linting
- CommonMark-Conversion

**Wann verwenden**:
- ✅ Documentation Tasks
- ✅ README Creation
- ✅ Markdown-File Formatting
- ✅ Documentation-Struktur

### Weitere Agenten (erweiterbar)

Die Liste wird laufend erweitert. Neue Agenten werden hinzugefügt, wenn neue Expertise-Bereiche identifiziert werden:

**Potenzielle zukünftige Agenten**:
- `react-developer` - React/TypeScript Frontend
- `devops-engineer` - CI/CD, Infrastructure
- `database-expert` - Database Design, Optimization
- `security-specialist` - Security Audits, Penetration Testing
- `test-automator` - Test-Automation, E2E Tests
- `ui-ux-designer` - UI/UX Design, Accessibility

## Task-Typ → Agent Mapping

### Backend Development

**Java-Backend**:
```yaml
Task-Types:
  - REST API Endpoints
  - Service-Layer Logic
  - Repository/Database Access
  - Spring Boot Configuration

Agent: java-developer
```

**Python-Backend**:
```yaml
Task-Types:
  - Django/FastAPI Endpoints
  - Data Processing
  - Async Handlers
  - Python Scripts

Agent: python-expert
```

### Frontend Development

**React/TypeScript**:
```yaml
Task-Types:
  - React Components
  - State Management (Redux, Context)
  - TypeScript Interfaces
  - Frontend Testing

Agent: react-developer (future)
Fallback: java-developer (TypeScript)
```

### AI/ML Features

**LLM-Integration**:
```yaml
Task-Types:
  - ChatGPT/Claude Integration
  - Prompt Engineering
  - RAG Implementation
  - Vector Database Setup

Agent: ai-engineer
```

**ML-Pipeline**:
```yaml
Task-Types:
  - Model Training
  - Data Preprocessing
  - Feature Engineering
  - Model Deployment

Agent: ai-engineer
```

### DevOps/Infrastructure

**CI/CD**:
```yaml
Task-Types:
  - GitHub Actions Workflows
  - Docker Configuration
  - Kubernetes Manifests
  - Terraform Scripts

Agent: devops-engineer (future)
Fallback: java-developer oder python-expert
```

### Testing

**Unit Tests**:
```yaml
Task-Types:
  - Component Tests
  - Function Tests
  - Mock Setup

Agent: Matching Developer Agent
  - Java: java-developer
  - Python: python-expert
  - React: react-developer
```

**E2E Tests**:
```yaml
Task-Types:
  - Cypress Tests
  - Playwright Tests
  - User-Flow Tests

Agent: test-automator (future)
Fallback: react-developer
```

### Documentation

**Code Documentation**:
```yaml
Task-Types:
  - JavaDoc/JSDoc
  - Code Comments
  - Architecture Docs

Agent: markdown-syntax-formatter
```

**User Documentation**:
```yaml
Task-Types:
  - User Guides
  - Tutorials
  - FAQ

Agent: markdown-syntax-formatter
```

### Security

**Security Audits**:
```yaml
Task-Types:
  - OWASP Top 10 Check
  - Dependency Audit
  - Code Security Review

Agent: security-specialist (future)
Fallback: code-reviewer
```

### Code Review

**Quality Review**:
```yaml
Task-Types:
  - Code-Qualitäts-Check
  - Best-Practice Review
  - Performance-Analyse

Agent: code-reviewer
```

## Multi-Agent-Workflows

Manche Tasks benötigen mehrere Agenten in Sequenz oder parallel.

### Beispiel 1: Feature-Development

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

### Beispiel 2: AI-Feature-Development

**Workflow**:
```yaml
Feature: "AI-gestützte Content-Generierung"

Tasks:
  1. LLM-Integration (Sequential):
     - "Claude API Integration" → ai-engineer
     - "Prompt Templates" → ai-engineer
     - "Response Parsing" → ai-engineer

  2. Backend-Integration (Sequential):
     - "REST Endpoint" → java-developer
     - "Service-Layer" → java-developer
     - "Caching" → java-developer

  3. Testing (Parallel):
     - "Unit Tests" → java-developer
     - "Integration Tests" → ai-engineer
     - "E2E Tests" → test-automator

  4. Review:
     - "Code Review" → code-reviewer
     - "AI-Review" → ai-engineer (Prompt-Qualität)
```

## Agent-Empfehlungs-Algorithmus

```typescript
function recommendAgent(task: Task): Agent {
  // 1. Check Task-Type
  if (task.type === "rest-api" && task.language === "java") {
    return "java-developer"
  }

  if (task.type === "rest-api" && task.language === "python") {
    return "python-expert"
  }

  if (task.type === "llm-integration") {
    return "ai-engineer"
  }

  if (task.type === "agent-development") {
    return "agent-expert"
  }

  if (task.type === "documentation") {
    return "markdown-syntax-formatter"
  }

  if (task.type === "code-review") {
    return "code-reviewer"
  }

  // 2. Check Technology Stack
  if (task.technologies.includes("spring-boot")) {
    return "java-developer"
  }

  if (task.technologies.includes("django") || task.technologies.includes("fastapi")) {
    return "python-expert"
  }

  if (task.technologies.includes("react")) {
    return "react-developer"
  }

  // 3. Check Keywords
  const keywords = task.description.toLowerCase()

  if (keywords.includes("llm") || keywords.includes("openai") || keywords.includes("claude")) {
    return "ai-engineer"
  }

  if (keywords.includes("agent") || keywords.includes("multi-agent")) {
    return "agent-expert"
  }

  // 4. Fallback: No recommendation
  return null
}
```

## In Linear Issue speichern

Agent-Empfehlungen werden in Issue-Description als eigener Abschnitt gespeichert:

```markdown
## Agent Recommendation

**Recommended Agent**: `java-developer`

**Rationale**:
Spring Boot REST Controller mit Service-Layer-Logic.
Expertise in Enterprise Java Patterns erforderlich.

**Alternative Agents**:
- `python-expert` (falls Python-Rewrite gewünscht)

**Multi-Agent Workflow**:
1. `java-developer` - Implementation
2. `code-reviewer` - Quality Review
```

## Custom Agent Integration

Falls neue Agenten hinzugefügt werden, muss die Mapping-Logik aktualisiert werden:

### 1. Agent definieren

```yaml
# .claude/agents/new-agent.md
---
name: new-agent
description: Beschreibung des Agenten
color: blue
category: development
model: sonnet
---

# New Agent

...
```

### 2. Mapping aktualisieren

```typescript
// In create-plan Command
const agentMapping = {
  ...existingMappings,

  "new-task-type": {
    agent: "new-agent",
    rationale: "Expertise in X erforderlich"
  }
}
```

### 3. Dokumentation aktualisieren

- `agent-mapping.md` erweitern
- Neue Task-Typen dokumentieren
- Verwendungs-Beispiele hinzufügen

## Best Practices

### DO ✅

**Passenden Agent wählen**:
- Agent-Expertise matched Task-Requirements
- Rationale dokumentieren
- Alternative Agenten erwähnen

**Multi-Agent bei Komplexität**:
- Große Tasks → Mehrere Agenten
- Sequentielle vs. parallele Workflows
- Koordination dokumentieren

**Agent-Empfehlung in Issues**:
- Immer in Issue-Description
- Klar formatiert
- Rationale angeben

### DON'T ❌

**Falschen Agent zuweisen**:
- Java-Task → python-expert ❌
- LLM-Integration → java-developer ❌

**Agent-Empfehlung auslassen**:
- Jeder Task sollte Empfehlung haben
- Auch wenn "offensichtlich"

**Zu viele Agenten**:
- Keep it simple
- Nur wenn wirklich nötig

## Häufige Fehler

### ❌ Agent-Mismatch

**Problem**: Task und Agent passen nicht zusammen

**Beispiel**:
```yaml
Task: "FastAPI REST Endpoint implementieren"
Agent: java-developer ❌
```

**Lösung**:
```yaml
Task: "FastAPI REST Endpoint implementieren"
Agent: python-expert ✅
```

### ❌ Keine Multi-Agent-Planung

**Problem**: Großer Task ohne Multi-Agent-Workflow

**Beispiel**:
```yaml
Task: "Complete E-Commerce Feature (21 SP)"
Agent: java-developer ❌
```

**Lösung**: Task aufteilen und Multi-Agent-Workflow:
```yaml
Tasks:
  - "Backend API" (5 SP) → java-developer
  - "Frontend UI" (5 SP) → react-developer
  - "Payment Integration" (8 SP) → java-developer
  - "Testing" (3 SP) → test-automator
  - "Code Review" (2 SP) → code-reviewer
```

### ❌ Agent-Rationale fehlt

**Problem**: Keine Begründung für Agent-Wahl

**Schlecht**:
```markdown
## Agent Recommendation
**Agent**: java-developer
```

**Gut**:
```markdown
## Agent Recommendation
**Agent**: `java-developer`

**Rationale**:
Spring Boot REST API mit JPA-Repositories.
Enterprise Java Patterns erforderlich.
```

## Checkliste: Agent-Empfehlung

Vor dem Erstellen eines Tasks:

- [ ] **Agent identifiziert**: Passender Agent für Task-Typ?
- [ ] **Rationale dokumentiert**: Warum dieser Agent?
- [ ] **Alternative geprüft**: Gibt es andere passende Agenten?
- [ ] **Multi-Agent erwägt**: Ist Multi-Agent-Workflow nötig?
- [ ] **In Issue dokumentiert**: Agent-Empfehlung in Description?

---

**Siehe auch**:
- [task-breakdown.md](task-breakdown.md) - Task-Breakdown Strategien
- [linear-integration.md](linear-integration.md) - Linear-Integration Details
- [best-practices.md](best-practices.md) - Allgemeine Best Practices
