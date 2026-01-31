# Professional Init-Project Skill

Initialisiert Open-Source-Projekte mit GitHub Best Practices und professioneller Git-Branching-Strategie.

## Version 1.0.0

---

## Features

- **Git-Branching**: develop → main Strategie als Standard
- **Java/Gradle**: Kotlin DSL mit Java 21 Toolchain
- **Python/uv**: Moderne Python-Projektverwaltung
- **Community Standards**: LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY
- **GitHub Templates**: Issue-Templates, PR-Template, Workflows

---

## Usage

### Via Command

```bash
/development:init-project --with-skills --java --name "my-app"
```

### Direkte Script-Ausführung

```bash
cd plugins/development/skills/professional-init-project
python scripts/main.py --type java --name my-app
```

### Optionen

| Option | Beschreibung |
|--------|--------------|
| `--type` | Projekttyp: git, java, uv, node, go, rust |
| `--name` | Projektname (kebab-case empfohlen) |
| `--no-branching` | Nur main-Branch, kein develop |
| `--license` | Lizenztyp: mit, apache2, gpl3, bsd3 |

---

## Projekttypen

### Java (`--type java`)

- Gradle Kotlin DSL (build.gradle.kts)
- Java 21 Toolchain
- JUnit 5 Test-Framework
- Gradle Wrapper inkludiert

### Python (`--type uv`)

- uv Package Manager
- pyproject.toml mit Ruff-Konfiguration
- pytest Test-Framework
- src-Layout

### Git (`--type git`)

- Minimales Setup
- Spracherkennung aus bestehenden Dateien
- Passende .gitignore

---

## Git-Branching-Strategie

```
develop (default, aktive Entwicklung)
    │
    ├── feature/xyz
    ├── fix/abc
    │
    └── → main (stabile Releases)
```

- **develop**: Standardbranch für Entwicklung
- **main**: Nur stabile, getestete Releases
- **feature/**: Neue Features
- **fix/**: Bugfixes

---

## Verzeichnisstruktur

```
professional-init-project/
├── SKILL.md              # Skill-Definition
├── README.md             # Diese Datei
├── scripts/
│   ├── main.py           # Entry-Point
│   ├── git_initializer.py
│   └── generators/
│       ├── java_gradle.py
│       ├── python_uv.py
│       └── common.py
├── templates/
│   ├── java/
│   ├── python/
│   └── common/
├── config/
│   └── project_types.json
└── docs/
    ├── branching-strategy.md
    └── troubleshooting.md
```

---

## Konfiguration

### project_types.json

```json
{
  "java": {
    "build_tool": "gradle-kotlin",
    "java_version": 21,
    "test_framework": "junit5",
    "gradle_version": "8.12"
  },
  "python": {
    "package_manager": "uv",
    "python_version": "3.12",
    "test_framework": "pytest"
  }
}
```

---

## Beispiel-Output

```
✓ Git-Repository initialisiert
✓ Branch 'develop' erstellt (aktiv)
✓ Projektstruktur generiert (Java/Gradle)
✓ Community Standards erstellt
✓ GitHub Templates erstellt
✓ Initialer Commit erstellt
✓ Branch 'main' erstellt (synchron mit develop)

📁 Projekt bereit: my-app/
   Branch: develop (aktiv)
   Nächster Schritt: ./gradlew build
```

---

## Related

- [/development:init-project](../../commands/init-project.md) - Command-Dokumentation
- [java-developer Agent](../../agents/java-developer.md) - Java-Entwicklungsunterstützung

---

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE)

---

**Made with care by Talent Factory GmbH**
