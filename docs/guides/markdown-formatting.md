# Formatting Markdown with `markdown-syntax-formatter`

Learn how to produce clean, consistent Markdown documents using the education plugin's
Markdown formatting skill.

**Level**: Beginner
**Plugin**: education

---

## What You'll Learn

- How to invoke the Markdown syntax formatter skill
- Fixing common Markdown structure issues (headings, lists, code blocks)
- Applying Swiss German orthography to German-language documents
- Handling linter exceptions in training materials and templates
- Best practices for professional Markdown documentation

---

## Prerequisites

- Education plugin installed and enabled
- A Markdown file (`.md`) in your project or working directory

---

## Why Markdown Quality Matters

As a BSc student, you write Markdown constantly: README files, lab reports, project
documentation, pull request descriptions, and wiki pages. Poorly formatted Markdown
leads to:

- Broken rendering on GitHub, GitLab, or MkDocs
- Inconsistent heading hierarchies that confuse readers
- Mixed list styles that look unprofessional
- Code blocks without syntax highlighting

The `markdown-syntax-formatter` skill helps you catch and fix these issues automatically.

---

## Step 1: Invoke the Skill

The skill activates in two ways:

=== "Automatic"

    Simply ask Claude to format or review a Markdown file:

    ```
    Can you check the formatting of my README.md?
    ```

    ```
    Please fix the Markdown structure in docs/setup-guide.md
    ```

    Claude recognizes the intent and loads the skill automatically.

=== "Manual"

    Invoke the skill explicitly:

    ```
    /markdown-syntax-formatter
    ```

    Then provide the file or text you want formatted.

---

## Step 2: Understanding What Gets Fixed

The skill checks and repairs several categories of issues.

### Heading Hierarchy

One of the most common mistakes in student documentation: skipping heading levels.

**Before** (broken hierarchy):

```markdown
# My Project

### Installation (skipped h2!)

##### Usage (skipped h3, h4!)
```

**After** (correct hierarchy):

```markdown
# My Project

## Installation

### Usage
```

!!! warning "Why this matters"
    Screen readers, table-of-contents generators, and documentation tools rely on
    heading levels to build navigation. Skipping levels breaks accessibility and
    structure.

---

### List Formatting

Mixed list markers and inconsistent indentation are common in collaborative documents.

**Before** (inconsistent):

```markdown
* First item
- Second item
  + Nested item
  * Another nested
1) Numbered item
2. Another numbered
```

**After** (consistent):

```markdown
- First item
- Second item
  - Nested item
  - Another nested
1. Numbered item
1. Another numbered
```

!!! tip "Ordered list numbering"
    Using `1.` for all ordered list items is intentional. Markdown renderers
    auto-number them, and this avoids manual renumbering when you insert items.

---

### Code Blocks

Indented code blocks and missing language identifiers reduce readability.

**Before** (no language identifier):

````
```
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```
````

**After** (with language identifier):

````
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```
````

The language identifier (`java`, `python`, `bash`, etc.) enables syntax highlighting,
which significantly improves readability for code reviewers and fellow students.

---

### Emphasis and Formatting

**Before** (mixed styles):

```markdown
This is __bold__ and this is _italic_ and this is **also bold**.
```

**After** (consistent):

```markdown
This is **bold** and this is *italic* and this is **also bold**.
```

The skill uses asterisks consistently: `**bold**` and `*italic*`. This avoids ambiguity
with filenames containing underscores (e.g., `my_module`).

---

## Step 3: German-Language Documents

If your document is in German, the skill automatically applies Swiss German orthography.

### Eszett Replacement

The Eszett (ß) is not used in Swiss German. The skill replaces it with "ss":

| Input | Output |
|-------|--------|
| Straße | Strasse |
| großes Projekt | grosses Projekt |
| schließlich | schliesslich |
| Fußnote | Fussnote |

### Umlaut Correction

Digraph substitutions (ae, oe, ue) are corrected to proper umlauts:

| Input | Output |
|-------|--------|
| Aenderung | Änderung |
| Uebersicht | Übersicht |
| oeffnen | öffnen |

!!! note "Code is never modified"
    Swiss German rules apply only to prose text. Code blocks, inline code, URLs, and
    technical identifiers remain unchanged.

---

## Step 4: Handling Linter Exceptions

Not every linter warning needs fixing. The skill recognizes legitimate exceptions.

### Duplicate Headings in Training Materials

In a lab exercise document, repeating headings like "Exercise" and "Solution" per chapter
is expected:

````markdown
## Chapter 1: Variables

### Exercise

Write a program that declares three variables...

### Solution

```java
int x = 10;
```

## Chapter 2: Loops

### Exercise

Write a program that prints numbers 1-10...

### Solution

```java
for (int i = 1; i <= 10; i++) { ... }
```
````

The skill recognizes this as training material and does **not** rename the headings.

For regular documents, it suggests more specific headings instead:

```markdown
## Setup -- Development Environment
## Setup -- Production Server
```

---

## Practical Examples

### Example 1: Cleaning Up a Project README

A typical BSc project README with common issues:

**Before:**

````markdown
# semester project 2024

### team members
- Alice Mueller
- Bob Schmidt

### how to run
First install dependencies
```
npm install
```
Then start the server
```
npm start
```

##### technologies used
We used React and Node.js
````

**After:**

````markdown
# Semester Project 2024

## Team Members

- Alice Mueller
- Bob Schmidt

## How to Run

First install dependencies:

```bash
npm install
```

Then start the server:

```bash
npm start
```

## Technologies Used

We used React and Node.js.
````

**What changed:**

1. Title capitalized properly
2. Heading hierarchy fixed (h3 → h2, h5 → h2)
3. Blank lines added around code blocks
4. Language identifiers added (`bash`)
5. Punctuation added to final sentence

---

### Example 2: Formatting a Lab Report

**Before:**

```
EXPERIMENT 3: SORTING ALGORITHMS

OBJECTIVE
Compare the performance of different sorting algorithms.

METHODOLOGY
We tested the following algorithms:
* Bubble Sort
- Quick Sort
* Merge Sort

RESULTS
The results show that Quick Sort is the FASTEST algorithm
for large datasets.

CODE
public void bubbleSort(int[] arr) {
    // implementation
}
```

**After:**

````markdown
# Experiment 3: Sorting Algorithms

## Objective

Compare the performance of different sorting algorithms.

## Methodology

We tested the following algorithms:

- Bubble Sort
- Quick Sort
- Merge Sort

## Results

The results show that Quick Sort is the **fastest** algorithm
for large datasets.

## Code

```java
public void bubbleSort(int[] arr) {
    // implementation
}
```
````

**What changed:**

1. ALL CAPS headings converted to proper Markdown headings
2. Heading hierarchy established (h1 for title, h2 for sections)
3. Mixed list markers (`*`, `-`) unified to `-`
4. "FASTEST" converted to `**fastest**` (bold emphasis)
5. Code wrapped in fenced block with `java` language identifier

---

## Common Mistakes to Avoid

| Mistake | Problem | Fix |
|---------|---------|-----|
| No blank line before heading | Heading may not render | Always add a blank line before `##` |
| Indented code without fence | Fragile, no syntax highlighting | Use triple backticks with language |
| Skipping heading levels | Breaks document outline | Follow h1 → h2 → h3 sequence |
| Mixing `*` and `-` in lists | Inconsistent rendering | Pick one marker and use it throughout |
| Using `_emphasis_` in code docs | Conflicts with `snake_case` | Use `*emphasis*` instead |
| German text with ß | Incorrect for Swiss German | Skill auto-converts to "ss" |

---

## What's Next?

- **[Your First Commit](first-commit.md)** -- Commit your formatted documentation
  professionally
- **[Create Your First PR](create-first-pr.md)** -- Submit your documentation in a pull
  request
- **[Skill Format Reference](../reference/skill-format.md)** -- Learn how the skill is
  built (for plugin developers)

---

## Summary

The `markdown-syntax-formatter` skill helps you write professional Markdown by:

1. Fixing structural issues (headings, lists, code blocks, emphasis)
2. Applying Swiss German orthography to German documents
3. Respecting legitimate linter exceptions in training materials
4. Providing consistent formatting across all your documentation

Use it whenever you write or review Markdown files -- it activates automatically when you
ask Claude to format or check a document.
