# Linear Integration Guide

Umfassende Dokumentation zur Integration mit Linear für EPIC- und Issue-Management.

## Übersicht

Linear wird als zentrale Projekt-Management-Plattform verwendet:

- **EPICs**: Repräsentieren PRD-basierte Features/Initiativen
- **Issues**: Individuelle, atomare Tasks
- **Labels**: Kategorisierung und Filterung
- **Estimates**: Story Point Schätzungen
- **Dependencies**: Task-Verknüpfungen
- **Custom Fields**: Erweiterte Metadaten (z.B. Agent-Empfehlungen)

## Linear-Hierarchie

```
Workspace (Organization)
└── Team
    └── Project (EPIC)
        ├── Issue 1
        ├── Issue 2
        └── Issue N
```

### EPIC-Struktur

**EPIC = PRD-Feature**:

```yaml
Title: "[Feature-Name]"
Description: |
  ## Executive Summary
  [Aus PRD übernommen]

  ## Business Value
  [Warum wird das gebaut?]

  ## Success Metrics
  [Messbare Ziele]

  ## Timeline
  [Grobe Meilensteine]

  ## Full PRD
  Link: [PRD-Pfad oder URL]
Status: planned | in_progress | completed | canceled
Priority: urgent | high | medium | low | no_priority
Estimate: [Summe aller Issue-Estimates]
Labels: [epic, feature, ...]
```

### Issue-Struktur

**Issue = Atomic Task**:

```yaml
Title: "[Prägnante Task-Beschreibung]"
Description: |
  ## Task Details
  [Vollständige Beschreibung]

  ## Acceptance Criteria
  - [ ] Kriterium 1
  - [ ] Kriterium 2

  ## Technical Notes
  [Implementierungs-Hinweise]

  ## Agent Recommendation
  - Empfohlener Agent: [agent-name]
  - Rationale: [Warum dieser Agent?]

  ## Dependencies
  - Depends on: LIN-XXX
  - Blocks: LIN-YYY

Parent: [EPIC-ID]
Status: backlog | todo | in_progress | done | canceled
Priority: urgent | high | medium | low | no_priority
Estimate: [1, 2, 3, 5, 8, 13, 21]
Labels: [feature, bug, documentation, ...]
Assignee: [Optional]
```

## Linear MCP Tools

### Verfügbare Tools

Der Linear-MCP-Server bietet folgende Tools:

#### Project/EPIC Management

```typescript
// EPIC erstellen
mcp__linear__create_project({
  name: "Dark Mode Toggle",
  description: "Executive Summary + Full Description",
  state: "planned",
  priority: "high",
  teamId: "TEAM_ID"
})

// EPIC auflisten
mcp__linear__list_projects({
  teamId: "TEAM_ID",
  status: "planned" // planned, in_progress, completed
})

// EPIC Details abrufen
mcp__linear__get_project({
  projectId: "PROJECT_ID"
})

// EPIC aktualisieren
mcp__linear__update_project({
  projectId: "PROJECT_ID",
  name: "Updated Name",
  description: "Updated Description",
  state: "in_progress"
})
```

#### Issue Management

```typescript
// Issue erstellen
mcp__linear__create_issue({
  title: "Implement UI Toggle Component",
  description: "Detailed description with acceptance criteria",
  projectId: "PROJECT_ID", // Verknüpfung mit EPIC
  priority: "high",
  estimate: 3, // Story Points
  labelIds: ["LABEL_ID_1", "LABEL_ID_2"],
  teamId: "TEAM_ID"
})

// Issues auflisten
mcp__linear__list_issues({
  projectId: "PROJECT_ID",
  status: "backlog", // backlog, todo, in_progress, done
  teamId: "TEAM_ID"
})

// Issue Details abrufen
mcp__linear__get_issue({
  issueId: "ISSUE_ID"
})

// Issue aktualisieren
mcp__linear__update_issue({
  issueId: "ISSUE_ID",
  title: "Updated Title",
  description: "Updated Description",
  status: "in_progress",
  estimate: 5
})

// Issue löschen (bei Duplikaten)
mcp__linear__delete_issue({
  issueId: "ISSUE_ID"
})
```

#### Label Management

```typescript
// Labels auflisten
mcp__linear__list_labels({
  teamId: "TEAM_ID"
})

// Label erstellen
mcp__linear__create_label({
  name: "feature",
  color: "#4CAF50",
  teamId: "TEAM_ID"
})

// Issue Labels zuweisen
mcp__linear__add_label_to_issue({
  issueId: "ISSUE_ID",
  labelId: "LABEL_ID"
})
```

#### Dependencies

```typescript
// Dependency erstellen
mcp__linear__create_issue_relation({
  issueId: "ISSUE_ID",
  relatedIssueId: "RELATED_ISSUE_ID",
  type: "blocks" // blocks, blocked_by, related_to
})

// Dependencies auflisten
mcp__linear__list_issue_relations({
  issueId: "ISSUE_ID"
})
```

## Workflow-Implementation

### 1. PRD einlesen

```typescript
// PRD-Datei einlesen
const prdContent = await read_file({ file_path: prdPath })

// PRD-Struktur validieren
const prdData = parsePRD(prdContent)
validatePRDStructure(prdData)
```

### 2. Duplikat-Check

```typescript
// Existierende EPICs prüfen
const existingProjects = await mcp__linear__list_projects({
  teamId: TEAM_ID,
  status: "planned,in_progress"
})

// Nach ähnlichen Namen suchen
const duplicates = existingProjects.filter(p =>
  similarity(p.name, prdData.title) > 0.8
)

if (duplicates.length > 0) {
  // Interaktive Bestätigung
  const userChoice = await askUserQuestion({
    question: "Ähnliches EPIC gefunden. Was möchten Sie tun?",
    options: [
      "Neues EPIC erstellen",
      "Existierendes EPIC erweitern",
      "Abbrechen"
    ]
  })
}
```

### 3. EPIC erstellen

```typescript
// EPIC aus PRD erstellen
const epic = await mcp__linear__create_project({
  name: prdData.title,
  description: formatEpicDescription(prdData),
  state: "planned",
  priority: mapPRDPriority(prdData.priority),
  teamId: TEAM_ID
})

console.log(`✅ EPIC erstellt: ${epic.name} (${epic.identifier})`)
```

### 4. Task-Breakdown

```typescript
// Tasks aus PRD ableiten
const tasks = breakdownPRDToTasks(prdData)

// Tasks kategorisieren
const categorizedTasks = {
  mustHave: tasks.filter(t => t.priority === "must"),
  shouldHave: tasks.filter(t => t.priority === "should"),
  couldHave: tasks.filter(t => t.priority === "could")
}
```

### 5. Issues erstellen

```typescript
// Für jeden Task ein Issue erstellen
for (const task of categorizedTasks.mustHave) {
  // Duplikat-Check
  const existingIssue = await checkForDuplicateIssue(task, epic.id)
  if (existingIssue) {
    console.log(`⚠️  Duplikat gefunden: ${existingIssue.identifier}`)
    continue
  }

  // Labels vorbereiten
  const labels = await getOrCreateLabels(task.labels, TEAM_ID)

  // Issue erstellen
  const issue = await mcp__linear__create_issue({
    title: task.title,
    description: formatIssueDescription(task),
    projectId: epic.id,
    priority: mapPriority(task.priority),
    estimate: task.estimate,
    labelIds: labels.map(l => l.id),
    teamId: TEAM_ID
  })

  console.log(`✅ Issue erstellt: ${issue.identifier} - ${issue.title}`)
}
```

### 6. Dependencies verknüpfen

```typescript
// Dependencies zwischen Issues erstellen
for (const task of tasks) {
  if (task.dependencies && task.dependencies.length > 0) {
    for (const depIdentifier of task.dependencies) {
      await mcp__linear__create_issue_relation({
        issueId: task.issueId,
        relatedIssueId: depIdentifier,
        type: "blocked_by"
      })
    }
  }
}
```

## Label-Strategie

### Standard-Labels

**Technology Stack**:
- `java` - Java/Spring Boot Tasks
- `python` - Python/Django/FastAPI Tasks
- `javascript` - JavaScript/TypeScript Tasks
- `react` - React Frontend
- `database` - Database-related Tasks

**Task Type**:
- `feature` - Neue Funktionalität
- `bug` - Fehlerbehebung
- `documentation` - Dokumentation
- `testing` - Test-Tasks
- `refactor` - Code-Refactoring
- `security` - Security-Tasks
- `performance` - Performance-Optimierung

**Priority** (redundant zu Issue-Priority, aber nützlich für Filtering):
- `must-have` - Must-Have Features
- `should-have` - Should-Have Features
- `could-have` - Could-Have Features

**Agent Tags**:
- `agent:code-reviewer` - Für Code-Review Tasks
- `agent:java-developer` - Für Java Tasks
- `agent:python-expert` - Für Python Tasks
- `agent:ai-engineer` - Für AI/ML Tasks

### Label-Erstellung

```typescript
const standardLabels = [
  { name: "java", color: "#E76F00" },
  { name: "python", color: "#3776AB" },
  { name: "javascript", color: "#F7DF1E" },
  { name: "react", color: "#61DAFB" },
  { name: "feature", color: "#4CAF50" },
  { name: "bug", color: "#F44336" },
  { name: "documentation", color: "#FFC107" },
  { name: "testing", color: "#9C27B0" },
  { name: "must-have", color: "#D32F2F" },
  { name: "should-have", color: "#FF9800" },
  { name: "could-have", color: "#8BC34A" }
]

// Labels erstellen (falls nicht vorhanden)
for (const labelDef of standardLabels) {
  const existingLabel = existingLabels.find(l => l.name === labelDef.name)
  if (!existingLabel) {
    await mcp__linear__create_label({
      name: labelDef.name,
      color: labelDef.color,
      teamId: TEAM_ID
    })
  }
}
```

## Story Point Estimation

**Story Points** basieren auf Komplexität, nicht Zeit:

| Story Points | Komplexität | Beispiel |
|--------------|-------------|----------|
| **1** | Trivial | Konfigurationsänderung |
| **2** | Einfach | Einfache CRUD-Operation |
| **3** | Mittel | Feature mit wenigen Edge Cases |
| **5** | Komplex | Feature mit mehreren Edge Cases |
| **8** | Sehr Komplex | Feature mit vielen Dependencies |
| **13** | Extrem Komplex | Große Refactoring/Migration |
| **21** | Episch | Zu groß, aufteilen! |

**Faustregel**: Tasks > 8 SP sollten in kleinere Tasks aufgeteilt werden.

## Custom Fields

Linear erlaubt Custom Fields für erweiterte Metadaten:

```typescript
// Custom Field für Agent-Empfehlungen
await mcp__linear__create_custom_field({
  teamId: TEAM_ID,
  name: "Recommended Agent",
  type: "text",
  description: "KI-Agent der für diesen Task empfohlen wird"
})

// Custom Field setzen
await mcp__linear__set_issue_custom_field({
  issueId: issue.id,
  customFieldId: CUSTOM_FIELD_ID,
  value: "java-developer"
})
```

## Error Handling

### Duplikat-Erkennung

```typescript
function checkForDuplicateIssue(task, epicId) {
  const existingIssues = await mcp__linear__list_issues({
    projectId: epicId
  })

  return existingIssues.find(issue => {
    // Exakte Titel-Übereinstimmung
    if (issue.title === task.title) return true

    // Ähnlichkeit > 90%
    if (similarity(issue.title, task.title) > 0.9) return true

    return false
  })
}
```

### Rate Limiting

Linear-API hat Rate Limits:

```typescript
// Throttle API-Calls
async function createIssuesWithThrottle(tasks, epicId) {
  for (const task of tasks) {
    await createIssue(task, epicId)
    await sleep(100) // 100ms Pause zwischen Calls
  }
}
```

### Fehlerbehandlung

```typescript
try {
  const issue = await mcp__linear__create_issue({...})
} catch (error) {
  if (error.code === "DUPLICATE") {
    console.log(`⚠️  Issue bereits vorhanden: ${task.title}`)
  } else if (error.code === "RATE_LIMIT") {
    console.log("⏳ Rate Limit erreicht, warte 60s...")
    await sleep(60000)
    // Retry
  } else {
    console.error(`❌ Fehler beim Erstellen: ${error.message}`)
    throw error
  }
}
```

## Best Practices

### EPIC-Erstellung

**DO ✅**:
- Executive Summary in EPIC-Description
- Link zum vollständigen PRD
- Realistische Timeline setzen
- Business Value klar kommunizieren

**DON'T ❌**:
- Technische Implementierung in EPIC
- Zu viele Details (gehören in Issues)
- EPICs ohne klare Success Metrics

### Issue-Erstellung

**DO ✅**:
- Klare, prägnante Titel
- Ausführliche Acceptance Criteria
- Dependencies dokumentieren
- Realistische Estimates
- Agent-Empfehlungen hinzufügen

**DON'T ❌**:
- Vage Beschreibungen
- Zu große Tasks (> 8 SP)
- Issues ohne Akzeptanzkriterien
- Dependencies ignorieren

### Label-Verwendung

**DO ✅**:
- Konsistente Label-Strategie
- Technology + Type Labels kombinieren
- Agent-Tags für Empfehlungen

**DON'T ❌**:
- Zu viele Labels pro Issue (max 5-7)
- Label-Namen inkonsistent
- Labels ohne klare Bedeutung

## Troubleshooting

### "EPIC nicht gefunden"

**Problem**: Issue kann nicht mit EPIC verknüpft werden

**Lösung**:
```typescript
// EPIC-ID verifizieren
const epic = await mcp__linear__get_project({ projectId: EPIC_ID })
if (!epic) {
  console.error("EPIC existiert nicht!")
}
```

### "Label nicht gefunden"

**Problem**: Label-ID ist ungültig

**Lösung**:
```typescript
// Labels neu abrufen
const labels = await mcp__linear__list_labels({ teamId: TEAM_ID })
const labelMap = Object.fromEntries(
  labels.map(l => [l.name, l.id])
)
```

### "Rate Limit exceeded"

**Problem**: Zu viele API-Calls

**Lösung**:
- Throttling implementieren (100-200ms zwischen Calls)
- Batch-Operations verwenden wo möglich
- Bei 429-Fehler: 60s warten

---

**Siehe auch**:
- [task-breakdown.md](task-breakdown.md) - Task-Breakdown Strategien
- [agent-mapping.md](agent-mapping.md) - Agent-Empfehlungen
- [best-practices.md](best-practices.md) - Allgemeine Best Practices
