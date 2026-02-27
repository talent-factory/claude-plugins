# Education Plugin

Teaching aids, code explanations, and student support for IT education.

## Version 1.3.2

This plugin provides educational tools for students and instructors, including code explanations, a Java Tutor agent, and Markdown formatting skills.

---

## Commands

### `/education:explain-code`

Provide clear, educational explanations of code for students learning programming.

**Features:**

- Step-by-step code breakdown
- Concept explanations with examples
- Visual flow diagrams
- Practice exercises
- Adaptable to student level (beginner/intermediate/advanced)

**Usage:**

```
/education:explain-code
```

Claude will ask about the student's level and provide tailored explanations.

## Agents

### Java Tutor

Expert Java programming instructor specializing in teaching students.

**Specialties:**

- Java fundamentals and OOP
- Data structures and algorithms
- Best practices and clean code
- Common mistake prevention
- Exam preparation

**Activation:**
Use `/agents` and select "Java Tutor" for Java-specific teaching support.

### Markdown Syntax Formatter

Expert Markdown formatting specialist with comprehensive knowledge of CommonMark and GitHub Flavored Markdown specifications.

**Capabilities:**

- Convert visual formatting cues into proper Markdown syntax
- Correct heading hierarchies ensuring logical progression
- Format lists with consistent markers and proper indentation
- Handle code blocks with appropriate language identifiers
- Apply Swiss orthography rules for German text
- Handle linter exceptions for training materials

**Activation:**

- **Automatic:** Triggered when formatting or reviewing Markdown documents
- **Manual:** Use Task tool with `subagent_type: "education:markdown-syntax-formatter"`

## Skills

### Markdown Syntax Formatter

Converts text with visual formatting into proper Markdown syntax, fixes formatting issues,
and ensures consistent document structure.

**Capabilities:**

- Fix heading hierarchies and document structure
- Convert visual formatting cues to proper Markdown syntax
- Apply Swiss German orthography to German-language documents
- Handle linter exceptions for training materials and templates

**Activation:**

The skill activates automatically when formatting or reviewing Markdown files,
or invoke it manually:

```
/education:markdown-syntax-formatter
```

## Who This Is For

- **Students**: Learning programming at universities and educational institutions
- **Instructors**: Teaching programming courses
- **Self-learners**: Studying programming independently
- **Code reviewers**: Providing educational feedback

## Teaching Approach

This plugin follows evidence-based teaching principles:

1. **Progressive Disclosure**: Start simple, add complexity gradually
2. **Active Learning**: Encourage experimentation and practice
3. **Conceptual Understanding**: Focus on "why" not just "how"
4. **Real-World Context**: Connect concepts to practical applications

## Examples

### Explaining Simple Code

```
/education:explain-code

Student: Can you explain this loop?
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

Claude: [Provides detailed explanation with analogies and practice exercises]
```

### Using Java Tutor Agent

```
/agents
> Select: Java Tutor

Student: I'm confused about inheritance
Java Tutor: [Provides step-by-step explanation with family tree analogy]
```

## Supported Languages

While the plugin works with any programming language, it has specialized support for:

- **Java** (primary focus for computer science courses)
- **Python** (data structures, algorithms)
- **JavaScript** (web development)
- **C/C++** (systems programming)

## Best Practices for Instructors

1. Use `/education:explain-code` to generate teaching materials
2. Activate Java Tutor for consistent Java teaching
3. Encourage students to ask questions
4. Use generated exercises for practice
5. Review explanations before sharing with students

## Curriculum Integration

This plugin is designed to complement computer science curricula:

- Aligned with standard CS programs
- References course materials appropriately
- Prepares students for exams
- Connects to other CS concepts

---

## Installation

```json
{
  "enabledPlugins": {
    "education@talent-factory": true
  }
}
```

---

## Changelog

### Version 1.3.2 (2026-02-27)

- Added `keywords` and `license` fields to plugin.json
- Improved agent descriptions with when-to-use context
- Translated documentation to English

---

## Related Plugins

- **[Code Quality](../code-quality/README.md)** - Python and Frontend expert agents
- **[Development](../development/README.md)** - Java developer agent
- **[Core Utilities](../core/README.md)** - Plugin development and validation

---

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) for details.

---

**Made with care by Talent Factory GmbH**
