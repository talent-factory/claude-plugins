---
name: update-documents
description: Synchronizes documentation between CLAUDE.md, README.md, and docs/. Resolves documentation inconsistencies across project files with configurable sync rules and whitespace-tolerant comparison.
---

# Update Documentation

Automatically synchronize project documentation between the various documentation files.

## Sync Rules

| Source | Section | Targets |
|--------|---------|---------|
| CLAUDE.md | Tech Stack | README.md, docs/index.md |
| CLAUDE.md | Development Commands | README.md, docs/development/local-setup.md |
| CLAUDE.md | Project Structure | README.md |
| README.md | Quick Start | docs/getting-started/quickstart.md |

**Principle:** CLAUDE.md is the technical source of truth; README.md is the user-facing entry document.

## Workflow

### 1. Run Analysis

First check the current sync status:

```bash
cd ${PROJECT_ROOT} && python ${SKILL_DIR}/scripts/main.py --analyze
```

### 2. Interpret Output

The script displays:

- Synchronized: sections are identical
- Outdated: target differs from source
- Missing: section does not exist

### 3. Synchronize When Differences Are Found

If differences were found:

```bash
cd ${PROJECT_ROOT} && python ${SKILL_DIR}/scripts/main.py --sync
```

### 4. Review Results

After synchronization:

- Check the updated files for correct formatting
- Ensure no context-specific adjustments were lost
- If needed: manual post-processing for target-specific phrasing

### 5. Output Summary

Provide the user with a brief summary:

```
Documentation synchronized

Updated:
  - README.md: Tech Stack, Development
  - docs/index.md: Tech Stack

Unchanged:
  - docs/getting-started/quickstart.md
```

## Customize Configuration

The sync rules are defined in `${SKILL_DIR}/config/sync_rules.json`.

Add a new rule:

```json
{
  "id": "new-rule",
  "source": {"file": "SOURCE.md", "section": "Section Name"},
  "targets": [
    {"file": "TARGET.md", "section": "Target Section"}
  ]
}
```

## Notes

- **No automatic commits**: The skill only modifies files, it does not commit
- **Whitespace-tolerant**: Minor formatting differences are ignored
- **Section matching**: Case-insensitive heading search
- **Backup**: Create manually before synchronization if needed
