#!/usr/bin/env python3
"""Java/Gradle project generator with Kotlin DSL."""

import subprocess
from pathlib import Path


class JavaGradleGenerator:
    """Generates Java project with Gradle Kotlin DSL."""

    def __init__(
        self,
        project_path: Path,
        project_name: str,
        package_name: str = "com.example",
        java_version: int = 21,
        gradle_version: str = "8.12",
    ):
        self.project_path = project_path
        self.project_name = project_name
        self.package_name = package_name
        self.java_version = java_version
        self.gradle_version = gradle_version
        self.package_path = package_name.replace(".", "/")

    def generate_all(self) -> bool:
        """Generate all Java/Gradle files.

        Returns:
            True if successful, False otherwise.
        """
        try:
            self._create_directories()
            self._generate_build_gradle()
            self._generate_settings_gradle()
            self._generate_gitignore()
            self._generate_app_java()
            self._generate_app_test()
            self._setup_gradle_wrapper()
            print("✓ Projektstruktur generiert (Java/Gradle)")
            return True
        except Exception as e:
            print(f"❌ Failed to generate Java project: {e}")
            return False

    def _create_directories(self) -> None:
        """Create project directory structure."""
        dirs = [
            f"src/main/java/{self.package_path}",
            "src/main/resources",
            f"src/test/java/{self.package_path}",
            "src/test/resources",
            "gradle/wrapper",
        ]
        for dir_path in dirs:
            (self.project_path / dir_path).mkdir(parents=True, exist_ok=True)

    def _generate_build_gradle(self) -> None:
        """Generate build.gradle.kts file."""
        content = f"""plugins {{
    java
    application
}}

group = "{self.package_name}"
version = "0.1.0"

java {{
    toolchain {{
        languageVersion = JavaLanguageVersion.of({self.java_version})
    }}
}}

repositories {{
    mavenCentral()
}}

dependencies {{
    // Testing
    testImplementation(platform("org.junit:junit-bom:5.11.4"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}}

application {{
    mainClass = "{self.package_name}.App"
}}

tasks.test {{
    useJUnitPlatform()
    testLogging {{
        events("passed", "skipped", "failed")
    }}
}}

tasks.jar {{
    manifest {{
        attributes(
            "Main-Class" to "{self.package_name}.App",
            "Implementation-Version" to project.version
        )
    }}
}}
"""
        (self.project_path / "build.gradle.kts").write_text(content)

    def _generate_settings_gradle(self) -> None:
        """Generate settings.gradle.kts file."""
        content = f"""rootProject.name = "{self.project_name}"
"""
        (self.project_path / "settings.gradle.kts").write_text(content)

    def _generate_gitignore(self) -> None:
        """Generate .gitignore for Java/Gradle."""
        content = """# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar
!**/src/main/**/build/
!**/src/test/**/build/

# IDE
.idea/
*.iml
*.ipr
*.iws
.vscode/
*.swp
.project
.classpath
.settings/

# OS
.DS_Store
Thumbs.db

# Runtime
*.log
logs/

# Local configuration
local.properties
"""
        (self.project_path / ".gitignore").write_text(content)

    def _generate_app_java(self) -> None:
        """Generate main App.java file."""
        content = f"""package {self.package_name};

/**
 * Main application class.
 */
public class App {{

    /**
     * Returns a greeting message.
     *
     * @return the greeting message
     */
    public String getGreeting() {{
        return "Hello, World!";
    }}

    /**
     * Main entry point.
     *
     * @param args command line arguments
     */
    public static void main(String[] args) {{
        System.out.println(new App().getGreeting());
    }}
}}
"""
        java_path = self.project_path / f"src/main/java/{self.package_path}/App.java"
        java_path.write_text(content)

    def _generate_app_test(self) -> None:
        """Generate AppTest.java file."""
        content = f"""package {self.package_name};

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for App.
 */
class AppTest {{

    @Test
    void appHasAGreeting() {{
        App app = new App();
        assertNotNull(app.getGreeting(), "app should have a greeting");
    }}

    @Test
    void greetingContainsHello() {{
        App app = new App();
        assertTrue(app.getGreeting().contains("Hello"), "greeting should contain 'Hello'");
    }}
}}
"""
        test_path = self.project_path / f"src/test/java/{self.package_path}/AppTest.java"
        test_path.write_text(content)

    def _setup_gradle_wrapper(self) -> None:
        """Setup Gradle wrapper."""
        # Try to use gradle command if available
        try:
            result = subprocess.run(
                ["gradle", "wrapper", f"--gradle-version={self.gradle_version}"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return
        except FileNotFoundError:
            pass

        # Fallback: create minimal wrapper files
        self._create_wrapper_properties()
        self._create_wrapper_scripts()

    def _create_wrapper_properties(self) -> None:
        """Create gradle-wrapper.properties file."""
        content = f"""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-{self.gradle_version}-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
"""
        props_path = self.project_path / "gradle/wrapper/gradle-wrapper.properties"
        props_path.write_text(content)

    def _create_wrapper_scripts(self) -> None:
        """Create gradlew and gradlew.bat scripts."""
        # Unix script (simplified)
        gradlew = """#!/bin/sh
# Gradle wrapper script - download wrapper jar if missing
GRADLE_WRAPPER_JAR="gradle/wrapper/gradle-wrapper.jar"

if [ ! -f "$GRADLE_WRAPPER_JAR" ]; then
    echo "Downloading Gradle wrapper..."
    mkdir -p gradle/wrapper
    curl -sL "https://raw.githubusercontent.com/gradle/gradle/master/gradle/wrapper/gradle-wrapper.jar" -o "$GRADLE_WRAPPER_JAR"
fi

exec java -jar "$GRADLE_WRAPPER_JAR" "$@"
"""
        gradlew_path = self.project_path / "gradlew"
        gradlew_path.write_text(gradlew)
        gradlew_path.chmod(0o755)

        # Windows script (simplified)
        gradlew_bat = """@echo off
set GRADLE_WRAPPER_JAR=gradle\\wrapper\\gradle-wrapper.jar

if not exist "%GRADLE_WRAPPER_JAR%" (
    echo Downloading Gradle wrapper...
    mkdir gradle\\wrapper 2>nul
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/gradle/gradle/master/gradle/wrapper/gradle-wrapper.jar' -OutFile '%GRADLE_WRAPPER_JAR%'"
)

java -jar "%GRADLE_WRAPPER_JAR%" %*
"""
        (self.project_path / "gradlew.bat").write_text(gradlew_bat)
