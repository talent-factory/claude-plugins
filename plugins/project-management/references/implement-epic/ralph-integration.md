# Ralph Wiggum Integration

Konfiguration und Best Practices für die Integration des Ralph Wiggum Plugins.

## Installation

### Plugin installieren

```bash
# In Claude Code
/plugin install ralph-wiggum@claude-plugins-official

# Verfügbarkeit prüfen
claude plugins list
```

### Dependency in plugin.json

```json
{
  "name": "project-management",
  "version": "2.3.0",
  "dependencies": {
    "ralph-wiggum": "claude-plugins-official"
  }
}
```

## Ralph Wiggum Konzepte

### Stop-Hook Mechanismus

Ralph Wiggum verwendet einen Stop-Hook, der Claude's Exit-Versuche abfängt:

```
┌─────────────────────────────────────────────────────────┐
│                     Claude Session                      │
│                                                         │
│  1. Prompt eingeben                                     │
│           ▼                                             │
│  2. Claude arbeitet...                                  │
│           ▼                                             │
│  3. Claude versucht zu beenden                          │
│           ▼                                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │              STOP HOOK                          │   │
│  │                                                 │   │
│  │  Completion-Promise gefunden?                   │   │
│  │     ├── JA → Exit erlauben                      │   │
│  │     └── NEIN → Prompt erneut injizieren         │   │
│  └─────────────────────────────────────────────────┘   │
│           ▼                                             │
│  4. Zurück zu Schritt 2 (mit Dateien als Kontext)      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Completion-Promise

Der Hook prüft auf exakte String-Matches:

```bash
# Einfaches Promise
/ralph-loop "..." --completion-promise "COMPLETE"

# Mehrere Möglichkeiten (Regex-ähnlich)
/ralph-loop "..." --completion-promise "SUCCESS|FAILED|BLOCKED"
```

## Integration in EPIC-Workflow

### Implementation-Loop Konfiguration

```bash
/ralph-loop "
Implementiere Task {task_id}: {title}

## Beschreibung
{description}

## Akzeptanzkriterien
{acceptance_criteria}

## Erfolgsbedingungen
Wenn ALLE Kriterien erfüllt sind:
1. Alle Tests bestehen
2. Code ist committet
3. PR ist erstellt

Output: <promise>TASK_COMPLETE</promise>

## Fehlerbedingungen
Bei unlösbaren Blockern:
- Dokumentiere in BLOCKER.md
- Beschreibe was fehlt

Output: <promise>TASK_BLOCKED</promise>
" --max-iterations 30 --completion-promise "TASK_COMPLETE|TASK_BLOCKED"
```

### Review-Loop Konfiguration

```bash
/ralph-loop "
Review PR #{pr_number} für Task {task_id}

## Aufgabe
1. gh pr diff laden
2. Code-Review durchführen
3. Alle Issues selbst beheben
4. Fixes committen

## Erfolgsbedingungen
Wenn alle Issues behoben:
Output: <promise>REVIEW_COMPLETE</promise>

## User-Eingriff nötig
Bei Problemen die Entscheidung benötigen:
- Dokumentiere in PR-Kommentar
Output: <promise>REVIEW_NEEDS_ATTENTION</promise>
" --max-iterations 15 --completion-promise "REVIEW_COMPLETE|REVIEW_NEEDS_ATTENTION"
```

## Prompt-Engineering für Ralph

### Gute Prompts

**Klare Struktur**:
```
# Aufgabe
[Was zu tun ist]

# Kontext
[Relevante Informationen]

# Schritte
1. [Schritt 1]
2. [Schritt 2]
...

# Erfolgskriterien
[Wann ist die Aufgabe erledigt?]

# Completion
Output: <promise>DONE</promise>
```

**Testbare Kriterien**:
```
## Akzeptanzkriterien
- [ ] Unit-Tests bestehen (npm test)
- [ ] Lint-Checks bestehen (npm run lint)
- [ ] Coverage > 80%
- [ ] Keine TypeScript-Errors
```

**Escape-Hatch**:
```
## Fallback
Falls nach 20 Iterationen nicht abgeschlossen:
1. Dokumentiere aktuellen Stand
2. Liste offene Punkte
3. Output: <promise>PARTIAL_COMPLETE</promise>
```

### Schlechte Prompts

**Vage Ziele**:
```
❌ "Mach den Code besser"
✅ "Refactore AuthService: Extrahiere JWT-Logik in separate Klasse"
```

**Keine Exit-Bedingung**:
```
❌ "Implementiere Feature X"
✅ "Implementiere Feature X. Output <promise>DONE</promise> wenn alle Tests grün"
```

**Zu viele Aufgaben**:
```
❌ "Baue komplettes E-Commerce-System"
✅ "Implementiere User-Registrierung mit Email-Verifizierung"
```

## Iteration-Limits

### Empfohlene Werte

| Task-Typ | Max Iterations | Begründung |
|----------|----------------|------------|
| Kleiner Task (1-2 SP) | 15-20 | Sollte schnell abschliessbar sein |
| Mittlerer Task (3-5 SP) | 25-35 | Mehr Komplexität erlaubt |
| Grosser Task (8+ SP) | 40-50 | Besser aufteilen! |
| Review | 10-15 | Reviews sind fokussiert |

### Kosten-Kalkulation

```
Kosten ≈ Iterations × Tokens_pro_Iteration × API_Preis

Beispiel (Sonnet):
- 30 Iterations
- ~4000 Tokens/Iteration
- $0.003/1K Input + $0.015/1K Output

≈ 30 × 4000 × ($0.003 + $0.015) / 1000
≈ $2.16 pro Task
```

## Parallele Ralph-Loops

### Architektur

```
Terminal 1                Terminal 2                Terminal 3
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│ Worktree     │         │ Worktree     │         │ Worktree     │
│ task-001     │         │ task-002     │         │ task-004     │
│              │         │              │         │              │
│ Ralph-Loop   │         │ Ralph-Loop   │         │ Ralph-Loop   │
│ (impl)       │         │ (impl)       │         │ (impl)       │
└──────────────┘         └──────────────┘         └──────────────┘
       │                        │                        │
       └────────────────────────┼────────────────────────┘
                                │
                         ┌──────┴──────┐
                         │ Shared Git  │
                         │ Repository  │
                         └─────────────┘
```

### Konflikt-Vermeidung

1. **Separate Worktrees**: Jeder Task in eigenem Verzeichnis
2. **Separate Branches**: Kein Branch-Sharing
3. **Gemeinsame Dateien vermeiden**: Tasks sollten unterschiedliche Bereiche ändern
4. **Regelmässiges Rebase**: `git fetch && git rebase origin/main`

## Memory-Management

### Kontext-Rotation

Ralph-Loops können lange laufen und viel Kontext akkumulieren:

```python
# Orchestrator spawnt Task-Agents mit frischem Kontext
spawn_subagent(
    type="implementation",
    fresh_context=True,  # Kein History-Bloat
    memory_handoff={     # Nur essentielles
        'task': task.to_dict(),
        'worktree': worktree_path,
        'iteration': current_iteration
    }
)
```

### File-basierte Kommunikation

Statt grosse Kontexte zu übergeben:

```
.worktrees/task-001/
├── .claude/
│   ├── context.json    # Aktueller Stand
│   ├── progress.md     # Was wurde gemacht
│   └── blockers.md     # Bekannte Probleme
```

## Debugging

### Loop-Status prüfen

```bash
# Aktive Loops anzeigen (in anderem Terminal)
claude process list

# Logs eines Tasks
cat .plans/feature/.orchestrator/logs/task-001.log
```

### Manueller Eingriff

```bash
# Loop stoppen
/cancel-ralph

# Manuell fortsetzen
cd .worktrees/task-001
# ... Fixes machen ...
git add . && git commit -m "fix: manual intervention"

# Loop neu starten
/ralph-loop "..." --max-iterations 10
```

### Häufige Probleme

| Problem | Lösung |
|---------|--------|
| Loop terminiert nicht | Completion-Promise prüfen, Prompt anpassen |
| Zu viele Iterationen | Prompt spezifischer machen |
| Falsche Completion | Promise-String genau prüfen (Whitespace!) |
| Memory-Overflow | Task aufteilen, Kontext-Rotation nutzen |
