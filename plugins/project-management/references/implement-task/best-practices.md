# Best Practices: Task Implementation

Best Practices für die Implementierung von Tasks (Filesystem oder Linear).

## Branch-Naming

### Einheitliches Format

**Alle Provider nutzen dasselbe Format**:

```
feature/<ISSUE-ID>-<description>
```

| Provider | Beispiel |
|----------|----------|
| Filesystem | `feature/task-001-ui-toggle-component` |
| Linear | `feature/proj-123-oauth2-auth` |

### Regeln

1. **Prefix `feature/`**: Für alle Feature-Branches
2. **Lowercase**: Immer kleingeschrieben
3. **Kebab-case**: Wörter mit Bindestrichen trennen
4. **Issue-ID nach Prefix**: `feature/<ID>-...`
5. **Kurze Beschreibung**: Max. 3-4 Wörter nach ID
6. **Keine Emojis**: Nur ASCII-Zeichen

### Beispiele

```bash
# Gut ✅
feature/task-001-ui-toggle-component
feature/proj-123-user-authentication

# Schlecht ❌
task-001-ui-toggle          # Fehlt feature/ prefix
feature/oauth               # Fehlt Issue-ID
Feature/PROJ-123            # Nicht lowercase
daniels-branch              # Kein Standard-Format
```

### Alternative Prefixes

Für andere Branch-Typen:

| Typ | Format | Beispiel |
|-----|--------|----------|
| Feature | `feature/<ID>-desc` | `feature/task-001-toggle` |
| Bugfix | `fix/<ID>-desc` | `fix/task-002-button-crash` |
| Hotfix | `hotfix/<ID>-desc` | `hotfix/proj-999-security` |

## Commit-Messages

### Format

```
<emoji> <type>: <description>

[optional body]
```

### Commit-Typen aus Task-Labels

| Task-Label | Commit-Typ | Emoji |
|------------|------------|-------|
| `bug`, `fix` | fix | 🐛 |
| `feature`, `enhancement` | feat | ✨ |
| `docs`, `documentation` | docs | 📚 |
| `refactor` | refactor | ♻️ |
| `performance` | perf | ⚡ |
| `test` | test | 🧪 |
| `style` | style | 💎 |
| `chore` | chore | 🔧 |

### Beispiele

```bash
# Feature
git commit -m "✨ feat: Add ThemeToggle component"

# Bug-Fix
git commit -m "🐛 fix: Correct theme persistence bug"

# Tests
git commit -m "🧪 test: Add ThemeToggle unit tests"

# Status-Updates
git commit -m "🔄 chore: Start task-001 implementation"
git commit -m "✅ chore: Mark task-001 as completed"
```

### Atomic Commits

**Best Practice**: Ein Commit pro logischer Änderung

```bash
# Gut ✅
git commit -m "✨ feat: Add ThemeToggle component"
git commit -m "🧪 test: Add ThemeToggle tests"
git commit -m "📚 docs: Document ThemeToggle usage"

# Schlecht ❌
git commit -m "Implement everything"
```

## PR-Gestaltung

### PR-Titel

```bash
# Einheitliches Format
feat(task-001): UI Toggle Component
feat(proj-123): User Authentication via OAuth2
```

### PR-Body-Template

```markdown
## Task: [ID] - [Titel]

**Beschreibung**:
<Task-Beschreibung>

**Änderungen**:
- <Änderung 1>
- <Änderung 2>

**Test-Plan**:
- [x] Akzeptanzkriterium 1
- [x] Akzeptanzkriterium 2

**Status**: In Progress → Completed
```

### PR-Größe

| LOC | Bewertung |
|-----|-----------|
| < 150 | ✅ Sehr gut, schnelles Review |
| 150-400 | ✅ Gut, normales Review |
| 400-800 | ⚠️ OK, langsames Review |
| > 800 | ❌ Zu groß, aufteilen! |

## Testing

### Mindest-Coverage

- **Neue Features**: 80%+
- **Bug-Fixes**: 100% (Bug + Fix covered)
- **Refactoring**: Keine Reduktion
- **Critical Paths**: 100%

### Akzeptanzkriterien als Tests

```javascript
// Issue-AC: "User can log in with Google"
// → Test:
it('should allow user to log in with Google', async () => {
  // Test implementation
})
```

### Test-Pyramide

```
       / E2E \        ← 10% Wenige, wichtigste Flows
     /Integration\   ← 20% Mittelviel, API-Tests
   /  Unit Tests   \ ← 70% Viele, alle Funktionen
```

## Code-Qualität

### Vor PR-Erstellung

- [ ] Alle Akzeptanzkriterien erfüllt?
- [ ] Tests geschrieben und grün?
- [ ] Linting erfolgreich?
- [ ] Build erfolgreich?
- [ ] Keine Debug-Code?
- [ ] Dokumentation aktualisiert?

### Self-Review

```bash
# Diff anschauen
git diff main...HEAD

# Fragen:
# - Würde ich diesen Code mergen?
# - Ist der Code verständlich ohne Kontext?
# - Fehlen Tests für Edge Cases?
```

## Task-Organisation

### Status-Workflow

**Best Practice**: Max. 1-2 Tasks gleichzeitig in Bearbeitung

```
1. Task auswählen (pending/Backlog)
2. Status → in_progress/In Progress
3. Implementieren
4. PR erstellen
5. Status → completed/Done
6. Nächsten Task auswählen
```

### Dependency-Awareness (Filesystem)

**Vor Task-Start**: Dependencies prüfen!

```markdown
## Dependencies
- **Requires**: task-001, task-003  ← Müssen completed sein!
- **Blocks**: task-005
```

## Summary: Do's & Don'ts

### DO ✅

1. **Aussagekräftige Branch-Names**
2. **Atomic Commits** mit Emoji Conventional Format
3. **Kleine PRs** (< 400 LOC)
4. **Tests schreiben** (80%+ Coverage)
5. **Dependencies prüfen** vor Task-Start
6. **Status aktuell halten**
7. **Self-Review** vor PR

### DON'T ❌

1. **Vage Branch-Namen** (`fix-stuff`)
2. **Riesige Commits** (`Implement everything`)
3. **Große PRs** (> 800 LOC)
4. **Keine Tests**
5. **Dependencies ignorieren**
6. **Veraltete Status**
7. **Parallele Tasks** (max. 1-2)

## Siehe auch

- [workflow.md](./workflow.md) - Detaillierter Workflow
- [filesystem.md](./filesystem.md) - Filesystem-spezifisch
- [linear.md](./linear.md) - Linear-spezifisch
- [troubleshooting.md](./troubleshooting.md) - Problemlösungen

