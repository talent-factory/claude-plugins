# Education Plugin

Teaching aids, code explanations, and student support for IT education.

## Version 1.2.0

This plugin provides educational tools for students and instructors, including code explanations, a Java Tutor agent, and Markdown formatting skills.

---

## Commands

### `/explain-code`
Provide clear, educational explanations of code for students learning programming.

**Features:**

- Step-by-step code breakdown
- Concept explanations with examples
- Visual flow diagrams
- Practice exercises
- Adaptable to student level (beginner/intermediate/advanced)

**Usage:**
```
/explain-code
```

Claude will ask about the student's level and provide tailored explanations.

## Agents

See [Skills & Agents Activation Guide](../reference/skills-agents-activation.md) for detailed activation instructions.

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

## Skills

See [Skills & Agents Activation Guide](../reference/skills-agents-activation.md) for detailed activation instructions.

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
/markdown-syntax-formatter
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
/explain-code

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

1. Use `/explain-code` to generate teaching materials
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

## Related Plugins

- **[Code Quality](code-quality.md)** - Python and Frontend expert agents
- **[Development](development.md)** - Java developer agent
- **[Core Utilities](core.md)** - Plugin development and validation

---

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) for details.

---

**Made with care by Talent Factory GmbH**
