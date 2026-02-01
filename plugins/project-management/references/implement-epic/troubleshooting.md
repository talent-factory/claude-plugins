# Troubleshooting

Häufige Probleme und Lösungen bei der EPIC-Implementation.

## Orchestrator-Probleme

### EPIC wird nicht gefunden

**Symptom**:
```
Error: EPIC 'feature-x' not found
```

**Ursachen & Lösungen**:

1. **Falscher Pfad**
   ```bash
   # Prüfen
   ls -la .plans/

   # Korrekter Aufruf
   /implement-epic --plan .plans/feature-x/
   ```

2. **EPIC.md fehlt**
   ```bash
   # EPIC neu erstellen
   /create-plan --prd PRD.md
   ```

3. **Linear-Flag vergessen**
   ```bash
   # Für Linear-EPICs
   /implement-epic --linear PROJ-123
   ```

### Circular Dependency Error

**Symptom**:
```
Error: Circular dependency detected: task-001 → task-003 → task-001
```

**Lösung**:
```bash
# Dependencies prüfen
grep -r "Requires:" .plans/feature-x/tasks/

# Zirkuläre Referenz auflösen
# In task-001.md:
# - Requires: task-003  ← Entfernen oder Task aufteilen
```

### Keine Tasks startbar

**Symptom**:
```
Warning: No tasks ready to start (all blocked or completed)
```

**Ursachen**:

1. **Alle Tasks haben Dependencies**
   ```bash
   # Mindestens ein Task ohne Requires nötig
   cat .plans/feature-x/tasks/task-001.md | grep "Requires"
   # Sollte "Requires: None" sein
   ```

2. **Tasks bereits in Bearbeitung**
   ```bash
   # Status prüfen
   cat .plans/feature-x/STATUS.md
   ```

## Ralph-Loop-Probleme

### Loop terminiert nicht

**Symptom**:
Loop läuft endlos, erreicht max-iterations.

**Lösungen**:

1. **Completion-Promise prüfen**
   ```bash
   # Promise muss exakt im Output erscheinen
   # Falsch:
   Output: TASK_COMPLETE

   # Richtig:
   <promise>TASK_COMPLETE</promise>
   ```

2. **Prompt anpassen**
   ```markdown
   # Klarere Erfolgskriterien
   Wenn diese Bedingungen erfüllt sind:
   1. npm test erfolgreich (exit code 0)
   2. npm run lint ohne Errors

   Dann output GENAU diesen Text:
   <promise>TASK_COMPLETE</promise>
   ```

3. **Fallback einbauen**
   ```markdown
   Nach 25 Iterationen, falls nicht abgeschlossen:
   1. Dokumentiere Fortschritt in PROGRESS.md
   2. Liste offene Punkte
   3. <promise>TASK_PARTIAL</promise>
   ```

### Falsche Completion

**Symptom**:
Loop endet obwohl Task nicht fertig ist.

**Ursachen**:

1. **Promise zu früh ausgegeben**
   ```markdown
   # Prompt anpassen
   WICHTIG: Output <promise>TASK_COMPLETE</promise> NUR wenn:
   - Alle Tests grün (npm test zeigt "X passing, 0 failing")
   - Kein ESLint-Error
   - Änderungen committed
   ```

2. **Versehentlicher Match**
   ```bash
   # Wenn Code "TASK_COMPLETE" enthält
   # Eindeutigeres Promise verwenden
   --completion-promise "RALPH_EPIC_TASK_001_COMPLETE"
   ```

### Memory/Context Issues

**Symptom**:
Loop wird langsamer, Kontext-Overflow Fehler.

**Lösungen**:

1. **Kontext-Rotation aktivieren**
   ```python
   # Im Orchestrator
   spawn_subagent(
       fresh_context=True,
       memory_handoff='minimal'  # Nur essentielles übergeben
   )
   ```

2. **Tasks aufteilen**
   ```bash
   # Statt einem grossen Task
   task-001: Komplettes Auth-System  # 13 SP ← Zu gross!

   # Mehrere kleine
   task-001a: Auth-Service Grundgerüst  # 3 SP
   task-001b: JWT-Integration            # 3 SP
   task-001c: Password-Hashing           # 2 SP
   task-001d: Auth-Tests                 # 3 SP
   ```

## Worktree-Probleme

### Worktree existiert bereits

**Symptom**:
```
fatal: '.worktrees/task-001' already exists
```

**Lösungen**:

1. **Existierenden nutzen**
   ```bash
   cd .worktrees/task-001
   git status  # Prüfen was dort ist
   ```

2. **Cleanup und neu erstellen**
   ```bash
   git worktree remove .worktrees/task-001 --force
   git worktree add -b feature/task-001 .worktrees/task-001 origin/main
   ```

### Branch existiert bereits

**Symptom**:
```
fatal: A branch named 'feature/task-001' already exists
```

**Lösungen**:

1. **Existierenden Branch nutzen**
   ```bash
   git worktree add .worktrees/task-001 feature/task-001
   ```

2. **Branch löschen (wenn nicht mehr gebraucht)**
   ```bash
   git branch -D feature/task-001
   git worktree add -b feature/task-001 .worktrees/task-001 origin/main
   ```

### Submodule nicht initialisiert

**Symptom**:
```
Error: Submodule 'libs/shared' not initialized
```

**Lösung**:
```bash
cd .worktrees/task-001
git submodule update --init --recursive
```

## Git-Probleme

### Merge-Konflikte

**Symptom**:
```
CONFLICT (content): Merge conflict in src/utils.ts
```

**Automatische Lösung (im Ralph-Loop)**:
```markdown
Bei Merge-Konflikten:
1. git fetch origin
2. git rebase origin/main
3. Bei Konflikten:
   - Analysiere beide Versionen
   - Wähle sinnvollste Lösung
   - git add <file>
   - git rebase --continue
4. Falls unlösbar: <promise>TASK_BLOCKED</promise>
```

**Manuelle Lösung**:
```bash
cd .worktrees/task-001
git status  # Konflikt-Dateien sehen
# Manuell auflösen
git add .
git rebase --continue
```

### Push rejected

**Symptom**:
```
! [rejected] feature/task-001 -> feature/task-001 (non-fast-forward)
```

**Lösung**:
```bash
cd .worktrees/task-001
git fetch origin
git rebase origin/feature/task-001
git push --force-with-lease
```

## PR-Probleme

### Draft-PR kann nicht erstellt werden

**Symptom**:
```
Error: Failed to create pull request
```

**Ursachen & Lösungen**:

1. **gh nicht authentifiziert**
   ```bash
   gh auth status
   gh auth login
   ```

2. **Branch nicht gepusht**
   ```bash
   git push -u origin feature/task-001
   ```

3. **Repository-Rechte fehlen**
   ```bash
   # Fork statt Push zu Original
   gh repo fork
   git remote add fork <fork-url>
   git push fork feature/task-001
   gh pr create --repo original/repo --head fork:feature/task-001
   ```

### Review-Änderungen werden nicht erkannt

**Symptom**:
Review-Loop behebt Issues, aber PR zeigt keine Änderungen.

**Lösung**:
```bash
# Im Worktree
cd .worktrees/task-001
git status  # Gibt es unstaged Änderungen?
git add .
git commit -m "fix: Addressed review comments"
git push
```

## Performance-Probleme

### Zu hohe CPU/Memory-Nutzung

**Symptom**:
System wird langsam, Agents crashen.

**Lösungen**:

1. **Parallelität reduzieren**
   ```bash
   /implement-epic feature-x --max-parallel 2
   ```

2. **Iterations begrenzen**
   ```bash
   /implement-epic feature-x --max-iterations 20
   ```

3. **Pausen einbauen**
   ```python
   # Im Orchestrator
   after_each_task_complete:
       await asyncio.sleep(5)  # 5 Sekunden Pause
   ```

### Zu hohe API-Kosten

**Symptom**:
Kosten explodieren.

**Lösungen**:

1. **Dry-Run zuerst**
   ```bash
   /implement-epic feature-x --dry-run
   # Zeigt geschätzte Kosten
   ```

2. **Kleinere Tasks**
   ```bash
   # Statt 5 Tasks à 8 SP
   # Besser: 10 Tasks à 3-4 SP
   ```

3. **Effizientere Prompts**
   ```markdown
   # Kürzere, fokussiertere Prompts
   # Weniger Kontext = weniger Tokens
   ```

## Recovery

### Nach Crash fortsetzen

```bash
# Orchestrator-State prüfen
cat .plans/feature-x/.orchestrator/state.json

# Fortsetzen
/implement-epic feature-x --resume

# Oder: Spezifischen Task fortsetzen
/implement-task task-001 --continue
```

### Cleanup nach Abbruch

```bash
# Alle Worktrees auflisten
git worktree list

# Nicht mehr gebrauchte entfernen
git worktree remove .worktrees/task-001 --force

# Verwaiste Branches löschen
git branch -D feature/task-001

# Orchestrator-State zurücksetzen
rm -rf .plans/feature-x/.orchestrator/
```

## Debugging

### Verbose-Modus

```bash
/implement-epic feature-x --verbose
# Zeigt detaillierte Logs
```

### Einzelnen Task debuggen

```bash
# Task manuell starten
cd .worktrees/task-001

# Ohne Ralph-Loop, interaktiv
claude
> Implementiere Task task-001...
```

### Logs analysieren

```bash
# Orchestrator-Logs
tail -f .plans/feature-x/.orchestrator/logs/orchestrator.log

# Task-spezifische Logs
cat .plans/feature-x/.orchestrator/logs/task-001.log
```
