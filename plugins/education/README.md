# Education Plugin

## Version 5.0.0

Two skills for teaching and course material: Markdown clean-up with Swiss German orthography, and Markdown to PDF.

## Skills

### markdown-syntax-formatter

Fixes heading hierarchies, lists, code blocks and emphasis, converts visual cues into Markdown, applies Swiss German orthography (`ss` instead of `ß`, real umlauts) to German text, and respects the project's markdownlint configuration (including the documented MD024 exception for training material). Activates when you format or review Markdown, or invoke `/education:markdown-syntax-formatter`. Rules: [Swiss German conventions](skills/markdown-syntax-formatter/swiss-german-conventions.md), [linter exceptions](skills/markdown-syntax-formatter/linter-exceptions.md).

### md-to-pdf

Converts Markdown into a PDF or a ConTeXt source (`.tex`) with a freely configurable header and footer.

**Capabilities:**

- Engine ConTeXt (default) or XeLaTeX
- Configurable header and footer, font, margins, and page size via CLI or a `md-to-pdf.toml` in the repository
- Automatic rendering of Mermaid diagrams (requires `npx` and `@mermaid-js/mermaid-cli`)

**Requirements:** `pandoc`, Python 3.11+, and the chosen engine (`context` or `xelatex`) on the `PATH`

**Activation:**

- Automatic: "als PDF", "PDF erstellen", "md to pdf", "ConTeXt"
- Manual: `/education:md-to-pdf`

**Direct invocation:**

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/md-to-pdf/scripts/md_to_pdf.py QUELLE.md ZIEL.pdf \
  --header-left "Module · Block 05 · Worksheet" --header-right "Binary search trees"
```

## Installation

```json
{
  "extraKnownMarketplaces": {
    "talent-factory": {
      "source": { "source": "github", "repo": "talent-factory/claude-plugins" }
    }
  },
  "enabledPlugins": { "education@talent-factory": true }
}
```

## Changelog

### Version 5.0.0 (2026-11-14)

**Breaking:**

- Removed the command and skill `explain-code`, the agent `java-tutor` and the agent `markdown-syntax-formatter`. They described tutoring and explaining code, which a current model does without instructions; the formatter agent duplicated the skill of the same name.
- `markdown-syntax-formatter` skill cut from 207 to about 30 lines (the two reference files stay). Invoke it as a skill (`/education:markdown-syntax-formatter`), not as an agent.
- The plugin shrank from about 2.5k to about 1.4k lines; most of what remains is the tested `md-to-pdf` engine.

### Version 4.0.0 (2026-11-14)

**Breaking:** the command-line options, `md-to-pdf.toml` keys and `[these]` fields of `md-to-pdf` are renamed to English, in line with the repository language policy. The old names are rejected, there are no aliases. Migration:

| Before | After |
|---|---|
| `--profil`, `profil` | `--profile`, `profile` |
| `--kopf-links`, `--kopf-rechts` / `kopf_links`, `kopf_rechts` | `--header-left`, `--header-right` / `header_left`, `header_right` |
| `--fuss-links`, `--fuss-rechts` / `fuss_links`, `fuss_rechts` | `--footer-left`, `--footer-right` / `footer_left`, `footer_right` |
| `--schrift`, `--groesse`, `--rand` / `schrift`, `groesse`, `rand` | `--font`, `--font-size`, `--margin` / `font`, `font_size`, `margin` |
| `--fallback-zeichen` / `fallback_zeichen` | `--fallback-chars` / `fallback_chars` |
| `--mermaid-breite` / `mermaid_breite` | `--mermaid-width` / `mermaid_width` |
| `[these]` | `[thesis]` |
| `titel`, `untertitel`, `dokumenttyp`, `studiengang` | `title`, `subtitle`, `document_type`, `program` |
| `autor`, `referent_rolle`, `referent`, `eingereicht_bei` | `author`, `supervisor_role`, `supervisor`, `submitted_to` |
| `wohnort`, `datum`, `widmung`, `titelbild` | `residence`, `date`, `dedication`, `title_image` |
| `institution`, `logo` | unchanged |

### Version 3.0.0 (2026-11-14)

**Breaking:** the `md-to-pdf` profile `ffhs-thesis` is now the generic profile `thesis`. The FFHS-specific part (institution name, logo, preset) moved to the private marketplace. Title page data accepts a new optional field `institution`; the ConTeXt macros `\ffhsVorspann` and `\ffhsVerzeichnisse` are renamed to `\thesisVorspann` and `\thesisVerzeichnisse`. Existing `md-to-pdf.toml` files must change `profil = "ffhs-thesis"` to `profil = "thesis"` and add `institution` if the institution name should appear.

### Version 2.0.0 (2026-11-14)

**Breaking:** the `ffhs-lecture-slides` skill was removed from this public marketplace. FFHS branding and course material now live in a private marketplace. The `md-to-pdf` skill and its `ffhs-thesis` profile are unchanged.

### Version 1.8.2 (2026-11-14)

- `ffhs-lecture-slides`: table header gradient now spans the whole header row instead of restarting in every cell
- `md-to-pdf`: fixed invalid YAML in the SKILL.md frontmatter (`description` is now a block scalar)

### Version 1.8.1 (2026-11-08)

- `md-to-pdf`: SKILL.md prose translated to English (profile `ffhs-thesis`, code blocks, listings, table captions, pitfalls)

### Version 1.8.0 (2026-10-12)

- `md-to-pdf`: Codeblöcke als umbrechbare Tabelle mit grauem Hintergrund, Listings `Listing N: Titel` aus dem Info-String, Tabellen-Captions `Tabelle N: Titel` (`: Titel` oder `: Table: Titel`), Abstände um Codeblöcke

### Version 1.7.0 (2026-10-12)

- Added `ffhs-thesis` profile to `md-to-pdf` (ConTeXt): FFHS thesis layout, title page from `[these]` in `md-to-pdf.toml`, roman front matter and arabic main text, table of contents and optional list of figures and tables
- `md-to-pdf` validates `[these]` (types, required fields, image names) and derives line spacing from `groesse`
- Unit and end-to-end tests in `scripts/test_md_to_pdf.py`

### Version 1.6.0 (2026-10-12)

- Added `md-to-pdf` skill for Markdown-to-PDF and ConTeXt conversion with configurable header/footer and Mermaid rendering

### Version 1.5.0 (2026-05-08)

- Added `explain-code` skill for natural-language code explanation activation

### Version 1.4.0 (2026-03-28)

- Added FFHS Lecture Slides skill for reveal.js and PowerPoint presentation generation
- Added FFHS, presentations, and slides keywords

### Version 1.3.3 (2026-02-27)

- Added `keywords` and `license` fields to plugin.json
- Improved agent descriptions with when-to-use context
- Translated documentation to English

---

## Related Plugins

- **[Code Quality](https://talent-factory.github.io/claude-plugins/plugins/code-quality/)** - Python and Frontend expert agents
- **[Development](https://talent-factory.github.io/claude-plugins/plugins/development/)** - Java developer agent
- **[Core Utilities](https://talent-factory.github.io/claude-plugins/plugins/core/)** - Plugin development and validation

---

## License

MIT License - see [LICENSE](https://github.com/talent-factory/claude-plugins/blob/main/LICENSE) for details.

---

**Made with care by Talent Factory GmbH**
