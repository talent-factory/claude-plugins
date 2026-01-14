# Handoff Beispiele

## Beispiel 1: Minimal (Bug-Fix)

```markdown
# Handoff: RBAC Regression Fix

**Datum**: 2026-01-14 15:30
**Branch**: feature/TF-177-rbac-regression-exam-creation
**Linear Issue**: TF-177 - RAG Exam Creator Premium Feature Bug

## Original-Aufgabe

RAG Exam Creator zeigt "Premium Feature" Upgrade-Prompt trotz Full Deployment Mode.

## Bereits erledigt

- `.env.example` angepasst (DEPLOYMENT_MODE Variablen dokumentiert)
- `packages/core/backend/main.py` untersucht (RBAC-Logik identifiziert)
- Frontend Component-Loading analysiert

## Aktueller Zustand

**Modified Files** (uncommitted):
- `.env.example` - Neue Variablen dokumentiert
- `packages/core/backend/main.py` - Debug-Logging hinzugefügt

## Nächste Schritte

1. **RBAC-Logik prüfen**: `packages/core/backend/main.py:712`
2. **Frontend Premium Loading testen**: `packages/core/frontend/src/pages/Exams.tsx:45`
3. **Integration Test schreiben**: Neuer Test für RBAC + Deployment Mode

## Für den nächsten Agent

Backend scheint korrekt konfiguriert. Problem liegt wahrscheinlich im Frontend Component Loading. Prüfe `Exams.tsx` auf Premium-Import-Logik und wie `deploymentMode` aus dem Context gelesen wird.
```

## Beispiel 2: Vollständig (Feature-Entwicklung)

```markdown
# Handoff: Dark Mode Implementation

**Datum**: 2026-01-14 18:45
**Branch**: feature/dark-mode-toggle
**Linear Issue**: TF-234 - Dark Mode für Settings Page

## Original-Aufgabe

Implementiere einen Dark Mode Toggle in den Anwendungseinstellungen. Der Modus soll persistent gespeichert werden und alle Komponenten betreffen.

**Warum wichtig**: Nutzer-Feedback zeigt hohe Nachfrage (47% der Support-Tickets erwähnen Augenbelastung bei Nachtnutzung).

## Bereits erledigt

### Änderungen

| Datei | Änderung | Status |
|-------|----------|--------|
| `src/contexts/ThemeContext.tsx` | Neuer Context für Theme-State | Committed |
| `src/hooks/useTheme.ts` | Custom Hook für Theme-Zugriff | Committed |
| `src/components/Settings/ThemeToggle.tsx` | Toggle-Komponente | Uncommitted |
| `src/styles/themes/dark.css` | Dark Mode CSS Variablen | Uncommitted |

### Erfolgreiche Ansätze

1. **CSS Custom Properties für Theming**
   - Was: Alle Farben als CSS Variablen definiert
   - Warum erfolgreich: Einfaches Switching ohne Component-Re-Renders
   - Relevante Dateien: `src/styles/themes/light.css`, `dark.css`

2. **localStorage für Persistenz**
   - Was: Theme-Präferenz in localStorage speichern
   - Warum erfolgreich: Funktioniert auch ohne Backend-Änderung

## Gescheiterte Versuche

### Versuch 1: Styled-Components ThemeProvider

**Was versucht**: Theme über Styled-Components ThemeProvider injizieren

**Fehlermeldung**:
```
Warning: Cannot update a component while rendering a different component
Error in useLayoutEffect when theme changes
```

**Warum gescheitert**: Race Condition zwischen Theme-Change und Component-Render. Styled-Components erfordert Re-Render aller Komponenten.

**Lessons Learned**: CSS Variablen sind performanter für globales Theming.

### Versuch 2: System Preference Detection

**Was versucht**: `prefers-color-scheme` Media Query als Default

**Problem**: Funktionierte, aber Override durch User-Setting war kompliziert

**Warum verworfen**: User-Präferenz sollte immer Vorrang haben. Media Query nur als Initial-Default.

## Aktueller Zustand

### Git Status

```
On branch feature/dark-mode-toggle
Changes not staged for commit:
  modified:   src/components/Settings/ThemeToggle.tsx
  modified:   src/styles/themes/dark.css

Untracked files:
  src/components/Settings/ThemeToggle.test.tsx
```

### Modified Files

| Datei | Beschreibung der Änderungen |
|-------|----------------------------|
| `ThemeToggle.tsx` | Toggle UI fertig, fehlt Animation |
| `dark.css` | 80% der Variablen definiert, Sidebar fehlt |

### Environment

- **Services**: Dev Server läuft auf localhost:3000
- **Dependencies**: Keine neuen Dependencies nötig
- **Browser-Support**: CSS Variables ab IE11 (Polyfill vorhanden)

## Nächste Schritte

### Priorität 1: Dark Theme für Sidebar vervollständigen

**Was**: CSS Variablen für Sidebar-Komponenten definieren

**Wo**: `src/styles/themes/dark.css:45-80`

**Wie**:
1. Sidebar Background Variable hinzufügen
2. Sidebar Border Color anpassen
3. Active Item Highlight für Dark Mode

**Akzeptanzkriterien**:
- [ ] Sidebar hat korrekten Dark Mode Background
- [ ] Kontrast-Ratio mindestens 4.5:1 (WCAG AA)
- [ ] Hover-States sichtbar

### Priorität 2: Toggle Animation

**Was**: Smooth Transition beim Theme-Wechsel

**Wo**: `src/components/Settings/ThemeToggle.tsx:23`

**Wie**:
1. CSS Transition auf body/html Element
2. 200ms ease-in-out für color und background-color
3. Kein Flash beim Initial Load (FOUC vermeiden)

### Priorität 3: Unit Tests

**Was**: Tests für ThemeContext und useTheme Hook

**Wo**: `src/contexts/ThemeContext.test.tsx` (neu erstellen)

**Wie**:
1. Test: Initial Theme aus localStorage
2. Test: Theme Toggle funktioniert
3. Test: System Preference als Fallback

## Wichtige Referenzen

### Relevante Dateien

| Datei | Zeilen | Warum relevant |
|-------|--------|----------------|
| `src/contexts/ThemeContext.tsx` | 1-45 | Zentrale Theme-Logik |
| `src/styles/themes/light.css` | - | Referenz für Variable-Namen |
| `src/App.tsx` | 12-15 | ThemeProvider muss hier wrappen |

### Dokumentation

- [CSS Custom Properties Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [WCAG Contrast Requirements](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

### Code-Patterns

```tsx
// So wird Theme im Projekt verwendet:
import { useTheme } from '@/hooks/useTheme';

function MyComponent() {
  const { theme, toggleTheme } = useTheme();
  return <button onClick={toggleTheme}>Current: {theme}</button>;
}
```

## Wichtige Hinweise

- **FOUC vermeiden**: Script in `<head>` muss Theme vor Render setzen (siehe `public/index.html:15`)
- **Nicht `!important` verwenden**: Alle Styles über CSS Variablen, keine Overrides
- **Test in Safari**: Safari hat Bug mit CSS Variables in Pseudo-Elements

## Für den nächsten Agent

Theme-System ist implementiert und funktioniert. Hauptarbeit ist CSS-Feinarbeit für Sidebar und Animation. Der ThemeContext in `src/contexts/ThemeContext.tsx` ist die zentrale Stelle. Beginne mit `dark.css:45` für die fehlenden Sidebar-Variablen.
```

## Beispiel 3: Mit Linear Issue

```markdown
# Handoff: API Rate Limiting

**Datum**: 2026-01-14 12:00
**Branch**: feature/TF-456-api-rate-limiting
**Linear Issue**: [TF-456](https://linear.app/team/issue/TF-456) - Implement API Rate Limiting

## Original-Aufgabe

Aus Linear Issue TF-456:
> Implementiere Rate Limiting für die Public API. Max 100 Requests/Minute pro API Key. 429 Response bei Überschreitung.

**Akzeptanzkriterien aus Linear**:
- [ ] Redis-basiertes Token Bucket
- [ ] Configurable Limits per Endpoint
- [ ] Proper 429 Response mit Retry-After Header

## Bereits erledigt

- Redis Client Setup in `src/lib/redis.ts`
- Rate Limiter Middleware Skeleton
- Unit Tests für Token Bucket Algorithmus

## Aktueller Zustand

**Linear Status**: In Progress
**Blocker**: Redis Connection in Staging Environment nicht konfiguriert

## Nächste Schritte

1. **DevOps kontaktieren**: Redis für Staging anfordern
2. **Middleware fertigstellen**: `src/middleware/rateLimiter.ts:45`
3. **Integration Tests**: Nach Redis-Setup

## Für den nächsten Agent

Rate Limiter Logik ist fertig, aber nicht testbar ohne Redis in Staging. Koordiniere mit DevOps (Ticket TF-457 erstellt) oder teste lokal mit Docker Redis.
```
