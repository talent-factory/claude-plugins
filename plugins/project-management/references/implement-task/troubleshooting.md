# Troubleshooting: Task Implementation

Häufige Probleme bei der Implementierung von Tasks und deren Lösungen.

## Task-Identifikation

### Task nicht gefunden

**Symptom**:
```
❌ Error: Task [ID] not found
```

**Lösungen**:

**Filesystem**:
```bash
# Alle Tasks auflisten
find .plans -name "task-*.md"

# Mit Plan-Kontext suchen
/implement-task --plan dark-mode-toggle task-001
```

**Linear**:
```bash
# Issue-ID validieren (Format: [A-Z]+-[0-9]+)
# Beispiel: PROJ-123, nicht proj-123

# API-Test
curl -H "Authorization: Bearer $LINEAR_API_KEY" \
  https://api.linear.app/graphql \
  -d '{"query":"query{issue(id:\"PROJ-123\"){id title}}"}'
```

## Worktree-Probleme

### Worktree existiert bereits

**Symptom**:
```
❌ fatal: '.worktrees/task-001' already exists
```

**Lösungen**:

1. **In existierenden Worktree wechseln**:
   ```bash
   cd .worktrees/task-001
   # Weiterarbeiten
   ```

2. **Worktree entfernen und neu erstellen**:
   ```bash
   git worktree remove .worktrees/task-001
   git worktree add -b feature/task-001-desc .worktrees/task-001 origin/main
   ```

3. **Verwaisten Worktree bereinigen** (falls Verzeichnis manuell gelöscht wurde):
   ```bash
   git worktree prune
   git worktree add -b feature/task-001-desc .worktrees/task-001 origin/main
   ```

### Worktree-Verzeichnis fehlt

**Symptom**:
```
❌ Error: .worktrees directory not found
```

**Lösung**:
```bash
mkdir -p .worktrees
# Dann erneut versuchen
```

### Branch bereits in anderem Worktree ausgecheckt

**Symptom**:
```
❌ fatal: 'feature/task-001-...' is already checked out at '/path/to/.worktrees/...'
```

**Lösungen**:

1. **Anderen Worktree finden und verwenden**:
   ```bash
   git worktree list
   # Zeigt: .worktrees/task-001  abc1234 [feature/task-001-desc]
   cd .worktrees/task-001
   ```

2. **Alten Worktree entfernen**:
   ```bash
   git worktree remove /path/to/old/worktree
   # Dann neu erstellen
   ```

### Alle Worktrees auflisten

**Diagnose**:
```bash
git worktree list
# Ausgabe:
# /path/to/main           abc1234 [main]
# /path/to/.worktrees/task-001  def5678 [feature/task-001-desc]
```

### Verwaiste Worktrees bereinigen

**Symptom**: Worktree-Verzeichnis wurde manuell gelöscht, Git kennt es noch

**Lösung**:
```bash
git worktree prune
git worktree list  # Verifizieren
```

### Worktree nach Merge aufräumen

**Nach erfolgreichem PR-Merge**:
```bash
# Vom Hauptrepo aus (NICHT aus dem Worktree!)
cd /path/to/main/repo

# 1. Worktree entfernen
git worktree remove .worktrees/task-001

# 2. Lokalen Branch löschen
git branch -d feature/task-001-desc

# 3. Remote-Branch löschen (optional, meist via PR erledigt)
git push origin --delete feature/task-001-desc
```

## Submodule-Probleme

### Submodule nicht initialisiert im Worktree

**Symptom**:
```
❌ Submodule path 'libs/shared' not initialized
```

**Lösung**:
```bash
cd .worktrees/task-001
git submodule update --init --recursive
```

### Branch-Konflikt in Submodul

**Symptom**:
```
❌ fatal: A branch named 'feature/task-001-...' already exists in submodule
```

**Lösungen**:

1. **Existierenden Branch verwenden**:
   ```bash
   cd .worktrees/task-001/libs/shared
   git checkout feature/task-001-desc
   ```

2. **Branch in Submodul löschen und neu erstellen**:
   ```bash
   cd .worktrees/task-001/libs/shared
   git branch -D feature/task-001-desc
   git checkout -b feature/task-001-desc origin/main
   ```

### Submodule-Status prüfen

**Diagnose**:
```bash
cd .worktrees/task-001

# Alle Submodule und deren Branches anzeigen
git submodule foreach --recursive 'echo "=== $name ===" && git branch --show-current'

# Submodule-Status
git submodule status --recursive
```

### Submodule-Branches nach Merge aufräumen

**Nach erfolgreichem PR-Merge**:
```bash
# Vom Worktree aus
cd .worktrees/task-001

# Alle Submodule auf main zurücksetzen und Branches löschen
git submodule foreach --recursive '
  git checkout main
  git pull origin main
  git branch -d "feature/task-001-desc" 2>/dev/null || echo "Branch not found in $name"
'
```

### Submodule zeigt "detached HEAD"

**Symptom**:
```
HEAD detached at abc1234
```

**Ursache**: Submodul wurde nicht auf Branch ausgecheckt

**Lösung**:
```bash
cd .worktrees/task-001/libs/shared
git checkout -b feature/task-001-desc
# oder falls Branch existiert:
git checkout feature/task-001-desc
```

## Branch-Probleme

### Branch existiert bereits

**Symptom**:
```
⚠️ Branch feature/proj-123-... already exists
```

**Lösungen**:

1. **Existierenden Worktree mit diesem Branch finden**:
   ```bash
   git worktree list | grep "feature/proj-123"
   ```

2. **Branch löschen und neu erstellen** (falls kein Worktree):
   ```bash
   git branch -D feature/proj-123-user-auth
   git worktree add -b feature/proj-123-user-auth .worktrees/task-proj-123 origin/main
   ```

3. **Anderen Task wählen**

### Working Directory nicht sauber

**Symptom**:
```
❌ Error: Working directory not clean
```

**Lösungen**:

```bash
# Option 1: Committen
/commit

# Option 2: Stashen
git stash save "WIP before implementing task"

# Option 3: Verwerfen (Vorsicht!)
git reset --hard HEAD
```

> 💡 **Hinweis**: Bei Worktrees ist das Hauptrepo oft sauber, da Änderungen im Worktree isoliert sind.

### Remote nicht up-to-date

**Symptom**:
```
⚠️ Local branch is behind remote
```

**Lösung**:
```bash
git fetch origin
git pull --rebase origin main
```

## Status-Update Probleme

### Filesystem: Status-Update schlägt fehl

**Symptom**:
```
❌ Could not update task status
Old string not found: "- **Status**: pending"
```

**Ursache**: Format in Task-Datei weicht ab

**Lösung**: Task-Datei manuell korrigieren:
```markdown
- **Status**: pending
```

### Linear: MCP Server nicht verfügbar

**Symptom**:
```
❌ Linear MCP server not available
```

**Diagnose**:
```bash
# MCP-Konfiguration prüfen
cat ~/.config/claude/mcp_config.json

# API Key testen
echo $LINEAR_API_KEY
curl -H "Authorization: Bearer $LINEAR_API_KEY" \
  https://api.linear.app/graphql \
  -d '{"query":"{ viewer { id } }"}'
```

**Lösung**: MCP-Konfiguration erstellen:
```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-linear"],
      "env": { "LINEAR_API_KEY": "${LINEAR_API_KEY}" }
    }
  }
}
```

### Linear: API Key ungültig

**Symptom**:
```
❌ Error 401: Unauthorized
```

**Lösung**:
1. Neuen Key generieren: https://linear.app → Settings → API
2. In `~/.env` aktualisieren:
   ```bash
   export LINEAR_API_KEY="lin_api_NEW_KEY"
   source ~/.env
   ```

## PR-Erstellung Probleme

### GitHub CLI nicht authentifiziert

**Symptom**:
```
❌ gh: Not authenticated
```

**Lösung**:
```bash
gh auth login
# Folge dem Browser-Login
gh auth status  # Verifizieren
```

### Keine Commits für PR

**Symptom**:
```
❌ No commits between main and feature-branch
```

**Lösung**:
```bash
# Änderungen committen
git add .
git commit -m "✨ feat: Implement feature"

# Dann PR erstellen
/create-pr
```

## Finalisierung Probleme

### Task bleibt in_progress nach PR

**Symptom**: Task-Status ist noch `in_progress` obwohl PR erstellt

**Lösung**:

**Filesystem**:
```bash
# Task-Status manuell setzen
# Edit: - **Status**: completed
# Edit: - **Updated**: <heute>

# STATUS.md regenerieren
git add .plans/*/tasks/*.md .plans/*/STATUS.md
git commit -m "✅ chore: Mark task as completed"
```

**Linear**:
```bash
# Issue-Status in Linear auf "In Review" oder "Done" setzen
```

## Performance-Probleme

### Command hängt

**Symptom**: Keine Ausgabe für >5 Minuten

**Lösungen**:
1. `Ctrl+C` zum Abbrechen
2. Rate Limit prüfen (Linear: 1200 req/hour)
3. Neu starten mit Debug: `export DEBUG=*`

### Suche zu langsam (Filesystem)

**Symptom**: Task-Suche dauert >5 Sekunden

**Lösung**: Plan-Kontext angeben
```bash
# Statt
/implement-task task-001

# Besser
/implement-task --plan dark-mode task-001
```

## Quick Reference: Worktree-Befehle

```bash
# === WORKTREE ERSTELLEN ===
mkdir -p .worktrees
git worktree add -b feature/task-001-desc .worktrees/task-001 origin/main
cd .worktrees/task-001

# === SUBMODULE INITIALISIEREN ===
git submodule update --init --recursive
git submodule foreach --recursive 'git checkout -b feature/task-001-desc origin/main'

# === WORKTREE AUFLISTEN ===
git worktree list

# === WORKTREE ENTFERNEN ===
git worktree remove .worktrees/task-001
git branch -d feature/task-001-desc

# === VERWAISTE WORKTREES BEREINIGEN ===
git worktree prune

# === SUBMODULE-STATUS ===
git submodule foreach --recursive 'echo "=== $name ===" && git branch --show-current'
```

## Siehe auch

- [workflow.md](./workflow.md) - Detaillierter Workflow
- [best-practices.md](./best-practices.md) - Best Practices
- [filesystem.md](./filesystem.md) - Filesystem-spezifisch
- [linear.md](./linear.md) - Linear-spezifisch

