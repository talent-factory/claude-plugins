---
name: professional-init-project
description: Initialisiert Open-Source-Projekte mit GitHub Best Practices und Git-Branching-Strategie
version: 1.0.1
---

# Professional Init-Project Workflow

Dieser Skill führt dich durch die Projekt-Initialisierung. **Folge diesen Anweisungen Schritt für Schritt.**

## WICHTIGE REGELN

1. **Java-Projekte verwenden IMMER Gradle Kotlin DSL** - NIEMALS Maven!
2. **Initialer Commit MUSS über `/git-workflow:commit` erfolgen** - NIEMALS direkt `git commit`!
3. **Git-Branching: develop → main** ist der Standard

---

## Schritt 1: Projekttyp und Parameter erkennen

Analysiere die Argumente des Users:

| Argument | Projekttyp | Build-Tool |
|----------|-----------|------------|
| `--java` | Java | **Gradle Kotlin DSL** (NICHT Maven!) |
| `--uv` | Python | uv |
| `--git` | Standard | - |
| `--node` | Node.js | npm/pnpm |

Optionale Argumente:
- `--name "xyz"`: Projektname
- `--no-branching`: Nur main, kein develop

---

## Schritt 2: Projektverzeichnis erstellen

```bash
# Falls --name angegeben
mkdir -p <project-name>
cd <project-name>
```

---

## Schritt 3: Git-Repository initialisieren

```bash
# Repository initialisieren
git init

# Auf develop Branch wechseln (Standard)
git checkout -b develop
```

Falls `--no-branching`: Stattdessen `git branch -M main`

---

## Schritt 4: Projektstruktur generieren

### Bei `--java`: Gradle Kotlin DSL Projekt

**WICHTIG: IMMER Gradle verwenden, NIEMALS Maven!**

Erstelle folgende Dateien:

**build.gradle.kts:**
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

**settings.gradle.kts:**
```kotlin
rootProject.name = "<project-name>"
```

**Verzeichnisstruktur:**
```
<project-name>/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle/wrapper/gradle-wrapper.properties
├── gradlew (executable)
├── gradlew.bat
├── src/main/java/com/example/App.java
├── src/main/resources/
├── src/test/java/com/example/AppTest.java
└── src/test/resources/
```

**gradle/wrapper/gradle-wrapper.properties:**
```properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.12-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

**.gitignore (Java/Gradle):**
```gitignore
# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar

# IDE
.idea/
*.iml
.vscode/

# OS
.DS_Store
```

### Bei `--uv`: Python Projekt

Verwende `uv init` falls verfügbar, sonst manuell:

```bash
uv init <project-name> || mkdir -p src/<package_name> tests
```

---

## Schritt 5: Community Standards erstellen

Erstelle diese Dateien in jedem Projekt:

- **LICENSE** (MIT als Standard)
- **README.md** (mit Badges und Struktur)
- **CONTRIBUTING.md** (Contribution Guidelines)
- **CODE_OF_CONDUCT.md** (Contributor Covenant 2.1)
- **SECURITY.md** (Security Policy)

---

## Schritt 6: GitHub Templates erstellen

Erstelle `.github/` Verzeichnis mit:

- **ISSUE_TEMPLATE/bug_report.yml**
- **ISSUE_TEMPLATE/feature_request.yml**
- **ISSUE_TEMPLATE/config.yml**
- **PULL_REQUEST_TEMPLATE.md**

---

## Schritt 7: Initialen Commit erstellen

**WICHTIG: Verwende IMMER den `/git-workflow:commit` Command!**

Rufe den Skill auf:
```
/git-workflow:commit
```

Der Commit-Skill wird:
1. Alle Dateien stagen
2. Pre-Commit-Checks durchführen
3. Einen professionellen Commit erstellen mit Emoji Conventional Commit Format

**NIEMALS direkt `git commit` verwenden!**

---

## Schritt 8: Main Branch erstellen

Nach dem initialen Commit auf develop:

```bash
# Main Branch von develop erstellen (synchron)
git branch main
```

---

## Schritt 9: Abschluss

Zeige dem User:

```
✓ Git-Repository initialisiert
✓ Branch 'develop' erstellt (aktiv)
✓ Projektstruktur generiert (<Projekttyp>)
✓ Community Standards erstellt
✓ GitHub Templates erstellt
✓ Initialer Commit erstellt (via /git-workflow:commit)
✓ Branch 'main' erstellt (synchron mit develop)

📁 Projekt bereit: <project-name>/
   Branch: develop (aktiv)

   Nächste Schritte:
   - Java: ./gradlew build
   - Python: uv venv && source .venv/bin/activate
```

---

## Zusammenfassung der wichtigsten Regeln

| Regel | Beschreibung |
|-------|--------------|
| **Gradle, nicht Maven** | Java-Projekte verwenden IMMER Gradle Kotlin DSL |
| **Commit via Skill** | Initialer Commit IMMER über `/git-workflow:commit` |
| **develop → main** | Standard-Branching-Strategie |
| **Java 21** | Aktuelle LTS-Version |
| **JUnit 5** | Standard Test-Framework |
