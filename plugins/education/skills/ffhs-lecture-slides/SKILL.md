---
name: ffhs-lecture-slides
description: Create lecture presentations for FFHS in reveal.js (default) or PowerPoint format. Use when user requests presentations for PVA sessions, lecture slides, or teaching materials. Supports both web-based reveal.js and traditional PPTX output.
---

# FFHS Lecture Slides

Create lecture presentations for FFHS (Fernfachhochschule Schweiz) in two formats:

1. **reveal.js** (Default) - Web-based HTML presentations
2. **PowerPoint** - Traditional PPTX files with FFHS branding

## When to Use

Use this skill when:

- User requests a presentation for PVA (Präsenzveranstaltung) sessions
- Creating lecture slides for the Java Fundamentals (JaF) course
- User asks for teaching materials in FFHS style
- User mentions "reveal.js", "slides", or "presentation"

## Output Formats

| Format | File Type | Output Directory | Advantages |
|--------|-----------|------------------|------------|
| **reveal.js** | HTML/Markdown | `docs/slides/` | Web-based, Mermaid support, code highlighting |
| **PowerPoint** | PPTX | `docs/slides/` | Offline, FFHS template, easy sharing |

---

## Format 1: reveal.js (Default)

### File Structure

```
docs/slides/
├── pva-01/
│   ├── index.html      # Main presentation
│   └── slides.md       # Markdown content (optional)
├── pva-02/
│   └── index.html
└── assets/
    ├── ffhs-theme.css  # FFHS styling
    └── ffhs-logo.svg   # Logo
```

### HTML Template

Create a reveal.js presentation using this template:

```html
<!doctype html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PVA 1 - Grundlagen und Strukturen</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reset.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/styles/github.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        /* FFHS Corporate Design - Red/Violet */
        :root {
            --ffhs-red: #d50006;
            --ffhs-red-light: #e63946;
            --ffhs-violet: #51247a;
            --ffhs-violet-light: #9b59b6;
            --ffhs-violet-transparent: rgba(81, 36, 122, 0.1);
            --ffhs-text: #181716;
            --ffhs-gray: #666666;
            --ffhs-light-gray: #f5f5f5;
        }
        .reveal h1, .reveal h2 { color: var(--ffhs-red); font-weight: 600; }
        .reveal h3 { color: var(--ffhs-violet); font-weight: 600; }
        .reveal { font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif; color: var(--ffhs-text); }
        .reveal .slides section { text-align: left; }
        .reveal pre { border-left: 3px solid var(--ffhs-red); background: var(--ffhs-light-gray); border-radius: 4px; }
        .reveal pre code { font-family: 'JetBrains Mono', monospace; font-size: 0.8em; background: var(--ffhs-light-gray) !important; }
        .reveal pre code tr, .reveal pre code .hljs-ln-line { background: transparent !important; }
        .reveal ul { margin-left: 1em; }
        .reveal a { color: var(--ffhs-violet); }
        .reveal a:hover { color: var(--ffhs-red); }
        .reveal blockquote { background: var(--ffhs-violet-transparent); border-left: 4px solid var(--ffhs-violet); }
        .reveal table th { background: linear-gradient(90deg, var(--ffhs-red) 0%, var(--ffhs-violet) 100%); color: white; }
        .reveal .title-slide h1 { font-size: 2.5em; text-align: center; }
        .reveal .title-slide h2 { color: var(--ffhs-violet); text-align: center; }
        .reveal .title-slide p { text-align: center; color: var(--ffhs-gray); }
        .ffhs-footer {
            position: absolute; bottom: 1em; left: 1em;
            font-size: 0.5em; color: var(--ffhs-gray);
        }
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
            <!-- Title slide -->
            <section class="title-slide">
                <h1>PVA 1</h1>
                <h2>Grundlagen und Strukturen</h2>
                <p>Java Fundamentals (JaF) - FFHS</p>
            </section>

            <!-- Learning objectives -->
            <section>
                <h2>Lernziele</h2>
                <ul>
                    <li>Von-Neumann-Architektur erklären</li>
                    <li>Java-Entwicklungsumgebung aufsetzen</li>
                    <li>Erstes Java-Programm schreiben</li>
                    <li>Klassen und Objekte verstehen</li>
                </ul>
            </section>

            <!-- Code example -->
            <section>
                <h2>Erstes Java-Programm</h2>
                <pre><code class="language-java" data-trim>
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, FFHS!");
    }
}
                </code></pre>
            </section>

            <!-- Mermaid diagram -->
            <section>
                <h2>UML-Klassendiagramm</h2>
                <div class="mermaid">
classDiagram
    class Hund {
        int groesse
        String name
        bellen()
    }
                </div>
            </section>
        </div>
        <div class="ffhs-footer">FFHS - Java Fundamentals</div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/highlight.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/markdown/markdown.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({ startOnLoad: true, theme: 'default' });
        Reveal.initialize({
            hash: true,
            slideNumber: true,
            plugins: [ RevealHighlight, RevealMarkdown ]
        });
    </script>
</body>
</html>
```

### Slide Types

| Type | HTML Structure |
|------|---------------|
| **Title** | `<section class="title-slide"><h1>...</h1></section>` |
| **Content** | `<section><h2>Title</h2><ul>...</ul></section>` |
| **Code** | `<section><h2>...</h2><pre><code>...</code></pre></section>` |
| **Diagram** | `<section><h2>...</h2><div class="mermaid">...</div></section>` |
| **Image** | `<section><h2>...</h2><img src="..."></section>` |
| **Two Columns** | `<section><div style="display:flex">...</div></section>` |

### Vertical Slides (Sub-slides)

```html
<section>
    <section><h2>Main slide</h2></section>
    <section><h3>Sub-slide 1</h3></section>
    <section><h3>Sub-slide 2</h3></section>
</section>
```

### Presenter Mode

Press `S` to open speaker notes:

```html
<section>
    <h2>Slide Title</h2>
    <aside class="notes">
        Notes for the instructor, not visible to students.
    </aside>
</section>
```

---

## Format 2: PowerPoint (PPTX)

### Template

The FFHS template is located at `assets/ffhs-template.pptx` (relative to this skill directory). When installed as a plugin, the resolved path is `${CLAUDE_PLUGIN_ROOT}/skills/ffhs-lecture-slides/assets/ffhs-template.pptx`.

### Available Layouts

| Index | Layout | Usage |
|-------|--------|-------|
| 0 | FFHS Titelfolie_einfach 4:3 | Title slide |
| 1 | FFHS Titel und Inhalt 4:3 | Standard content |
| 2 | FFHS Nummerierung 4:3 | Numbered list |
| 4 | FFHS Zwei Inhalte 4:3 | Two columns |
| 5 | FFHS Drei Inhalte 4:3 | Three columns |
| 6 | FFHS Vergleich 4:3 | Comparison slide |
| 9 | FFHS Bild mit Überschrift 4:3 | Image with title |
| 10 | FFHS Abschlussfolie 4:3 | Closing slide |

### Python Script for PPTX Generation

```python
from pathlib import Path
from pptx import Presentation

# Load template (adjust path to your project layout)
template_path = 'assets/ffhs-template.pptx'
prs = Presentation(template_path)

# Remove example slides
while len(prs.slides) > 0:
    rId = prs.slides._sldIdLst[0].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[0]

# Title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "PVA 1 - Grundlagen"

# Content slide
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "Lernziele"
for shape in slide.shapes:
    if shape.has_text_frame and shape != slide.shapes.title:
        tf = shape.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.text = "Von-Neumann-Architektur erklären"
        p = tf.add_paragraph()
        p.text = "Java-Programm schreiben"
        break

# Save
Path('docs/slides').mkdir(parents=True, exist_ok=True)
prs.save('docs/slides/pva-01-grundlagen.pptx')
```

---

## PVA Content Outlines

### PVA 1 - Foundations and Structures

Slide structure:

1. Title slide: "PVA 1 - Grundlagen und Strukturen"
2. Agenda / Learning objectives
3. Von Neumann architecture (diagram)
4. Development environment
5. First Java program (code)
6. Variables and data types
7. Control structures (if/else)
8. Loops (for/while)
9. Classes and objects
10. UML class diagram
11. Exercise / Summary

### PVA 2 - Inheritance and Polymorphism

Slide structure:

1. Title slide: "PVA 2 - Vererbung und Polymorphie"
2. Agenda / Learning objectives
3. Review: Classes
4. Introduction to inheritance (UML)
5. `extends` keyword
6. Method overriding (@Override)
7. Abstract classes
8. Polymorphism explained
9. IS-A vs HAS-A
10. Shapes example (code + UML)
11. Exercise / Summary

---

## Quick Start

### Create reveal.js presentation (recommended)

```bash
mkdir -p docs/slides/pva-01
# Then create index.html using the template above
```

### Create PowerPoint presentation

```bash
pip install python-pptx
python scripts/create_pva_slides.py
```

### View presentation (reveal.js)

```bash
# Using Python server
cd docs/slides/pva-01
python -m http.server 8000
# Open http://localhost:8000
```

---

## Keyboard Shortcuts (reveal.js)

| Key | Function |
|-----|----------|
| `→` / `↓` | Next slide |
| `←` / `↑` | Previous slide |
| `Esc` / `O` | Overview |
| `S` | Speaker notes |
| `F` | Fullscreen |
| `B` | Black screen |
| `?` | Help |
