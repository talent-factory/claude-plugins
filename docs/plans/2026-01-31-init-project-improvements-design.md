# Design: Init-Project Improvements

**Datum:** 2026-01-31
**Status:** Approved
**Autor:** Claude Code

## Übersicht

Verbesserung des `/development:init-project` Commands mit:
- Git-Branching-Strategie (develop → main)
- Java/Gradle Kotlin DSL Support
- `--with-skills` Parameter für Skill-basierten Workflow

---

## Teil 1: Architektur

### Kern-Änderungen

**1. Git-Branching (IMMER aktiv bei Git-Projekten):**
```bash
git init
git checkout -b develop          # Start auf develop
git commit --allow-empty -m "Initial commit"
git branch main                  # main von develop erstellen
git push -u origin develop main  # Beide Branches pushen (wenn Remote)
# Bleibt auf develop für Weiterentwicklung
```

**2. Java-Projekte: Gradle Kotlin DSL als Standard**
- `build.gradle.kts` statt `build.gradle`
- Moderne Toolchain-Konfiguration
- Vorkonfiguriert für Java 21

**3. Skill-Struktur:**
```
plugins/development/skills/
└── professional-init-project/
    ├── SKILL.md                 # Skill-Definition
    ├── scripts/
    │   ├── main.py              # Haupt-Entry-Point
    │   ├── git_initializer.py   # Git + Branch-Setup
    │   ├── project_detector.py  # Projekttyp-Erkennung
    │   └── generators/
    │       ├── java_gradle.py   # Java/Gradle Generator
    │       ├── python_uv.py     # Python/uv Generator
    │       └── common.py        # Gemeinsame Dateien
    └── templates/               # Datei-Templates
```

---

## Teil 2: Command-Änderungen

### Aktualisierte Parameter

```bash
# Bestehende Parameter (bleiben)
/init-project --git              # Standard Git-Projekt
/init-project --uv               # Python mit uv
/init-project --interactive      # Interaktiver Modus
/init-project --name "projekt"   # Projektname

# Neue Parameter
/init-project --with-skills      # Skill-basierter Workflow
/init-project --java             # Java/Gradle Kotlin DSL (NEU)
/init-project --no-branching     # Nur main, kein develop (Opt-out)
```

### Geändertes Verhalten

**Standard-Git-Workflow (bei allen --git, --java, --uv):**
```bash
# 1. Repository initialisieren
git init

# 2. Auf develop starten
git checkout -b develop

# 3. Projekt-Dateien erstellen (LICENSE, README, etc.)

# 4. Initialer Commit
git add .
git commit -m "feat: Initial open source setup"

# 5. main Branch erstellen (synchron mit develop)
git branch main

# 6. Optional: Remote hinzufügen
gh repo create [name] --public
git push -u origin develop main
git remote set-head origin develop  # develop als Default
```

---

## Teil 3: Gradle Kotlin DSL Templates

### build.gradle.kts

```kotlin
plugins {
    java
    application
}

group = "com.example"
version = "0.1.0"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

repositories {
    mavenCentral()
}

dependencies {
    // Testing
    testImplementation(platform("org.junit:junit-bom:5.11.4"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

application {
    mainClass = "com.example.App"
}

tasks.test {
    useJUnitPlatform()
    testLogging {
        events("passed", "skipped", "failed")
    }
}
```

### settings.gradle.kts

```kotlin
rootProject.name = "project-name"
```

### Projektstruktur

```
project-name/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/App.java
│   │   └── resources/
│   └── test/
│       ├── java/
│       │   └── com/example/AppTest.java
│       └── resources/
├── .gitignore
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── SECURITY.md
```

### .gitignore (Java/Gradle)

```gitignore
# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar

# IDE
.idea/
*.iml
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

## Teil 4: Skill SKILL.md Definition

Siehe `plugins/development/skills/professional-init-project/SKILL.md`

---

## Teil 5: Implementierungsplan

### Zu erstellende Dateien

```
plugins/development/
├── .claude-plugin/plugin.json        # Version 1.2.0
├── commands/init-project.md          # Aktualisiert
├── skills/
│   └── professional-init-project/
│       ├── SKILL.md                  # Skill-Definition
│       ├── README.md                 # Dokumentation
│       ├── scripts/
│       │   ├── main.py               # Entry-Point
│       │   ├── git_initializer.py    # Git + Branching
│       │   └── generators/
│       │       ├── java_gradle.py    # Java/Gradle Generator
│       │       ├── python_uv.py      # Python/uv Generator
│       │       └── common.py         # Community Standards
│       ├── templates/
│       │   ├── java/                 # Java Templates
│       │   ├── python/               # Python Templates
│       │   └── common/               # Gemeinsame Templates
│       └── config/
│           └── project_types.json    # Konfiguration
└── README.md                         # Aktualisiert
```

### Implementierungsreihenfolge

1. Command aktualisieren - init-project.md mit neuen Parametern
2. Skill-Grundstruktur - SKILL.md, README.md, config/
3. Git-Initializer - scripts/git_initializer.py
4. Generators - Java/Gradle, Python/uv, Common
5. Templates - Alle Datei-Templates
6. Main-Script - Entry-Point mit Orchestrierung
7. Plugin-Version - Bump auf 1.2.0
8. Tests - Manueller Test aller Projekttypen
