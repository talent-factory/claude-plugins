---
name: professional-init-project
description: Initializes open-source projects with GitHub best practices and git branching strategy. Use when setting up new repositories with standardized configuration.
---

# Professional Init-Project Workflow

This skill guides you through project initialization. **Follow these instructions step by step.**

## IMPORTANT RULES

1. **Java projects ALWAYS use Gradle Kotlin DSL** - NEVER Maven!
2. **Initial commit MUST be made via `/git-workflow:commit`** - NEVER use `git commit` directly!
3. **Git branching: develop -> main** is the default

---

## Step 1: Detect Project Type and Parameters

Analyze the user's arguments:

| Argument | Project Type | Build Tool |
|----------|-------------|------------|
| `--java` | Java | **Gradle Kotlin DSL** (NOT Maven!) |
| `--uv` | Python | uv |
| `--git` | Standard | - |
| `--node` | Node.js | npm/pnpm |

Optional arguments:
- `--name "xyz"`: Project name
- `--no-branching`: Only main, no develop

---

## Step 2: Create Project Directory

```bash
# If --name is specified
mkdir -p <project-name>
cd <project-name>
```

---

## Step 3: Initialize Git Repository

```bash
# Initialize repository
git init

# Switch to develop branch (default)
git checkout -b develop
```

If `--no-branching`: Use `git branch -M main` instead

---

## Step 4: Generate Project Structure

### For `--java`: Gradle Kotlin DSL Project

**IMPORTANT: ALWAYS use Gradle, NEVER Maven!**

Create the following files:

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

**Directory structure:**
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

### For `--uv`: Python Project

Use `uv init` if available, otherwise create manually:

```bash
uv init <project-name> || mkdir -p src/<package_name> tests
```

---

## Step 5: Create Community Standards

Create these files in every project:

- **LICENSE** (MIT as default)
- **README.md** (with badges and structure)
- **CONTRIBUTING.md** (Contribution Guidelines)
- **CODE_OF_CONDUCT.md** (Contributor Covenant 2.1)
- **SECURITY.md** (Security Policy)

---

## Step 6: Create GitHub Templates

Create `.github/` directory with:

- **ISSUE_TEMPLATE/bug_report.yml**
- **ISSUE_TEMPLATE/feature_request.yml**
- **ISSUE_TEMPLATE/config.yml**
- **PULL_REQUEST_TEMPLATE.md**

---

## Step 7: Create Initial Commit

**IMPORTANT: ALWAYS use the `/git-workflow:commit` command!**

Invoke the skill:
```
/git-workflow:commit
```

The commit skill will:
1. Stage all files
2. Run pre-commit checks
3. Create a professional commit with Emoji Conventional Commit format

**NEVER use `git commit` directly!**

---

## Step 8: Create Main Branch

After the initial commit on develop:

```bash
# Create main branch from develop (synchronized)
git branch main
```

---

## Step 9: Completion

Display to the user:

```
Git repository initialized
Branch 'develop' created (active)
Project structure generated (<project-type>)
Community standards created
GitHub templates created
Initial commit created (via /git-workflow:commit)
Branch 'main' created (synchronized with develop)

Project ready: <project-name>/
   Branch: develop (active)

   Next steps:
   - Java: ./gradlew build
   - Python: uv venv && source .venv/bin/activate
```

---

## Summary of Key Rules

| Rule | Description |
|------|-------------|
| **Gradle, not Maven** | Java projects ALWAYS use Gradle Kotlin DSL |
| **Commit via skill** | Initial commit ALWAYS via `/git-workflow:commit` |
| **develop -> main** | Default branching strategy |
| **Java 21** | Current LTS version |
| **JUnit 5** | Standard test framework |
